from django.test import TestCase

from huami.configs.payloads import PAYLOADS
from huami.models import HuamiAccount
from huami.utils import HuamiAmazfit


# Create your tests here.
class HuamiAccountTestCase(TestCase):
    """HuamiAccount 모델 관련 테스트
    """    
    def setUp(self):
        """Correct 계정과 Wrong 계정 설정
        Manual로 해주어야 함
        """        
        self.correct_email = ""
        self.correct_password = ""
        self.wrong_email = ""
        self.wrong_password = ""
        self.correct_huami_account = HuamiAmazfit(self.correct_email, self.correct_password)
        self.invalid_huami_account = HuamiAccount(self.wrong_email, self.wrong_password)

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

        self.assertTrue(response.status_code == 200)

    def testBandData(self):
        """band 센서 데이터가 수신되는지 확인
        """        
        self.correct_huami_account.access()
        self.correct_huami_account.login()
        band_response = self.correct_huami_account.band_data('2000-01-01', '2023-12-13')
        stress_response = self.correct_huami_account.stress('0', '1690803229711')
        blood_response = self.correct_huami_account.blood_oxygen('2019-01-01T00:00:00', '2023-07-31T20:33:52')

        self.correct_huami_account.logout()
        self.assertTrue(band_response.status_code == 200 and
                        stress_response.status_code == 200 and
                        blood_response.status_code == 200)
