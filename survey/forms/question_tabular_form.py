from django.forms import ModelForm, Select

from survey.models import SurveyQuestion


class QuestionTabularForm(ModelForm):
    class Meta:
        model = SurveyQuestion
        fields = ["title", "description", "type_filed"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control"}),
            "description": TextInput(attrs={"class": "form-control"}),
            "type_filed": Select(attrs={"class": "form-control"}),
        }