import os

from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.models import User


@receiver(post_save, sender=User, dispatch_uid="send_welcom_email")
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Welcome!",
            "Thanks for signing up!",
            "admin@django.com",
            [instance.email],
            fail_silently=False,
        )


@receiver(post_delete, sender=User, dispatch_uid="delete_associated_file")
def delete_associated_file(sender, instance, **kwargs):
    if instance.cv:
        if os.path.isfile(instance.cv.path):
            os.remove(instance.cv.path)
