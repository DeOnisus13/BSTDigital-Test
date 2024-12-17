import logging

from django.http import JsonResponse
from django.views.generic import FormView

from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order
from robots.models import Robot

logger = logging.getLogger(__name__)


class OrderView(FormView):
    """
    Представление для заказа робота.
    При вводе email и серийного номера создается Customer и Order.
    Если робота с таким серийным номером нет в БД, то заказ помечается как отложенный.
    """
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        robot_serial = form.cleaned_data["robot_serial"].upper()

        # Находим или создаем пользователя
        customer, created = Customer.objects.get_or_create(email=email)

        # Проверяем наличие робота в БД
        robot = Robot.objects.filter(serial=robot_serial).first()
        is_pending = False
        if not robot:
            is_pending = True

        # Создаем заказ
        Order.objects.create(customer=customer, robot_serial=robot_serial, is_pending=is_pending)

        if is_pending:
            logger.info(f"Заказ пользователя {customer.id} на робота {robot_serial} добавлен в список ожидания.")
            return JsonResponse({"error": "Робота с таким серийным номером нет в базе. Ваш заказ добавлен в очередь."},
                                status=400)

        return JsonResponse({"success": f"Робот с номером {robot_serial} успешно заказан."})

    def form_invalid(self, form):
        return JsonResponse({"error": form.errors}, status=400)
