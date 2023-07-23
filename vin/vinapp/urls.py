from django.urls import path
from . import views
from .views import MainPageFormView, TastingNoteDisplayView, ResultsView

app_name = 'vinapp'

urlpatterns = [
    path('main-page-form/', MainPageFormView.as_view(), name='main-page-form'),
    path('tasting-note-display/', TastingNoteDisplayView.as_view(), name='tasting-note-display'),
    path('results/', ResultsView.as_view(), name='results'),
]
