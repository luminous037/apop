from django.contrib import admin


# Register your models here.
class SurveyAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    list_display = ['title', 'description', 'created_at', 'updated_at']
    list_display_links = ['title']
    ordering = ['created_at']
    search_fields = ['title', 'description']
    search_help_text = "제목이나 설명을 입력하세요"
