from django.urls import path

from robots.apps import RobotsConfig
from robots.views import RobotCreateView, RobotBulkCreateView, IndexView

app_name = RobotsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='main_page'),
    path('add_robot/', RobotCreateView.as_view(), name='add_robot'),
    path('add_robots/', RobotBulkCreateView.as_view(), name='add_robots'),
]
