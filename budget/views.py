from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from . import models
from . import forms


def home(request):
    page_title = "Flexbudget"
    income_form = forms.IncomeForm()
    expense_form = forms.ExpenseForm()
    savings_form = forms.SavingsForm()

    if request.user.is_authenticated:
        user_income = models.Income.objects.filter(user=request.user)
        user_expenses = models.Expenses.objects.filter(user=request.user)
        user_savings = models.Savings.objects.filter(user=request.user)
        user_budget = models.UserBudgetInfo.objects.get(user=request.user)

        context = {
            "page_title": page_title,
            "income_form": income_form,
            "expense_form": expense_form,
            "savings_form": savings_form,
            "user_income": user_income,
            "user_expenses": user_expenses,
            "user_savings": user_savings,
            "user_budget": user_budget,
        }

        return render(request, "home.html", context)
    return render(request, "home.html")


@require_POST
def update_budget(request, model_to_update):
    form_collection = {
        "income": forms.IncomeForm,
        "expense": forms.ExpenseForm,
        "savings": forms.SavingsForm,
    }
    form = form_collection[model_to_update]
    populated_form = form(request.POST)
    if populated_form.is_valid():
        updated_data = populated_form.save(commit=False)
        updated_data.user = request.user
        updated_data.save()
        print(updated_data)
        return redirect(reverse("home"))
    print(form.errors)
    return redirect(reverse("home"))
