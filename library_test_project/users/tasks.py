from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def send_mail_task(subject, message, email):
    print(message)
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
