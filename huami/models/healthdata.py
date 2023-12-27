import base64
from typing import Any
from django.db import models
from . import HuamiAccount

class Base64Field(models.TextField):
    def to_python(self, value: Any) -> Any:
        if isinstance(value, str):
            value = base64.b64decode(value)
        return super().to_python(value)

    def get_prep_value(self, value: Any) -> Any:
        if isinstance(value, bytes):
            value = base64.b64encode(value)
        return super().get_prep_value(value)
    
class HealthData(models.Model):
    """건강 데이터 저장을 위한 모델 클래스
    """    
    huami_account = models.ForeignKey(to=HuamiAccount, 
                                      on_delete=models.CASCADE,
                                      db_column="account",
                                      db_comment="account info",
                                      null=False,
                                      blank=False,
                                      help_text="huami 계정정보입니다.",
                                      related_name="health")
    date = models.DateField(null=False, 
                            blank=False,
                            db_column="date",
                            db_comment="기록 시간정보",
                            help_text="YYYY-MM-DD 형식으로 입력할 수 있습니다.")
    heart_rate = Base64Field(null=False,
                             blank=False,
                             db_column="heart",
                             db_comment="심박수",
                             help_text="1분 단위의 하루 심박수를 base64로 인코딩하여 저장")
    stress = Base64Field(null=False,
                         blank=False,
                         db_column="stress",
                         db_comment="스트레스",
                         help_text="1분 단위의 하루 스트레스를 base64로 인코딩하여 저장")
    spo2 = Base64Field(null=False,
                       blank=False,
                       db_column="spo2",
                       db_comment="혈중 산소포화도",
                       help_text="1분 단위의 하루 혈중 산소포화도를 base64로 인코딩하여 저장")
    step_count = Base64Field(null=False,
                             blank=False,
                             db_column="steps",
                             db_comment="걸음 수",
                             help_text="1분 단위의 하루 걸음수를 base64로 인코딩하여 저장")
    sleep_quality = Base64Field(null=False,
                                blank=False,
                                db_column="sleep",
                                db_comment="1분 단위의 수면의 질을 base64로 인코딩하여 저장")
    weight = models.FloatField(null=False,
                                 blank=False,
                                 db_column="weight",
                                 db_comment="무게(kg)",
                                 help_text="무게를 입력해주세요. (kg단위)")
    height = models.FloatField(null=False,
                               blank=False,
                               db_column="height",
                               db_comment="키(m)",
                               help_text="키를 입력해주세요. (m단위)")
    
    @property
    def bmi(self) -> float:
        return self.weight / (self.height^2)