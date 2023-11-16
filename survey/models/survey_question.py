from django.db import models


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(
        to="Survey",
        db_comment="survey",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        to="Question",
        db_comment="question",
        on_delete=models.CASCADE,
    )
    order = models.IntegerField(
        db_column="order",
        db_comment="question order",
        null=False,
        blank=False,
        help_text="질문 순서"
    )

    class Meta:
        db_table = "survey_question"
        verbose_name = "설문조사 질문"
        verbose_name_plural = "설문조사 질문"
        ordering = ["survey", "order"]
