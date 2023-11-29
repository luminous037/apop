from django.db import models


class Reply(models.Model):
    user_survey = models.ForeignKey("UserSurvey", on_delete=models.CASCADE, related_name="replies")
    survey_question = models.ForeignKey("SurveyQuestion", on_delete=models.CASCADE, related_name="replies")
    content = models.TextField(
        db_column="content",
        db_comment="reply to question",
        null=False,
        blank=True,
        help_text="답변",
    )

    class Meta:
        db_table = "reply"
        verbose_name = "답변"
        verbose_name_plural = "답변"
        ordering = ["user_survey", "question"]

    @property
    def title(self) -> str:
        return self.survey_question.question.title

    @property
    def order(self) -> int:
        return self.survey_question.order
