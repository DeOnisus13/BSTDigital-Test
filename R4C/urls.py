from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("robots.urls", namespace="robots")),
    path('', include("orders.urls", namespace="orders")),
]
