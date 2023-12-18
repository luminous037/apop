from django.contrib import admin
from survey.models import Survey, Question


class QuestionInline(admin.StackedInline):
    """Survey 어드민에서 Question들을 나타내기 위한 클래스
    """    
    model = Survey.questions.through
    extra = 0


# Register your models here.
class SurveyAdmin(admin.ModelAdmin):
    """Survey 모델 어드민
    """
    fields = ['title', 'description']
    list_display = ['title', 'description', 'created_at', 'updated_at']
    list_display_links = ['title']
    ordering = ['created_at']
    search_fields = ['title', 'description']
    search_help_text = "제목이나 설명을 입력하세요"

    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)
