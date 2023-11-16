from django.db import models


class Question(models.Model):
    title = models.CharField(
        db_column="title",
        db_comment="question title",
        null=False,
        blank=False,
        help_text="질문 제목",
        max_length=40
    )
    description = models.TextField(
        db_column="description",
        db_comment="question description",
        null=True,
        blank=False,
        help_text="질문 설명",
        max_length=100
    )
    create_at = models.DateTimeField(
        db_column="create_at",
        db_comment="question created time",
        auto_now_add=True,
        help_text="질문 생성 시간"
    )
    updated_at = models.DateTimeField(
        db_column="updated_at",
        db_comment="question updated time",
        auto_now=True,
        help_text="질문 수정 시간"
    )
    answers = models.ManyToManyField(
        to="Answer",
        through="QuestionAnswer",
    )

    class Meta:
        db_table = "question"
        verbose_name = "질문"
        verbose_name_plural = "질문"
        ordering = ["create_at"]
