from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_list(request):
    """List user subscriptions"""
    return Response({
        'subscriptions': [],
        'message': 'Subscription system to be implemented'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_list(request):
    """List user invoices"""
    return Response({
        'invoices': [],
        'message': 'Invoice system to be implemented'
    })