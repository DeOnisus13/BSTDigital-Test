from django import forms
from django.utils.timezone import now


class DateForm(forms.Form):
    """
    Форма для отображения и ввода даты.
    """
    date = forms.DateField(
        label="Дата отчета",
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=now().date
    )
