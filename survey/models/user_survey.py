from django.db import models
from django.conf import settings


class UserSurvey(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='user_id',
        db_comment='user id',
        null=False,
        blank=False,
        help_text='유저 id'
    )
    survey = models.ForeignKey(
        to='Survey',
        on_delete=models.CASCADE,
        db_column='survey_id',
        db_comment='survey id',
        null=False,
        blank=False,
        help_text='설문 id'
    )
    create_at = models.DateTimeField(
        db_column='create_at',
        db_comment='user survey created time',
        auto_now_add=True,
        help_text='유저 설문 생성 시간'
    )
    updated_at = models.DateTimeField(
        db_column='updated_at',
        db_comment='user survey updated time',
        auto_now=True,
        help_text='유저 설문 수정 시간'
    )

    class Meta:
        db_table = 'user_survey'
        verbose_name = '유저 설문'
        verbose_name_plural = '유저 설문'
        ordering = ['create_at']