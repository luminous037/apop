from django.contrib import admin

from survey.models import UserSurvey


class UserSurveyAdmin(admin.ModelAdmin):
    fields = ['user', 'survey', 'create_at']
    list_display = ['user', 'survey', 'create_at']
    ordering = ['create_at']
    search_fields = ['user', 'survey']
    search_help_text = "유저나 설문조사를 검색할 수 있습니다."

admin.site.register(UserSurvey, UserSurveyAdmin)
