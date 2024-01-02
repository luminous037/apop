from django.db import models


class QuestionAnswer(models.Model):
    """Question과 Answer의 N:M관계 지원을 위한 모델 클래스
    """    
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
        """가질 수 있는 다음 순서를 반환

        Returns:
            int: 기본적으로 마지막 순서 번호 + 1
        """        
        return QuestionAnswer.objects.filter(question=self.question).count() + 1

    def exist_order(self) -> bool:
        """현재 QuestionAnswer의 순서 번호가 이미 존재하는지 확인

        Returns:
            bool: 존재하면 True, 존재하지 않으면 False
        """        
        return QuestionAnswer.objects.filter(question=self.question, order=self.order).exists()

    def swap_order(self, order: int):
        """두 QuestionAnswer의 순서 번호를 교환

        Args:
            order (int): 교환하고 싶은 번호
        """        
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
        """순서 번호 자동 설정을 위한 메서드
        """        
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