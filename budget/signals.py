from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Income, Expenses, Savings


@receiver(post_save, sender=Income)
def update_on_save_income(sender, instance, **kwargs):
    print("income saved")
    instance.user.update_gross_salary()
    instance.user.update_gross_paycheck()
    instance.user.update_net_paycheck()


@receiver(post_delete, sender=Income)
def update_on_delete_income(sender, instance, **kwargs):
    instance.user.update_gross_salary()
    instance.user.update_gross_paycheck()
    instance.user.update_net_paycheck()


@receiver(post_save, sender=Expenses)
def update_on_save_expenses(sender, instance, **kwargs):
    print("expense saved")
    instance.user.update_paycheck_expenses()
    instance.user.update_annual_expenses()


@receiver(post_delete, sender=Expenses)
def update_on_delete_expenses(sender, instance, **kwargs):
    instance.user.update_paycheck_expenses()
    instance.user.update_annual_expenses()


@receiver(post_save, sender=Savings)
def update_on_save_savings(sender, instance, **kwargs):
    instance.user.update_paycheck_savings()
    instance.user.update_annual_savings()


@receiver(post_delete, sender=Savings)
def update_on_delete_savings(sender, instance, **kwargs):
    instance.user.update_paycheck_savings()
    instance.user.update_annual_savings()
