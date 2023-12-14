from django.contrib import admin

# Register your models here.
from huami.models import HuamiAccount

class HuamiAccountAdmin(admin.ModelAdmin):
    fields = ['user', 'email', 'password', 'sync_date']
    list_display = ['user', 'email', 'sync_date']
    ordering = ['user', 'sync_date']
    search_fields = ['email', 'password']
    search_help_text = "유저나 설문조사를 검색할 수 있습니다."

admin.site.register(HuamiAccount, HuamiAccountAdmin)