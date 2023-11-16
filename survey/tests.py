from django.test import TestCase
from survey.models import Survey


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
