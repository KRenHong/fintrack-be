from django.db import models
from django.conf import settings
from categories.models import Category


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    month = models.DateField(help_text="Use first day of month, e.g. 2025-09-01")
    limit = models.DecimalField(max_digits=12, decimal_places=2)


    class Meta:
        unique_together = ("user", "category", "month")
        ordering = ["-month", "category__name"]


    def __str__(self):
        return f"{self.user_id}:{self.category.name}:{self.month}"
