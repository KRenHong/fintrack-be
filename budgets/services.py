from datetime import date
from decimal import Decimal
from .models import Budget
from .selectors import spent_in_month


THRESHOLDS = {"warn": Decimal("0.80"), "breach": Decimal("1.00")}




def ensure_budget(*, user_id: int, category_id: int, month: date, limit: Decimal) -> Budget:
    obj, _ = Budget.objects.update_or_create(
    user_id=user_id, category_id=category_id, month=month.replace(day=1),
    defaults={"limit": limit},
    )
    return obj




def budget_status(*, user_id: int, category_id: int, month: date):
      b = Budget.objects.filter(user_id=user_id, category_id=category_id, month=month.replace(day=1)).first()
      if not b:
          return None
      spent = spent_in_month(user_id=user_id, category_id=category_id, month=b.month)
      ratio = (spent / b.limit) if b.limit else Decimal("0")
      state = "ok"
      if ratio >= THRESHOLDS["breach"]:
          state = "over"
      elif ratio >= THRESHOLDS["warn"]:
          state = "warn"
      return {"limit": b.limit, "spent": spent, "ratio": ratio, "state": state}