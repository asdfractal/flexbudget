from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Income, Expenses, Savings, UserBudgetInfo
from . import forms


def home(request):
    page_title = "Flexbudget"
    income_form = forms.IncomeForm()
    expense_form = forms.ExpenseForm()
    savings_form = forms.SavingsForm()

    if request.user.is_authenticated:
        user_income = Income.objects.filter(user=request.user)
        user_expenses = Expenses.objects.filter(user=request.user)
        user_savings = Savings.objects.filter(user=request.user)
        user_budget = UserBudgetInfo.objects.get(user=request.user)

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
def create_budget_record(request, model_to_update):
    form_collection = {
        "income": forms.IncomeForm,
        "expenses": forms.ExpenseForm,
        "savings": forms.SavingsForm,
    }
    table_collection = {
        "income": "components/updates/create_income.html",
        "expenses": "components/updates/create_expenses.html",
        "savings": "components/updates/create_savings.html",
    }
    form = form_collection[model_to_update]
    component = table_collection[model_to_update]
    populated_form = form(request.POST)
    if populated_form.is_valid():
        updated_data = populated_form.save(commit=False)
        updated_data.user = request.user
        updated_data.save()
        updated_budget = UserBudgetInfo.objects.get(user=request.user)
        context = {
            "updated_data": updated_data,
            "updated_budget": updated_budget,
        }
        return render(
            request,
            component,
            context,
        )
        # return redirect(reverse("home"))
    print(form.errors)
    return redirect(reverse("home"))


def delete_budget_record(request, pk):
    url = request.get_full_path()
    url_parts = url.split("/")
    model_type = ContentType.objects.get(model=url_parts[2])
    model_class = apps.get_model(model_type.app_label, model_type.model)
    model_instance = get_object_or_404(model_class, pk=pk)
    model_instance.delete()
    print("deleted")
    return redirect(reverse("home"))
