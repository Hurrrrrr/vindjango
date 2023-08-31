# APP LEVEL URLs FILE

from django.urls import path
from . import views
from .views import MainPageFormView, TastingNoteDisplayView, ResultsView, start_over

app_name = 'vinapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('main-page-form/', MainPageFormView.as_view(), name='main-page-form'),
    path('tasting-note-display/', TastingNoteDisplayView.as_view(), name='tasting-note-display'),
    path('results/', ResultsView.as_view(), name='results'),
    path('start-over/', start_over, name='start-over'),
]
