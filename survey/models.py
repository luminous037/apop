from django.db import models


class Survey(models.Model):
    title = models.CharField(
        db_comment="survey title",
        null=False,
        blank=False,
        help_text="설문지 제목",
        max_length=40
    )
    description = models.TextField(
        db_comment="survey description",
        null=False,
        blank=False,
        help_text="설문지 설명",
        max_length=100
    )
    created_at = models.DateTimeField(
        db_comment="survey created time",
        auto_now_add=True,
        help_text="설문지 생성 시간"
    )
    updated_at = models.DateTimeField(
        db_comment="survey updated time",
        auto_now=True,
        help_text="설문지 수정 시간"
    )
    questions = models.ManyToManyField(
        to="Question",
        db_comment="survey questions",
        through="SurveyQuestion",
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "survey"
        verbose_name = "설문조사"
        verbose_name_plural = "설문조사"
        ordering = ["title", "created_at"]


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

    class Meta:
        db_table = "question"
        verbose_name = "질문"
        verbose_name_plural = "질문"
        ordering = ["create_at"]
