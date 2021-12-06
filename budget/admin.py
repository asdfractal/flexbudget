from django.contrib import admin
from .models import Income, Expenses, Savings, Category, UserBudgetInfo


class IncomeAdmin(admin.ModelAdmin):
    model = Income


class ExpensesAdmin(admin.ModelAdmin):
    model = Expenses


class SavingsAdmin(admin.ModelAdmin):
    model = Savings


class CategoryAdmin(admin.ModelAdmin):
    model = Category


class UserBudgetInfoAdmin(admin.ModelAdmin):
    model = UserBudgetInfo


admin.site.register(Income, IncomeAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(Savings, SavingsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserBudgetInfo, UserBudgetInfoAdmin)
