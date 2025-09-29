from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "category", "month", "limit"]


    def create(self, validated_data):
        user = self.context["request"].user
        return Budget.objects.create(user=user, **validated_data)