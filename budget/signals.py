from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Income


@receiver(post_save, sender=Income)
def update_on_save(sender, instance, **kwargs):
    instance.user.update_net_paycheck()


@receiver(post_delete, sender=Income)
def update_on_delete(sender, instance, **kwargs):
    instance.user.update_net_paycheck()
