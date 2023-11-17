from django.test import TestCase
from survey.models import Survey, SurveyQuestion, Question


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
        Question.objects.create(title="question1", description="question1 description")
        Question.objects.create(title="question2", description="question2 description")

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
        survey_question = SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question1"),
        )
        survey_question2 = SurveyQuestion.objects.create(
            survey=Survey.objects.get(title="survey1"),
            question=Question.objects.get(title="question2"),
        )
        survey_question.swap_order(2)
        self.assertEquals(survey_question2.order, 1)
