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

    @property
    def next_order(self) -> int:
        return QuestionAnswer.objects.filter(question=self.question).count() + 1

    def exist_order(self) -> bool:
        return QuestionAnswer.objects.filter(question=self.question, order=self.order).exists()

    def swap_order(self, order: int):
        if order == self.order:
            return
        question_answer = QuestionAnswer.objects.get(
            question=self.question,
            order=order
        )
        question_answer.order, self.order = self.order, question_answer.order
        question_answer.save()
        self.save()

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.next_order
        if self.exist_order():
            QuestionAnswer.objects.filter(
                question=self.question,
                order=self.order
            ).update(
                order=self.next_order
            )

        super().save(*args, **kwargs)