# APP LEVEL URLs FILE

from django.urls import path
from . import views
from .views import MainPageFormView, TastingNoteDisplayView, ResultsView, start_over
from django.views.generic import TemplateView

app_name = 'vinapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('main-page-form/', MainPageFormView.as_view(), name='main-page-form'),
    path('tasting-note-display/', TastingNoteDisplayView.as_view(), name='tasting-note-display'),
    path('results/', ResultsView.as_view(), name='results'),
    path('start-over/', start_over, name='start-over'),
    path('info/', TemplateView.as_view(template_name='info.html'), name='info'),
    path('how-to-play/', TemplateView.as_view(template_name='how_to_play.html'), name='how_to_play'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('bio/', TemplateView.as_view(template_name='bio.html'), name='bio'),
]
