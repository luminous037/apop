from django.db import models
from django.conf import settings

default_sny_date = "1970-01-01"

class HuamiAccount(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        db_comment="user id",
        null=False,
        blank=False,
        help_text="유저 id",
        related_name="huami",
    )
    email = models.EmailField(
        db_column="email",
        db_comment="huami account email address",
        null=False,
        blank=False,
        help_text="화웨이 계정 이메일"
    )
    password = models.CharField(
        db_column="password",
        db_comment="huami account password address",
        max_length=100,
        null=False,
        blank=False,
        help_text="화웨이 계정 패스워드"
    )
    sync_date = models.DateTimeField(
        db_column="sync_date",
        db_comment="huami account sync date",
        null=False,
        blank=False,
        help_text="화웨이 계정 동기화 날짜",
        default=default_sny_date,
    )

    def __str__(self):
        return self.email

    class Meta:
        db_table = "huami_account"
        verbose_name = "화웨이 계정"
        verbose_name_plural = "화웨이 계정"
        ordering = ["email", "sync_date"]

    def reset_sync_date(self):
        self.sync_date = default_sny_date
        self.save()


# Create your models here.
