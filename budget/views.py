from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_POST

from . import models
from . import forms


def home(request):
    page_title = "Flexbudget"
    income_form = forms.IncomeForm()

    user_income = models.Income.objects.filter(user=request.user)

    context = {
        "page_title": page_title,
        "income_form": income_form,
        "user_income": user_income,
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
