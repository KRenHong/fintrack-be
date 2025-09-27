from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.http import HttpResponse
import csv
from .models import Transaction
from .serializers import TransactionSerializer
from .filters import TransactionFilter


class TransactionViewSet(viewsets.ModelViewSet):
  serializer_class = TransactionSerializer
  filterset_class = TransactionFilter
  permission_classes = [permissions.IsAuthenticated]


  def get_queryset(self):
    return Transaction.objects.filter(user=self.request.user)


  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


  @action(detail=False, methods=["get"]) # /api/transactions/export/
  def export(self, request):
      response = HttpResponse(content_type="text/csv")
      response["Content-Disposition"] = "attachment; filename=transactions.csv"
      writer = csv.writer(response)
      writer.writerow(["Date", "Kind", "Amount", "Note"])
      for t in self.get_queryset():
        writer.writerow([t.occurred_on, t.kind, t.amount, t.note])
      return response