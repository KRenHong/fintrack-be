from datetime import date
from decimal import Decimal
from django.db.models import Sum
from transactions.models import Transaction



def next_month(d: date) -> date:
    return (d.replace(day=28) + __import__("datetime").timedelta(days=4)).replace(day=1)



def spent_in_month(*, user_id: int, category_id: int, month: date) -> Decimal:
    start = month.replace(day=1)
    end = next_month(start)
    agg = (Transaction.objects
    .filter(user_id=user_id, category_id=category_id, kind="EX",
    occurred_on__gte=start, occurred_on__lt=end)
    .aggregate(total=Sum("amount")))
    return agg["total"] or Decimal("0")