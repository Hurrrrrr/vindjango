from django.shortcuts import render
from .models import Answers, Wine
from .helpers import TastingNote
from .forms import AnswersForm, MainPageForm
from django.views.generic.detail import DetailView
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy 
import random

class MainPageFormView(FormView):
    template_name = 'vinapp/main_page_form.html'
    form_class = MainPageForm
    success_url = reverse_lazy('tasting-note-display')

    def form_valid(self, form):
        print("calling mainpage form_valid")
        scope = int(form.cleaned_data['scope'])
        accuracy = int(form.cleaned_data['accuracy'])

        filtered_wines = Wine.objects.filter(scope__lte=scope)
        if not filtered_wines.exists():
            print("filtered_wines doesn't exist")
        else:
            selected_wine = random.choice(filtered_wines)
            print(f"selected wine: {selected_wine}")
            tasting_note = TastingNote(selected_wine, accuracy)
            print(f"tasting note: {tasting_note}")
            self.request.session['tasting_note'] = tasting_note.generate_description()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasting_note'] = self.request.session.get('tasting_note')
        if 'tasting_note' in self.request.session:
            del self.request.session['tasting_note']
        return context
    

class TastingNoteDisplayView(FormView):
    template_name = 'vinapp/tasting_note_display.html'
    form_class= AnswersForm
    success_url = reverse_lazy('vinapp/results')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasting_note"] = self.request.session.get('tasting_note')  # I think this needs to be results, not tasting_note
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Here you can handle the form data
        # For example, you might want to create an Answers object and save it to the database
        return super().form_valid(form)

class ResultsView(TemplateView):
    template_name = 'vinapp/results.html'

def submit_answer(request):
    if request.method == 'POST':
        form = AnswersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a new page
    else:
        form = AnswersForm()

    return render(request, 'submit_answer.html', {'form': form})