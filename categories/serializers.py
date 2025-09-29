from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ["id", "name", "color"]


def create(self, validated_data):
  user = self.context["request"].user
  return Category.objects.create(user=user, **validated_data)