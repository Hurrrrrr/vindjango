from django.shortcuts import render
from .models import Answers
from .forms import AnswersForm
from django.views.generic.edit import FormView
from .forms import MainPageForm

class MainPageFormView(FormView):
    template_name = 'vinapp/main_page_form.html'
    form_class = MainPageForm
    success_url = '/tbd'   # or whatever the url ends up being

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # Here you can process the data before redirecting the user.

        # For example, you can store the form data in the session:
        self.request.session['scope'] = form.cleaned_data['scope']
        self.request.session['accuracy'] = form.cleaned_data['accuracy']

        # Then you can return the super class's form_valid method.
        # This will redirect the user to the URL specified in success_url.
        return super().form_valid(form)

def submit_answer(request):
    if request.method == 'POST':
        form = AnswersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a new page
    else:
        form = AnswersForm()

    return render(request, 'submit_answer.html', {'form': form})