from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
        help_text="질문 순서",
        validators=[MinValueValidator(1)],
    )
    
    def __str__(self):
        return self.question.title

    class Meta:
        db_table = "survey_question"
        verbose_name = "설문조사 질문"
        verbose_name_plural = "설문조사 질문"
        ordering = ["survey", "order"]

    @property
    def next_order(self) -> int:
        return SurveyQuestion.objects.filter(survey=self.survey).count() + 1

    def exist_order(self) -> bool:
        return SurveyQuestion.objects.filter(survey=self.survey, order=self.order).exists()

    def swap_order(self, order: int):
        if order == self.order:
            return
        survey_question = SurveyQuestion.objects.get(
            survey=self.survey,
            order=order
        )
        survey_question.order, self.order = self.order, survey_question.order
        survey_question.save()
        self.save()

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = self.next_order
        if self.exist_order():
            SurveyQuestion.objects.filter(
                survey=self.survey,
                order=self.order
            ).update(
                order=self.next_order
            )

        super().save(*args, **kwargs)