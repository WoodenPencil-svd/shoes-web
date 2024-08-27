# orders/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem

@receiver(post_save, sender=Order)
def send_order_receipt(sender, instance, created, **kwargs):
    if created:
        # Subject và message của email
        subject = f"Order #{instance.id} Confirmation"
        message = f"Thank you for your order, {instance.user.username}!\n\n"
        message += "You have placed your order successfully!\n"
        message += "We hope to see you again soon!"

        # Danh sách người nhận
        recipient_list = [instance.user.email]

        # Gửi email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
