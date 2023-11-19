from django.contrib import admin

from survey.models import Answer


class AnswerAdmin(admin.ModelAdmin):
    fields = ['description']
    list_display = ['description']
    list_display_links = ['description']
    search_fields = ['description']
    search_help_text = "설명을 입력하세요"


admin.site.register(Answer, AnswerAdmin)