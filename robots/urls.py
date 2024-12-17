from django.urls import path

from robots.apps import RobotsConfig
from robots.views import RobotCreateView, RobotBulkCreateView, IndexView, ExcelReportView, export_to_excel

app_name = RobotsConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='main_page'),
    path('add_robot/', RobotCreateView.as_view(), name='add_robot'),
    path('add_robots/', RobotBulkCreateView.as_view(), name='add_robots'),
    path('get_report/', ExcelReportView.as_view(), name='get_report'),
    path('export_to_excel/', export_to_excel, name='export_to_excel'),
]
