from django.contrib import admin
from .models import Income, Expenses, Savings, Category


class IncomeAdmin(admin.ModelAdmin):
    model = Income


class ExpensesAdmin(admin.ModelAdmin):
    model = Expenses


class SavingsAdmin(admin.ModelAdmin):
    model = Savings


class CategoryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(Income, IncomeAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(Savings, SavingsAdmin)
admin.site.register(Category, CategoryAdmin)
