from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Robot(models.Model):
    """
    Модель для роботов.
    """
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False, validators=[
        RegexValidator(regex=r'^[A-Za-z0-9]{2}$',
                       message="Поле 'model' должно иметь от 1 до 2 латинских символов или чисел.")])
    version = models.CharField(max_length=2, blank=False, null=False, validators=[
        RegexValidator(regex=r'^[A-Za-z0-9]{2}$',
                       message="Поле 'version' должно иметь от 1 до 2 латинских символов или чисел.")])
    created = models.DateTimeField(default=timezone.now, blank=False, null=False)

    def save(self, *args, **kwargs):
        """Переопределение метода save для перевода входных данных в верхний регистр."""
        self.model = self.model.upper()
        self.version = self.version.upper()
        self.serial = self.serial.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Модель: {self.model}. Версия: {self.version}."

    class Meta:
        verbose_name = "Робот"
        verbose_name_plural = "Роботы"
