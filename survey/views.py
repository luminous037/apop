from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from survey.models import Survey

# Create your views here.
class SurveyListView(ListView):
    template_name='survey/survey_list.html'
    model = Survey
    paginate_by = 5
    
    
class SurveyDetailView(DetailView):
    template_name='survey/survey_detail.html'
    model=Survey