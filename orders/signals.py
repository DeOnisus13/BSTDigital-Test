import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from R4C.settings import EMAIL_HOST_USER
from orders.models import Order
from robots.models import Robot

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Robot)
def notify_pending_orders(sender, instance, created, **kwargs):
    """Сигнал для отправки email пользователям, заказ которых находится в ожидании."""
    if created:
        # Находим все заказы в ожидании с нужным серийным номером
        pending_orders = Order.objects.filter(robot_serial=instance.serial, is_pending=True)

        for order in pending_orders:
            send_mail(
                subject="Робот теперь в наличии",
                message=f"Добрый день!\n"
                        f"Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n"
                        f"Этот робот теперь есть в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.",
                from_email=EMAIL_HOST_USER,
                recipient_list=[order.customer.email],
                fail_silently=False,
            )
            order.is_pending = False
            order.save()

            logger.info(f"Пользователю {order.customer.id} из заказа {order.id} отправлено письмо о поступлении робота.")
