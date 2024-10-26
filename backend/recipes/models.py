from api.validators import validate_bad_username, validate_username

from backend.settings import (
    LONG_CHARFIELD,
    MID_CHARFIELD,
    NAME_LEGNTH,
    SHORT_CHARFIELD,
)

from colorfield.fields import ColorField

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


TEXT_SIZE = 15


class User(AbstractUser):
    username = models.CharField(
        blank=False,
        unique=True,
        max_length=20,
        validators=[validate_bad_username, validate_username],
    )

    fio = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fio']

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self) -> str:
        return self.username[:TEXT_SIZE]


class Tag(models.Model):
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    color = ColorField(
        verbose_name="цвет",
        unique=True,
        validators=[
            RegexValidator(
                r'^#[0-9a-fA-F]{6}$',
                'Введите цвет в формате RGB, в формате #000000',
            )
        ],
    )

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    author = models.ForeignKey(
        User, related_name='created_tasks', on_delete=models.CASCADE
    )
    doer = models.ForeignKey(
        User, related_name='assigned_tasks', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    text = models.TextField(verbose_name='описание')
    tag = models.ForeignKey(
        Tag, related_name='tasks', verbose_name='тэги', on_delete=models.CASCADE
    )
    deadline = models.DateField(verbose_name='сроки выполнения')
    pub_date = models.DateField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def __str__(self) -> str:
        return f'{self.name[:TEXT_SIZE]}, {self.author}'
