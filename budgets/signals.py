import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from transactions.models import Transaction
from .services import budget_status


log = logging.getLogger(__name__)


@receiver(post_save, sender=Transaction)
def check_budget_after_txn(sender, instance: Transaction, created, **kwargs):
    if instance.kind != "EX" or not instance.category_id:
        return
    m = instance.occurred_on.replace(day=1)
    status = budget_status(user_id=instance.user_id, category_id=instance.category_id, month=m)
    if not status:
        return
    if status["state"] == "over":
        log.warning("Budget BREACHED: user=%s cat=%s month=%s spent=%s limit=%s", instance.user_id, instance.category_id, m, status["spent"], status["limit"])
    elif status["state"] == "warn":
        log.info("Budget WARNING 80%%: user=%s cat=%s month=%s spent=%s limit=%s", instance.user_id, instance.category_id, m, status["spent"], status["limit"])