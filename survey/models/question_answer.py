from django.db import models


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        to="Question",
        db_comment="question",
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        to="Answer",
        db_comment="answer",
        on_delete=models.CASCADE,
    )
    order = models.IntegerField(
        db_column="order",
        db_comment="answer order",
        null=False,
        blank=False,
        help_text="답변 순서"
    )

    class Meta:
        db_table = "question_answer"
        verbose_name = "질문 답변"
        verbose_name_plural = "질문 답변"
        ordering = ["question", "order"]