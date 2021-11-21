from django.conf import settings
from django.db import models
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    gross_paycheck = models.DecimalField(max_digits=10, decimal_places=2)
    net_paycheck = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.IntegerField(choices=Frequency.choices, default=Frequency.WEEKLY)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.IntegerField(choices=Frequency.choices, default=Frequency.WEEKLY)
    monthly_frequency = models.IntegerField(default=0)
    per_paycheck_cost = models.IntegerField(default=0)
    annual_cost = models.IntegerField(default=0)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_percent = models.BooleanField(default=True)
    per_paycheck_saving = models.IntegerField(default=0)
    annual_saving = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
