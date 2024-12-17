import json
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView
from django.core.exceptions import ValidationError
from robots.models import Robot


class IndexView(TemplateView):
    """
    Отображение главной страницы.
    """
    template_name = "robots/index.html"


class RobotCreateView(CreateView):
    """
    Отображение страницы для создания одного объекта класса Robot через форму.
    """
    model = Robot
    fields = ['model', 'version', 'created']
    template_name = "robots/add_robot_form.html"

    def form_invalid(self, form):
        """Возвращает ошибки валидации в формате JSON."""
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def form_valid(self, form):
        """Сохраняет форму и возвращает успешный ответ."""
        robot = form.save(commit=False)
        robot.serial = f"{robot.model}-{robot.version}"
        robot.save()
        return JsonResponse({"success": True, "robot_id": robot.id})


class RobotBulkCreateView(CreateView):
    """
    Отображение страницы для создания одного или нескольких объектов класса Robot через ввод данных в формате JSON.
    """
    model = Robot
    fields = ['model', 'version', 'created']
    template_name = "robots/add_robots_json_form.html"

    def post(self, request, *args, **kwargs):
        try:
            # Получаем JSON-данные из текстового поля
            data = json.loads(request.POST.get("robots_json", "[]"))

            # Если данные — один объект, оборачиваем в массив
            if isinstance(data, dict):  # Один объект
                data = [data]

            robots_to_create = []
            errors = []

            for item in data:
                try:
                    robot = Robot(
                        model=item.get("model").upper(),
                        version=item.get("version").upper(),
                        created=item.get("created")
                    )
                    robot.serial = f"{robot.model}-{robot.version}"
                    robot.full_clean()  # Валидация данных
                    robots_to_create.append(robot)
                except ValidationError as e:
                    errors.append({"data": item, "errors": e.message_dict})

            # Сохраняем валидные объекты
            if robots_to_create:
                Robot.objects.bulk_create(robots_to_create)

            return JsonResponse({
                "success": len(robots_to_create),
                "errors": errors,
            })
        except json.JSONDecodeError as err:
            return JsonResponse({"error": f"Invalid JSON format: {str(err)}"}, status=400)
