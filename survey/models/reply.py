from django.db import models


class Reply(models.Model):
    user_survey = models.ForeignKey("UserSurvey", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
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

    def to_answer_list(self) -> list[str]:
        return [self.question.title, self.content]