from django.contrib import admin

# Register your models here.
from huami.models import HuamiAccount, HealthData

class HuamiAccountAdmin(admin.ModelAdmin):
    """HuamiAccount 모델 어드민
    """    
    fields = ['user', 'email', 'password', 'sync_date', 'note']
    list_display = ['user', 'email', 'sync_date', 'note']
    ordering = ['user', 'sync_date']
    search_fields = ['user__username', 'email']
    search_help_text = "유저나 화웨이 계정으로 검색할 수 있습니다"
    

class HealthDataAdmin(admin.ModelAdmin):
    """HealthData 모델 어드민
    """    
    ordering = ['huami_account', 'date']
    search_fields = ['huami_account__user__username', 'date']
    search_help_text = "유저나 날짜로 검색할 수 있습니다."

admin.site.register(HuamiAccount, HuamiAccountAdmin)
admin.site.register(HealthData, HealthDataAdmin)