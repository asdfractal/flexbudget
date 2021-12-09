from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/<model_to_update>/", views.create_budget_record, name="create_budget_record"),
    path("delete/income/<int:pk>", views.delete_budget_record, name="delete_income"),
    path("delete/expenses/<int:pk>", views.delete_budget_record, name="delete_expenses"),
    path("delete/savings/<int:pk>", views.delete_budget_record, name="delete_savings"),
]
