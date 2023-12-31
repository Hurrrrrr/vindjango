from .models import UserAnswers, Wine
from .helpers import TastingNote, ResultsLogic, UserResults
from .forms import UserAnswersForm, MainPageForm
from django.conf import settings
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
import random, json

class MainPageFormView(FormView):
    template_name = 'main_page_form.html'
    form_class = MainPageForm
    success_url = reverse_lazy('vinapp:tasting-note-display')

    def form_valid(self, form):
        selected_wine = self.select_random_wine(form)
        self.request.session['chart_data'] = json.dumps(self.prepare_chart_data(selected_wine))
        self.request.session['color_data'] = json.dumps(self.prepare_color_data(selected_wine))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['tasting_note'] = self.request.session.get('tasting_note')
        if 'tasting_note' in self.request.session:
            del self.request.session['tasting_note']
        return context
        
    def select_random_wine(self, form):
        scope = int(form.cleaned_data['scope'])
        accuracy = int(form.cleaned_data['accuracy'])

        filtered_wines = Wine.objects.filter(scope__lte=scope)
        if not filtered_wines.exists():
            print("filtered_wines doesn't exist")
        else:
            selected_wine = random.choice(filtered_wines)
            self.request.session['selected_wine_id'] = selected_wine.id
            self.create_tasting_note(selected_wine, accuracy)
            return selected_wine
            
    def create_tasting_note(self, wine_obj, accuracy):
        tasting_note = TastingNote(wine_obj, accuracy)
        self.request.session['tasting_note'] = tasting_note.generate_description()
    
    def prepare_chart_data(self, wine_obj):

        chart_data = {
            'sweetness': wine_obj.sweetness,
            'acidity': wine_obj.acidity,
            'body': wine_obj.body,
            'alcohol': self.scale_alcohol(wine_obj),
            'tannin_or_bitterness': wine_obj.tannin_or_bitterness,
            'finish': wine_obj.finish
        }

        return chart_data
    
    # convert wine.alcohol (which is abv * 10) into value to be used in chart:
    # 14.5 = high, 13.5 = med+, 12.5 = med, 11.5 = med-, 10.5 = low, 10 = min
    def scale_alcohol(self, wine_obj):
        abv = wine_obj.alcohol / 10
        if abv < 10: return 0

        TARGET_ALC = 14.5
        TARGET_VALUE = 225
        MIN_ALC = 10    # the highest value which will bottom out the chart

        chart_alcohol = (abv - MIN_ALC) * (TARGET_VALUE / (TARGET_ALC - MIN_ALC))

        return chart_alcohol
    
    # wine.sweetness is the residual sugar of the wine in grams/litre
    # this doesn't work well for dry wines, since the vast majority are
    # <= 5g/l, which when scaled to the chart (which displays 0-255)
    # is too difficult to read, so this converts that into a subjective
    # (and therefore somewhat arbitrary) value for display
    # TODO: finish this. perhaps fix the overlap problem
    def scale_sweetness(self, wine_obj):
        sugar = wine_obj.sweetness
        output = 0
        if sugar < 3:
            return output * 10
        elif sugar < 5:
            return output * 8 
        elif sugar < 20:
            return output * 4

    
    def prepare_color_data(self, wine_obj):

        color_data = {
            'appearance_red': wine_obj.appearance_red,
            'appearance_green': wine_obj.appearance_green,
            'appearance_blue': wine_obj.appearance_blue
        }

        print(color_data)
        return color_data

class TastingNoteDisplayView(FormView):
    template_name = 'tasting_note_display.html'
    form_class = UserAnswersForm
    success_url = reverse_lazy('vinapp:results')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasting_note"] = self.request.session.get('tasting_note')
        context['chart_data'] = self.request.session.get('chart_data')
        context['color_data'] = json.loads(self.request.session.get('color_data', '{}'))
        # if 'tasting_note' in self.request.session:
        #     del self.request.session['tasting_note']
        # if 'chart_data' in self.request.session:
        #     del self.request.session['chart_data']
        # if 'color_data' in self.request.session:
        #     del self.request.session['color_data']
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):

        user_answers = self.create_user_answers_obj(form)
        selected_wine = self.retrieve_selected_wine()
        self.process_answers(user_answers, selected_wine)

        return HttpResponseRedirect(self.get_success_url())
    
    def create_user_answers_obj(self, form):

        answers = UserAnswers.objects.create(
            grape = form.cleaned_data['grape'],
            country = form.cleaned_data['country'],
            region = form.cleaned_data['region'],
            appellation = form.cleaned_data['appellation'],
            vintage = form.cleaned_data['vintage']
        )

        return answers
    
    def retrieve_selected_wine(self):
        wine_id = self.request.session.get('selected_wine_id')
        if 'selected_wine_id' in self.request.session:
            del self.request.session['selected_wine_id']
        selected_wine = Wine.objects.get(id = wine_id)
        return selected_wine
    
    # creates logic instance, stores formatted results in session for use 
    # in ResultsView, creates and saves UserResults instance
    def process_answers(self, user_answers_obj, wine_obj):

        results_logic = ResultsLogic(user_answers_obj, wine_obj)
        results_logic.check_user_answers()
        results_logic.update_score()

        results_string = results_logic.get_formatted_results()
        self.request.session['results_string'] = results_string

        results_list = results_logic.create_results_list()
        scores_list = results_logic.create_scores_list()

        user_results = UserResults.objects.create(
            grape = results_list[0],
            country = results_list[1],
            region = results_list[2],
            appellation = results_list[3],
            vintage = results_list[4],
            grape_score = scores_list[0],
            country_score = scores_list[1],
            region_score = scores_list[2],
            appellation_score = scores_list[3],
            vintage_score = scores_list[4]
        )

        user_results.save()

class ResultsView(TemplateView):
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.request.session.get('results_string')
        if 'results_string' in self.request.session:
            del self.request.session['results_string']
        return context

class ContactFormView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contact.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        send_mail(
            subject,
            f'Message from {name} <{email}>:\n\n{message}',
            settings.DEFAULT_FROM_EMAIL,
            ['jonahpalmer@gmail.com'],
        )

        return HttpResponse('Thank you for your message.')
    
def submit_answer(request):
    if request.method == 'POST':
        form = UserAnswersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserAnswersForm()

    return render(request, 'submit_answer.html', {'form': form})

def start_over(request):
    request.session.flush()
    return redirect('vinapp:main-page-form')

def index(request):
    return render(request, 'index.html')