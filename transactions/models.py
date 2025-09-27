from django.db import models
from django.conf import settings


class Transaction(models.Model):
  IN, EX = "IN", "EX"
  KIND_CHOICES = [(IN, "Income"), (EX, "Expense")]


  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  kind = models.CharField(max_length=2, choices=KIND_CHOICES, default=EX)
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  occurred_on = models.DateField()
  note = models.CharField(max_length=255, blank=True)


class Meta:
  ordering = ["-occurred_on", "-id"]
  indexes = [models.Index(fields=["user", "occurred_on"]) ]