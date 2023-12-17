from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from survey.models import Survey
from django.views.generic.edit import ProcessFormView
from django.shortcuts import render

# Create your views here.
class SurveyListView(ListView):
    template_name='survey/survey_list.html'
    model = Survey
    paginate_by = 5
    
    
class SurveyDetailView(DetailView):
    template_name='survey/survey_detail.html'
    model=Survey
    
    
class SurveyFormView(ProcessFormView):

    def get(self, request, *args, **kwargs):
        context = {'object': Survey.objects.get(**kwargs)}
        return render(request, 'survey/user_survey_form.html', context)
    
    def post(self, request, *args, **kwargs):
        print(request.POST.keys())
        return render(request, 'survey/survey_complete.html')
    
    def put(self, *args, **kwargs):
        pass
    