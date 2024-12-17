from django.urls import path

from orders.apps import OrdersConfig
from orders.views import OrderView

app_name = OrdersConfig.name

urlpatterns = [
    path('order/', OrderView.as_view(), name='order'),
]
