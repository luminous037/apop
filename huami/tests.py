from django.test import TestCase

from huami.configs.payloads import PAYLOADS
from huami.models import HuamiAccount
from huami.utils import HuamiAmazfit


# Create your tests here.
class HuamiAccountTestCase(TestCase):
    def setUp(self):
        self.correct_email = ""
        self.correct_password = ""
        self.wrong_email = ""
        self.wrong_password = ""

    def testHuamiGetAccessToken(self):
        huami = HuamiAmazfit(self.correct_email, self.correct_password)
        huami.access()
        self.assertIsNotNone(huami.access_token)

    def testHuamiGetAccessTokenWrongEmail(self):
        huami = HuamiAmazfit(self.wrong_email, self.correct_password)
        with self.assertRaises(ValueError):
            huami.access()

    def testHuamiLogin(self):
        huami = HuamiAmazfit(self.correct_email, self.correct_password)
        huami.access()
        huami.login()
        self.assertIsNotNone(huami.app_token)
        self.assertIsNotNone(huami.login_token)
        self.assertIsNotNone(huami.user_id)

    def testHuamiLogout(self):
        huami = HuamiAmazfit(self.correct_email, self.correct_password)
        huami.access()
        huami.login()
        huami.logout()
        self.assertIsNone(huami.app_token)
        self.assertIsNone(huami.login_token)
        self.assertIsNone(huami.user_id)