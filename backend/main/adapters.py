from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import send_mail
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Отправляем письмо в случае успешной регистрации
        user = emailconfirmation.email_address.user
        subject = 'Добро пожаловать в Agile Task Planning App!'
        message = f'Здравствуйте, {user.username}!\n\nРегистрация прошла успешно.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [emailconfirmation.email_address.email]
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False
        )

    def confirm_email(self, request, email_address):
        # Отключаем стандартное подтверждение по ссылке
        pass