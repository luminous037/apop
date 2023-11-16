from django.db import models


class Survey(models.Model):
    title = models.CharField(
        db_column="title",
        db_comment="survey title",
        null=False,
        blank=False,
        help_text="설문지 제목",
        max_length=40
    )
    description = models.TextField(
        db_column="description",
        db_comment="survey description",
        null=False,
        blank=False,
        help_text="설문지 설명",
        max_length=100
    )
    created_at = models.DateTimeField(
        db_column="created_at",
        db_comment="survey created time",
        auto_now_add=True,
        help_text="설문지 생성 시간"
    )
    updated_at = models.DateTimeField(
        db_column="updated_at",
        db_comment="survey updated time",
        auto_now=True,
        help_text="설문지 수정 시간"
    )
    questions = models.ManyToManyField(
        to="Question",
        through="SurveyQuestion",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "survey"
        verbose_name = "설문조사"
        verbose_name_plural = "설문조사"
        ordering = ["title", "created_at"]