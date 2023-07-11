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
        scope = form.cleaned_data['scope']
        accuracy = form.cleaned_data['accuracy']

        filtered_wines = Wine.objects.filter(scope__lte=scope)
        selected_wine = random.choice(filtered_wines)
        tasting_note = TastingNote(selected_wine, accuracy)
        form.instance.tasting_note = tasting_note.generate_description()

        return super().form_valid(form)

class TastingNoteDisplayView(FormView):
    model = TastingNote
    template_name = 'vinapp/tasting_note_display.html'
    form_class= AnswersForm

    def get_object(self):
        # Here you can access the data from the form and create the TastingNote object.
        # For now, just return an instance of TastingNote. You will need to implement the
        # actual logic to get the data from the form and generate the TastingNote.
        return TastingNote()
    
    def get_success_url(self):
        return reverse_lazy('vinapp/results.html')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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