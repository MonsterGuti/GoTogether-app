from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def create_notification_and_send_email(recipient, message):
    notification = Notification.objects.create(
        recipient=recipient,
        message=message
    )

    if recipient.email:
        send_mail(
            subject='Ново известие в TakeTheTrip',
            message=f'Здравейте, {recipient.first_name or recipient.username}!\n\n'
                    f'{message}\n\n'
                    f'Влезте в сайта, за да прегледате детайлите.\n\n'
                    f'Поздрави,\nЕкипът на TakeTheTrip',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=True,
        )

    return notification