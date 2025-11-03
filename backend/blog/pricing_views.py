from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PricingPlan
from .serializers import PricingPlanSerializer


@api_view(['GET'])
def pricing_plans_api(request):
    """API endpoint for pricing plans"""
    plans = PricingPlan.objects.filter(is_active=True).order_by('order', 'price')
    serializer = PricingPlanSerializer(plans, many=True)
    
    return Response({
        'plans': serializer.data
    })