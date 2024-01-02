import base64
import csv
import json
from django.test import TestCase

from huami.configs.payloads import PAYLOADS
from huami.models import HuamiAccount, HealthData
from huami.utils import HuamiAmazfit
from django.contrib.auth import get_user_model


# Create your tests here.
class HuamiAccountTestCase(TestCase):
    """HuamiAccount 모델 관련 테스트
    """    
    def setUp(self):
        """Correct 계정과 Wrong 계정 설정
        Manual로 해주어야 함
        """        
        user = get_user_model().objects.create(username='testman', password='test1')
        self.correct_email = ""
        self.correct_password = ""
        self.wrong_email = ""
        self.wrong_password = ""
        self.huami = HuamiAccount.objects.create(user=user, email=self.correct_email, password=self.correct_password)
        self.correct_huami_account = HuamiAmazfit(self.correct_email, self.correct_password)
        self.invalid_huami_account = HuamiAmazfit(self.wrong_email, self.wrong_password)

    def testHuamiGetAccessToken(self):
        """계정이 존재하는지 확인
        """        
        self.correct_huami_account.access()
        self.assertIsNotNone(self.correct_huami_account.access_token)

    def testHuamiGetAccessTokenWrongEmail(self):
        """틀린 계정에 대한 결과 확인
        """        
        huami = HuamiAmazfit(self.wrong_email, self.correct_password)
        with self.assertRaises(ValueError):
            huami.access()

    def testHuamiLogout(self):
        """logout이 정상 수행되는지 확인
        """        
        self.correct_huami_account.access()
        self.correct_huami_account.login()
        self.correct_huami_account.logout()

    def testHuamiProfile(self):
        """profile 데이터가 수신되는지 확인
        """        
        self.correct_huami_account.access()
        self.correct_huami_account.login()
        response = self.correct_huami_account.profile()
        self.correct_huami_account.logout()

        self.assertTrue(isinstance(response, dict))

    def testRequestData(self):
        """전달받은 데이터의 형식 확인을 위해 json파일로 저장
        """        
        self.correct_huami_account.access()
        self.correct_huami_account.login()
        band_response = self.correct_huami_account.band_data('2000-01-01', '2023-12-13')
        stress_response = self.correct_huami_account.stress('2000-01-01', '2023-12-13')
        blood_response = self.correct_huami_account.blood_oxygen('2000-01-01', '2023-12-13')
        
        with open(file='log.json', mode='w') as file:
            file.write('{"band data":')
            file.write(json.dumps(band_response))
            file.write(",")
            file.write('"stress data":')
            file.write(json.dumps(stress_response))
            file.write(",")
            file.write('"blood response":')
            file.write(json.dumps(blood_response))
            file.write("}")
        
        # self.correct_huami_account.logout()
            
    def testGetData(self):
        """HaumiAccount모델에서 데이터를 가져오는 것 검사
        """        
        result = self.huami.get_data()
        with open(file='log.json', mode='w') as file:
            file.write(json.dumps(result))
            
    def dataSave(self):
        with open(file='data/userdata.csv', mode='r') as file:
            user_data = csv.reader(file)
            
            for user in user_data:
                self.huami.email = user[2]
                self.huami.password = user[3]
                with open(file=f'data/{user[1].replace(" ", "_")}.json', mode='w') as saved_file:
                    saved_file.write(json.dumps(self.huami.get_data()))
                    
    
    def testRecordingHealth(self):
        """서버에서 수신한 데이터가 db에 잘 저장되는지 확인
        """        
        HealthData.create_from_sync_data(self.huami)
        
        for i in HealthData.objects.filter(huami_account=self.huami):
            print(i.date, i.heart_rate, i.sleep_quality, i.step_count, i.stress, i.spo2, i.weight, i.height, i.age)