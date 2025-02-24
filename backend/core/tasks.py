from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y


@shared_task
def hello_task(name):
    print(f"Hello {name}! You have {len(name)} characters in your name.")


@shared_task(name="core.tasks.send_order_confirmation_email")
def send_order_confirmation_email(order_id, user_email):
    subject = "Order Confirmation"
    message = f"Your order with ID {order_id} has been received and is being processed."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
