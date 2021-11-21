from django import forms
from .models import Income, Expenses, Savings


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


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = (
            "name",
            "category",
            "amount",
            "frequency",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = (
            "name",
            "amount",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
