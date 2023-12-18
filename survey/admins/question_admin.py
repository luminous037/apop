from django.contrib import admin
from survey.models import Question


class AnswerInline(admin.StackedInline):
    """Question 어드민에서 응답 가능한 Answer들을 나타내기 위한 클래스
    """    
    model = Question.answers.through
    extra = 0


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    """Question 모델 어드민
    """    
    fields = ['type_filed', 'title', 'description']
    list_display = ['title', 'description']
    list_display_links = ['title']
    search_fields = ['title', 'description']
    search_help_text = "제목이나 설명을 입력하세요"

    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
