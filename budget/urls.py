from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("update/<model_to_update>/", views.update_budget, name="update_budget"),
    path("delete/income/<int:pk>", views.delete_income, name="delete_income"),
]
