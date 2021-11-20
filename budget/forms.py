from django import forms
from .models import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = (
            "name",
            "gross_salary",
            "gross_paycheck",
            "net_paycheck",
            "frequency",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
