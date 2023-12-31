# APP LEVEL URLs File

from django.urls import path
from . import views
from .views import MainPageFormView, TastingNoteDisplayView, ResultsView, ContactFormView, start_over
from django.views.generic import TemplateView

app_name = 'vinapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('main-page-form/', MainPageFormView.as_view(), name='main-page-form'),
    path('tasting-note-display/', TastingNoteDisplayView.as_view(), name='tasting-note-display'),
    path('results/', ResultsView.as_view(), name='results'),
    path('start-over/', start_over, name='start-over'),
    path('info/', TemplateView.as_view(template_name='info.html'), name='info'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('bio/', TemplateView.as_view(template_name='bio.html'), name='bio'),
]
