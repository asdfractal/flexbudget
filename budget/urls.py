from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("update_income/", views.update_income, name="update_income"),
]
