from django.contrib.auth import get_user_model
from django.test import TestCase
from survey.models import Survey, SurveyQuestion, Question, Answer, QuestionAnswer, UserSurvey, Reply
from survey.models.question import TYPE_FILED
from django.conf import settings

# Create your tests here.
class SurveyTestCase(TestCase):
    """Survey 모델 관련 테스트
    """    
    def setUp(self):
        """사전설정
        3개의 Survey 생성
        """        
        Survey.objects.create(title="survey1", description="survey1 description")
        Survey.objects.create(title="survey2", description="survey2 description")
        Survey.objects.create(title="survey3", description="survey3 description")

    def testCreation(self):
        """테스트 데이터가 잘 생성되었는지 확인
        """        
        survey1: Survey = Survey.objects.get(title="survey1")
        self.assertEqual(survey1.description, "survey1 description")

    def testUpdate(self):
        """테스트 데이터가 잘 수정되었는지 확인
        """        
        survey2: Survey = Survey.objects.get(title="survey2")
        survey2.description = "survey2 description updated"
        survey2.save()
        self.assertEqual(survey2.description, "survey2 description updated")


class SurveyQuestionTest(TestCase):
    """SurveyQuestion 모델 관련 테스트
    """    
    def setUp(self):
        """사전설정
        1개의 Survey와 2개의 Question 생성
        """        
        Survey.objects.create(title="survey1", description="survey1 description")
        Question.objects.create(title="question1", description="question1 description", type_filed=TYPE_FILED.radio)
        Question.objects.create(title="question2", description="question2 description", type_filed=TYPE_FILED.radio)

    def testCreation(self):
        """Order 생성 확인
        order를 비워놓았을 때 테스트 데이터가 잘 생성되었는지 확인
        """        
        survey_question = SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1")
        )
        self.assertEquals(survey_question.order, 1)

    def testDefaultOrder(self):
        """Order 기본값 생성 확인
        기본값으로 설정했을 때 order 값이 증가하는지 확인
        """        
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )
        survey_question = SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
        )
        self.assertEquals(survey_question.order, 2)

    def testChangeOrder(self):
        """Order 교환 확인
        생성 시에 order를 주었을 때
        두 개의 SurveyQeustion의 Order가 교환되는지 확인
        """        
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
            order=1
        )
        survey_question = SurveyQuestion.objects.get(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )

        self.assertEquals(survey_question.order, 2)

    def testChangeOrder2(self):
        """Order 교환 확인2
        메서드를 통해 order 교환이 이루어지는 지 확인
        """        
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
        )
        SurveyQuestion.objects.get(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        ).swap_order(2)
        survey_question2 = SurveyQuestion.objects.get(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
        )

        self.assertEquals(survey_question2.order, 1)
        
    def testManyRelated(self):
        """ManyToMany 관계에서 참조 확인
        Survey에서 Question 들을 참조할 수 있는지 확인
        """        
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
        )
        
        survey1 = Survey.objects.get(
            title="survey1"
        )
        
        self.assertTrue(survey1.questions.all().count() == 2)

class QuestionAnswerCase(TestCase):
    """QuestionAnswer 모델 관련 테스트
    """    
    def setUp(self):
        """사전설정
        3개의 Question과 3개의 Answer를 생성
        """        
        Question.objects.create(title="question1", description="question1 description", type_filed=TYPE_FILED.radio)
        Question.objects.create(title="question2", description="question2 description", type_filed=TYPE_FILED.text)
        Question.objects.create(title="question3", description="question3 description", type_filed=TYPE_FILED.text_area)
        Answer.objects.create(description="answer1 description")
        Answer.objects.create(description="answer2 description")
        Answer.objects.create(description="answer3 description")

    def testUpdate(self):
        """Order의 변경이 잘 되는지 확인
        """        
        QuestionAnswer.objects.create(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer1 description"),
        )
        QuestionAnswer.objects.create(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer2 description"),
        )
        QuestionAnswer.objects.get(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer1 description"),
        ).swap_order(2)
        question_answer = QuestionAnswer.objects.get(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer2 description"),
        )
        self.assertEqual(question_answer.order, 1)


class UserSurveyCase(TestCase):
    """UserSurvey 모델 관련 테스트
    """    
    def setUp(self):
        """사전설정
        1개의 Survey, 1개의 Question, 3개의 Answer
        Survey에 Question을 연결
        Question에 3개의 Answer를 연결
        User를 생성
        """        
        Survey.objects.create(title="survey1", description="survey1 description")
        Question.objects.create(title="question1", description="question1 description", type_filed=TYPE_FILED.radio)
        Answer.objects.create(description="answer1 description")
        Answer.objects.create(description="answer2 description")
        Answer.objects.create(description="answer3 description")
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
        )
        SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question3"),
        )
        QuestionAnswer.objects.create(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer1 description"),
        )
        QuestionAnswer.objects.create(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer2 description"),
        )
        QuestionAnswer.objects.create(
            question=Question.objects.get(title="question1"),
            answer=Answer.objects.get(description="answer3 description"),
        )
        get_user_model().objects.create(username="testuser", password="testuser")

    def createUserSurvey(self):
        """답변 확인
        작성한 답변이 정상적으로 저장되었는지 확인
        """        
        user_survey = UserSurvey.objects.create(
            user=get_user_model().objects.get(username="testuser"),
            survey=Survey.objects.get(title="survey1"),
        )
        reply = Reply.objects.create(
            user_survey=user_survey,
            question=Question.objects.get(title="question1"),
            content="answer1 description"
        )
        self.assertEquals(reply.content, "answer1 description")