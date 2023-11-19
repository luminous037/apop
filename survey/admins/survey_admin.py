from django.contrib import admin
from survey.models import Survey, Question


class QuestionInline(admin.StackedInline):
    model = Survey.questions.through
    extra = 0


# Register your models here.
class SurveyAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    list_display = ['title', 'description', 'created_at', 'updated_at']
    list_display_links = ['title']
    ordering = ['created_at']
    search_fields = ['title', 'description']
    search_help_text = "제목이나 설명을 입력하세요"

    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)
