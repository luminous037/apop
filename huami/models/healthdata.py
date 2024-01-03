from typing import Any
from django.db import models
from . import HuamiAccount

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
    heart_rate = models.TextField(null=True,
                             blank=False,
                             db_column="heart",
                             db_comment="심박수",
                             help_text="1분 단위의 하루 심박수를 문자열로 저장")
    stress = models.TextField(null=True,
                         blank=False,
                         db_column="stress",
                         db_comment="스트레스",
                         help_text="1분 단위의 하루 스트레스를 문자열로 저장")
    spo2 = models.TextField(null=True,
                       blank=False,
                       db_column="spo2",
                       db_comment="혈중 산소포화도",
                       help_text="1분 단위의 하루 혈중 산소포화도를 문자열로 저장")
    step_count = models.TextField(null=True,
                             blank=False,
                             db_column="steps",
                             db_comment="걸음 수",
                             help_text="1분 단위의 하루 걸음수를 문자열로 저장")
    sleep_quality = models.TextField(null=True,
                                blank=False,
                                db_column="sleep",
                                db_comment="1분 단위의 수면의 질을 문자열로 저장")
    weight = models.FloatField(null=True,
                                 blank=False,
                                 db_column="weight",
                                 db_comment="무게(kg)",
                                 help_text="무게를 입력해주세요. (kg단위)")
    height = models.FloatField(null=True,
                               blank=False,
                               db_column="height",
                               db_comment="키(m)",
                               help_text="키를 입력해주세요. (m단위)")
    age = models.IntegerField(null=True,
                              blank=False,
                              db_column="age",
                              db_comment="나이",
                              help_text="나이를 입력하세요 (세)")
    
    @classmethod
    #Code Smell
    def create_from_sync_data(cls, huami_account: HuamiAccount) -> tuple:
        """Huami서버에서 가져온 데이터를 DB에 저장

        Args:
            huami_account (HuamiAccount): Huami 계정
        
        Returns:
            tuple[HealthData]: 동기화된 건강 기록 데이터들
        """        
        def _get_or_create() -> tuple[HealthData, bool]:
            """각 날짜마다 중복되는 작업들의 모임
            만약 데이터가 새로 생성되었으면 무게, 키, 나이를 설정

            Returns:
                tuple[HealthData, bool]: 기존에 있었거나 새로 생성된 오브젝트와 오브젝트 생성여부(created)
            """      
            health, created = HealthData.objects.get_or_create(huami_account=huami_account, date=date)
            if created:
                health.weight = result['profile']['weight']
                health.height = result['profile']['height']
                health.age = int(date.split("-")[0]) - int(result['profile']['birth'].split("-")[0])
            
            return health, created
        updated_health = []
        result = huami_account.get_data()
        
        for date in result['band'].keys():
            health, _ = _get_or_create()
            health.heart_rate = result['band'][date]['heart']
            health.step_count = result['band'][date]['steps']
            health.sleep_quality = result['band'][date]['sleeps']
            health.save()
            updated_health.append(health)
        
        for date in result['stress'].keys():
            health, _ = _get_or_create()
            health.stress = result['stress'][date]
            health.save()
            updated_health.append(health)
        
        for date in result['blood'].keys():
            health, _ = _get_or_create()
            health.spo2 = result['blood'][date]
            health.save()
            updated_health.append(health)
            
        return set(updated_health)
        
    
    @property
    def bmi(self) -> float:
        return self.weight / (self.height*self.height)
    
    class Meta:
        verbose_name = "건강 데이터"
        verbose_name_plural = "건강 데이터"