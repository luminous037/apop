from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from survey.models import Survey, Question, UserSurvey, Reply, SurveyQuestion
from django.views.generic.edit import ProcessFormView
from django.shortcuts import render

# Create your views here.
class SurveyListView(ListView):
    """참여 가능한 설문 목록을 제공하는 클래스 기반 뷰
    """    
    template_name='survey/survey_list.html'
    model = Survey
    paginate_by = 5
    
    
class SurveyDetailView(DetailView):
    """설문에 대한 구체적인 정보를 제공하는 클래스 기반 뷰
    TODO 구현예정
    """    
    template_name='survey/survey_detail.html'
    model=Survey
    
    
class SurveyFormView(ProcessFormView):
    """설문조사 폼을 제공하는 클래스 기반 뷰
    """
    
    def _create_replies(self, user_survey, post_data):
        """응답들을 생성하기 위한 메서드

        Args:
            user_survey (UserSurvey): 유저가 실시한 설문조사(새로 만들어진)
            post_data (QueryDict): 폼으로 입력받은 데이터
        """        
        for key, value in post_data.items():
            if not key.isdigit(): # for excepting csrf_token
                continue
            
            question = Question.objects.get(pk=int(key))
            survey_question = SurveyQuestion.objects.get(survey=user_survey.survey, 
                                                         question=question)
            Reply.objects.create(user_survey=user_survey,
                                 survey_question=survey_question,
                                 content=value)

    def get(self, request, *args, **kwargs):
        """폼 입력 화면

        Args:
            request (HttpRequest): HttpRequest정보

        Returns:
            HttpResponse: 렌더링 된 입력 화면 HTML
        """        
        context = {'object': Survey.objects.get(**kwargs)}
        return render(request, 'survey/user_survey_form.html', context)
    
    def post(self, request, *args, **kwargs):
        """폼 제출 화면

        Args:
            request (HttpRequest): HttpRequest정보

        Returns:
            HttpResponse: 렌더링 된 완료 화면 HTML
        """        
        self._create_replies(UserSurvey.objects.create(user=request.user,
                                                       survey=Survey.objects.get(**kwargs)),
                             request.POST)
        
        return render(request, 'survey/survey_complete.html')
    
    def put(self, request, *args, **kwargs):
        """작성된 설문 수정 화면
        
        Args:
            request (HttpRequest): HttpRequest정보
        
        Returns:
            HttpResponse: 렌더링 된 완료 화면 HTML
        """        
        return render(request, 'survey/survey_complete.html')
    