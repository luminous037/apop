from django.contrib import admin

from survey.models import UserSurvey, Reply

class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 0


class UserSurveyAdmin(admin.ModelAdmin):
    fields = ['user', 'survey']
    list_display = ['user', 'survey', 'create_at']
    ordering = ['user', 'create_at']
    search_fields = ['user__username', 'survey__title']
    search_help_text = "유저나 설문조사를 검색할 수 있습니다."
    
    inlines = [ReplyInline]

admin.site.register(UserSurvey, UserSurveyAdmin)
