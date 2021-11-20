from django.shortcuts import render

from . import models


def home(request):
    """
    Render homepage.
    """
    page_title = "Flexbudget"

    return render(request, "home.html", {"page_title": page_title})
