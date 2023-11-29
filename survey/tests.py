from django.contrib.auth import get_user_model
from django.test import TestCase
from survey.models import Survey, SurveyQuestion, Question, Answer, QuestionAnswer, UserSurvey, Reply
from survey.models.question import TYPE_FILED
from django.conf import settings

# Create your tests here.
class SurveyTestCase(TestCase):
    def setUp(self):
        Survey.objects.create(title="survey1", description="survey1 description")
        Survey.objects.create(title="survey2", description="survey2 description")
        Survey.objects.create(title="survey3", description="survey3 description")

    def testCreation(self):
        # 테스트 데이터가 잘 생성되었는지 확인
        survey1: Survey = Survey.objects.get(title="survey1")
        self.assertEqual(survey1.description, "survey1 description")

    def testUpdate(self):
        # 테스트 데이터가 잘 수정되었는지 확인
        survey2: Survey = Survey.objects.get(title="survey2")
        survey2.description = "survey2 description updated"
        survey2.save()
        self.assertEqual(survey2.description, "survey2 description updated")


class SurveyQuestionTest(TestCase):
    def setUp(self):
        Survey.objects.create(title="survey1", description="survey1 description")
        Question.objects.create(title="question1", description="question1 description", type_filed=TYPE_FILED.radio)
        Question.objects.create(title="question2", description="question2 description", type_filed=TYPE_FILED.radio)

    def testCreation(self):
        # order를 안줬을 때 테스트 데이터가 잘 생성되었는지 확인
        survey_question = SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1")
        )
        self.assertEquals(survey_question.order, 1)

    def testDefaultOrder(self):
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

class QuestionAnswerCase(TestCase):
    def setUp(self):
        Question.objects.create(title="question1", description="question1 description", type_filed=TYPE_FILED.radio)
        Question.objects.create(title="question2", description="question2 description", type_filed=TYPE_FILED.text)
        Question.objects.create(title="question3", description="question3 description", type_filed=TYPE_FILED.text_area)
        Answer.objects.create(description="answer1 description")
        Answer.objects.create(description="answer2 description")
        Answer.objects.create(description="answer3 description")

    def testUpdate(self):
        # 테스트 데이터가 잘 수정되었는지 확인
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
    def setUp(self):
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