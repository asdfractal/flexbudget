from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from . import models
from . import forms


def home(request):
    page_title = "Flexbudget"
    income_form = forms.IncomeForm()
    expense_form = forms.ExpenseForm()

    user_income = models.Income.objects.filter(user=request.user)
    user_expenses = models.Expenses.objects.filter(user=request.user)

    context = {
        "page_title": page_title,
        "income_form": income_form,
        "expense_form": expense_form,
        "user_income": user_income,
        "user_expenses": user_expenses,
    }

    return render(request, "home.html", context)


@require_POST
def update_income(request):
    form = forms.IncomeForm(request.POST)
    if form.is_valid():
        income = form.save(commit=False)
        income.user = request.user
        income.save()
        return redirect(reverse("home"))


@require_POST
def update_expense(request):
    form = forms.ExpenseForm(request.POST)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect(reverse("home"))
    print(form.errors)
    return redirect(reverse("home"))
