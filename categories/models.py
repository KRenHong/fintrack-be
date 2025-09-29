from django.db import models
from django.conf import settings


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=7, default="#64748b")  # e.g., #64748b


class Meta:
    unique_together = ("user", "name")
    ordering = ["name"]


def __str__(self):
    return self.name
