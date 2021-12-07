from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Income, Expenses, Savings, UserBudgetInfo

CURRENT_USER = get_user_model()


@receiver(post_save, sender=Income)
def update_budget_on_save_income(sender, instance, **kwargs):
    instance.user.budget.update_budget()


@receiver(post_save, sender=Expenses)
def update_budget_on_save_expenses(sender, instance, **kwargs):
    instance.user.budget.update_budget()


@receiver(post_save, sender=Savings)
def update_budget_on_save_savings(sender, instance, **kwargs):
    instance.user.budget.update_budget()


@receiver(post_save, sender=CURRENT_USER)
def create_or_update_user_budget(sender, instance, created, **kwargs):
    """
    Create or update the user budget.
    """
    if created:
        UserBudgetInfo.objects.create(user=instance)
    # If user exists, save budget
    instance.budget.save()
