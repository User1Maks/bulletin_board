from smtplib import SMTPException

from celery import shared_task
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from config import settings


@shared_task
def send_reset_password_email(email, reset_link):
    try:
        send_mail(
            'Сброс пароля',
            f'Перейдите по ссылке для сброса пароля:'
            f' {reset_link}. Если Вы не запрашивали сброс пароля '
            f'проигнорируйте данное сообщение.',
            settings.EMAIL_HOST_USER,
            [email],
            #  Позволяет видеть и обрабатывать ошибки при отправке письма
            fail_silently=False,
        )
    except SMTPException as e:
        return Response(
            {'error': f'Ошибка при отправке письма:: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except ValueError:
        return Response(
            {'error': 'Некорректный email или данные для отправки.'},
            status=status.HTTP_400_BAD_REQUEST
        )
