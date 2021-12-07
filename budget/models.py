from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class IncomeFrequency(models.IntegerChoices):
    """
    Choices for frequency of income.
    """

    WEEKLY = 52, _("Weekly")
    BI_WEEKLY = 26, _("Bi-weekly")
    SEMI_MONTHLY = 24, _("Semi-monthly")
    MONTHLY = 12, _("Monthly")
    QUARTERLY = 4, _("Quarterly")
    SEMIANNUALLY = 2, _("Semi-annually")
    ANNUALLY = 1, _("Annually")


class BillingFrequency(models.IntegerChoices):
    """
    Choices for frequency of an expense.
    """

    MONTHLY = 1, _("Monthly")
    BI_MONTHLY = 2, _("Bi-monthly")
    QUARTERLY = 3, _("Quarterly")
    SEMIANNUALLY = 6, _("Semi-annually")
    ANNUALLY = 12, _("Annually")
    BI_ANNUALLY = 24, _("Bi-annually")


class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="income")
    name = models.CharField(max_length=100)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_paycheck = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_paycheck = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frequency = models.IntegerField(choices=IncomeFrequency.choices, default=IncomeFrequency.WEEKLY)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    per_paycheck_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frequency = models.IntegerField(choices=BillingFrequency.choices, default=BillingFrequency.MONTHLY)

    def __str__(self):
        return self.name

    def _set_cost_totals(self):
        annual_cost = (self.amount * 12) / self.frequency
        self.annual_cost = annual_cost
        self.per_paycheck_cost = annual_cost / self.user.budget.primary_income_frequency

    def save(self, *args, **kwargs):
        self._set_cost_totals()
        super().save(*args, **kwargs)


class Savings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="savings")
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_percent = models.BooleanField(default=True)
    per_paycheck_saving = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_saving = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def _set_saving_totals(self):
        self.annual_saving = self.user.budget.primary_income_frequency * self.amount
        self.per_paycheck_saving = self.amount

    def save(self, *args, **kwargs):
        self._set_saving_totals()
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserBudgetInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budget")
    primary_income_frequency = models.IntegerField(choices=IncomeFrequency.choices, default=IncomeFrequency.WEEKLY)
    total_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_gross_paycheck = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_net_paycheck = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_paycheck_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_annual_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_paycheck_savings = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_annual_savings = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"{self.user}'s budget"

    def update_budget(self):
        self._update_gross_salary()
        self._update_gross_paycheck()
        self._update_net_paycheck()
        self._update_paycheck_expenses()
        self._update_annual_expenses()
        self._update_paycheck_savings()
        self._update_annual_savings()
        self.save()

    def _update_gross_salary(self):
        self.total_gross_salary = self.user.income.aggregate(Sum("gross_salary"))["gross_salary__sum"] or 0

    def _update_gross_paycheck(self):
        self.total_gross_paycheck = self.user.income.aggregate(Sum("gross_paycheck"))["gross_paycheck__sum"] or 0

    def _update_net_paycheck(self):
        self.total_net_paycheck = self.user.income.aggregate(Sum("net_paycheck"))["net_paycheck__sum"] or 0

    def _update_paycheck_expenses(self):
        self.total_paycheck_expenses = (
            self.user.expenses.aggregate(Sum("per_paycheck_cost"))["per_paycheck_cost__sum"] or 0
        )

    def _update_annual_expenses(self):
        self.total_annual_expenses = self.user.expenses.aggregate(Sum("annual_cost"))["annual_cost__sum"] or 0

    def _update_paycheck_savings(self):
        self.total_paycheck_savings = (
            self.user.savings.aggregate(Sum("per_paycheck_saving"))["per_paycheck_saving__sum"] or 0
        )

    def _update_annual_savings(self):
        self.total_annual_savings = self.user.savings.aggregate(Sum("annual_saving"))["annual_saving__sum"] or 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
