from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Frequency(models.IntegerChoices):
    """
    Choices for frequency of a transaction.
    """

    WEEKLY = 52, _("Weekly")
    BI_WEEKLY = 26, _("Bi-weekly")
    SEMI_MONTHLY = 24, _("Semi-monthly")
    MONTHLY = 12, _("Monthly")
    QUARTERLY = 4, _("Quarterly")
    SEMIANNUALLY = 2, _("Semi-annually")
    ANNUALLY = 1, _("Annually")


class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="income")
    name = models.CharField(max_length=100)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_paycheck = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_paycheck = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frequency = models.IntegerField(choices=Frequency.choices, default=Frequency.WEEKLY)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_frequency = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    per_paycheck_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frequency = models.IntegerField(choices=Frequency.choices, default=Frequency.WEEKLY)

    def __str__(self):
        return self.name

    def _set_monthly_frequency(self):
        if self.frequency >= 12:
            self.monthly_frequency = self.frequency / 12
        else:
            self.monthly_frequency = 12 / self.frequency

    def save(self, *args, **kwargs):
        self._set_monthly_frequency()
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


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserBudgetInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budget")
    primary_income_frequency = models.IntegerField(choices=Frequency.choices, default=Frequency.WEEKLY)
    total_gross_salary = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_gross_paycheck = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_net_paycheck = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_paycheck_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_annual_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_paycheck_savings = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    total_annual_savings = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"{self.user}'s budget"

    def update_gross_salary(self):
        self.total_gross_salary = self.user.income.aggregate(Sum("gross_salary"))["gross_salary__sum"] or 0
        self.save()

    def update_gross_paycheck(self):
        self.total_gross_paycheck = self.user.income.aggregate(Sum("gross_paycheck"))["gross_paycheck__sum"] or 0
        self.save()

    def update_net_paycheck(self):
        self.total_net_paycheck = self.user.income.aggregate(Sum("net_paycheck"))["net_paycheck__sum"] or 0
        self.save()

    def update_paycheck_expenses(self):
        print("update_paycheck_expenses")
        self.total_paycheck_expenses = (
            self.user.expenses.aggregate(Sum("per_paycheck_cost"))["per_paycheck_cost__sum"] or 0
        )
        the_expense = self.expenses.aggregate(Sum("per_paycheck_cost"))["per_paycheck_cost__sum"]
        print(the_expense)
        self.save()

    def update_annual_expenses(self):
        self.total_annual_expenses = self.user.expenses.aggregate(Sum("annual_cost"))["annual_cost__sum"] or 0
        self.save()

    def update_paycheck_savings(self):
        self.total_paycheck_savings = (
            self.user.savings.aggregate(Sum("per_paycheck_saving"))["per_paycheck_saving__sum"] or 0
        )
        self.save()

    def update_annual_savings(self):
        self.total_annual_savings = self.user.savings.aggregate(Sum("annual_saving"))["annual_saving__sum"] or 0
        self.save()
