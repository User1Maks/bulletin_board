from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя."""

    username = None
    email = models.EmailField(unique=True, verbose_name='Email',
                              help_text='Укажите email')
    first_name = models.CharField(max_length=50, **NULLABLE,
                                  verbose_name='Имя',
                                  help_text='Введите имя')
    last_name = models.CharField(max_length=50, **NULLABLE,
                                 verbose_name='Фамилия',
                                 help_text='Введите фамилию')
    phone = models.CharField(max_length=25,
                             **NULLABLE,
                             verbose_name='Номер телефона',
                             help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/',
                               verbose_name='Аватар',
                               **NULLABLE,
                               help_text='Загрузите аватар профиля')
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin')
    ]

    role = models.CharField(max_length=5, choices=ROLE_CHOICES,
                            default='user', verbose_name='Роль пользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

