from django import forms
from django.core.exceptions import ValidationError

class HoneypotField(forms.CharField):
    """
    Simple honeypot field to help prevent spam bots.
    Rendered as hidden; any non-empty value triggers validation error.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", forms.HiddenInput)
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if value:
            raise ValidationError("Campo inválido.")
        return value


class RSVPForm(forms.Form):
    ATTENDING_CHOICES = (
        ("sim", "Sim"),
        ("nao", "Não"),
    )

    comparece = forms.ChoiceField(label="Comparece?", choices=ATTENDING_CHOICES)
    hp = HoneypotField()

__all__ = ["RSVPForm", "HoneypotField"]