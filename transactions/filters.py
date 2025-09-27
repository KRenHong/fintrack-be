import django_filters as df
from .models import Transaction


class TransactionFilter(df.FilterSet):
  min_date = df.DateFilter(field_name="occurred_on", lookup_expr="gte")
  max_date = df.DateFilter(field_name="occurred_on", lookup_expr="lte")
  kind = df.CharFilter(field_name="kind")


  class Meta:
    model = Transaction
    fields = ["min_date", "max_date", "kind"]