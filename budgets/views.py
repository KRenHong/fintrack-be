from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from .models import Budget
from .serializers import BudgetSerializer
from .services import budget_status


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


    @action(detail=False, methods=["get"], url_path="progress")
    def progress(self, request):
        """GET /api/budgets/progress/?category=<id>&month=YYYY-MM-01"""
        category_id = int(request.query_params.get("category"))
        month_str = request.query_params.get("month")
        m = date.fromisoformat(month_str) if month_str else date.today().replace(day=1)
        data = budget_status(user_id=request.user.id, category_id=category_id, month=m)
        return Response(data)