from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from survey.models import Survey, Question, UserSurvey, Reply, SurveyQuestion
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
        survey = Survey.objects.get(**kwargs)
        user_survey = UserSurvey.objects.get_or_create(user=request.user,
                                                       survey=survey)
        
        if user_survey[1] == False:
            """
            error 발생
            """
            pass
        
        user_survey=user_survey[0]
        
        for key, value in request.POST.items():
            if not key.isdigit():
                continue
            question = Question.objects.get(pk=int(key))
            
            Reply.objects.create(user_survey=user_survey,
                                 survey_question=SurveyQuestion.objects.get(survey=survey,
                                                                            question=question),
                                 content=value)
        
        return render(request, 'survey/survey_complete.html')
    
    def put(self, *args, **kwargs):
        pass
    