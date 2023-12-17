from django.urls import path
from django.views.generic import TemplateView
from survey.views import SurveyListView, SurveyDetailView, SurveyFormView

app_name = 'survey'

urlpatterns = [
    path('<int:pk>', SurveyFormView.as_view(), name='survey-detail'),
    path('', SurveyListView.as_view(), name='survey-list'),
]