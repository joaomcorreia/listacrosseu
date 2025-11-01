from rest_framework.generics import ListAPIView
from .models import Plan
from .serializers import PlanSerializer


class PlanList(ListAPIView):
    queryset = Plan.objects.filter(is_active=True).order_by("priority_weight")
    serializer_class = PlanSerializer
