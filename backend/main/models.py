from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Расширенная модель пользователя
    
    display_name = models.CharField(
        'Отображаемое имя', max_length=100, default='Новый пользователь'
    )
    date_of_last_visit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Sprint(models.Model):
    # Модель Sprint представляет спринт
    title = models.CharField('Название', max_length=100, default='Спринт')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='sprints'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Спринт'
        verbose_name_plural = 'Спринты'

class Task(models.Model):
    # Модель Task представляет задачу

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]

    title = models.CharField('Название', max_length=100, default='Задача')
    text = models.TextField('Текст задачи')
    points = models.IntegerField('Баллы', default=0)
    date = models.DateTimeField('Дата', default=now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    sprint = models.ForeignKey(
        'Sprint', 
        on_delete=models.CASCADE, 
        verbose_name='Спринт',
        null=True,
        blank=True
    )
    priority = models.CharField(
        'Приоритет', 
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Родительская задача',
        null=True,
        blank=True,
        related_name='subtasks'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'