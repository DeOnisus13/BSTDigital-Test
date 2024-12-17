from django import forms
from django.core.exceptions import ValidationError
import re


class OrderForm(forms.Form):
    """
    Форма для ввода и валидации email и серийного номера.
    """
    email = forms.EmailField(label="Ваш email", max_length=50)
    robot_serial = forms.CharField(label="Серийный номер робота", max_length=5)

    def clean_robot_serial(self):
        robot_serial = self.cleaned_data["robot_serial"]
        pattern = r'^[A-Za-z0-9]{2}-[A-Za-z0-9]{2}$'
        if not re.match(pattern, robot_serial):
            raise ValidationError("Серийный номер должен быть в формате XX-YY, где X и Y - латинские буквы или цифры.")
        return robot_serial
