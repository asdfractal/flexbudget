from django.shortcuts import render
from django.views.decorators.http import require_POST

from . import models
from . import forms


def home(request):
    page_title = "Flexbudget"
    income_form = forms.IncomeForm()

    context = {
        "page_title": page_title,
        "income_form": income_form,
    }

    print(income_form)

    return render(request, "home.html", context)
