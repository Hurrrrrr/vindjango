from django.shortcuts import render
from .models import UserAnswers, Wine
from .helpers import TastingNote, ResultsLogic, UserResults
from .forms import UserAnswersForm, MainPageForm
from django.views.generic.detail import DetailView
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import random

class MainPageFormView(FormView):
    template_name = 'vinapp/main_page_form.html'
    form_class = MainPageForm
    success_url = reverse_lazy('vinapp:tasting-note-display')

    def form_valid(self, form):
        self.select_random_wine(form)
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
            tasting_note = TastingNote(selected_wine, accuracy)
            self.request.session['tasting_note'] = tasting_note.generate_description()

class TastingNoteDisplayView(FormView):
    template_name = 'vinapp/tasting_note_display.html'
    form_class= UserAnswersForm
    success_url = reverse_lazy('vinapp:results')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasting_note"] = self.request.session.get('tasting_note')
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):

        user_answers = UserAnswers.objects.create(
            grape = form.cleaned_data['grape'],
            country = form.cleaned_data['country'],
            region = form.cleaned_data['region'],
            appellation = form.cleaned_data['appellation'],
            vintage = form.cleaned_data['vintage']
        )

        wine_id = self.request.session.get('selected_wine_id')
        del self.request.session['selected_wine_id']
        selected_wine = Wine.objects.get(id = wine_id)

        results_logic = ResultsLogic(user_answers, selected_wine)
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
        # use this later?
        # self.request.session['user_results_id'] = user_results.id

        return HttpResponseRedirect(self.get_success_url())

class ResultsView(TemplateView):
    template_name = 'vinapp/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.request.session.get('results_string')
        if 'results_string' in self.request.session:
            del self.request.session['results_string']
        return context
    

def submit_answer(request):
    if request.method == 'POST':
        form = UserAnswersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserAnswersForm()

    return render(request, 'submit_answer.html', {'form': form})