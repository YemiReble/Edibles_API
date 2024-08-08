from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription, SubscriptionPlan
from .serializers import SubscriptionSerializer

class ListSubscriptionsView(APIView):
    def get(self, request):
        # Get user subscriptions (assuming user is authenticated)
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

class SubscribeView(APIView):
    def post(self, request):
        # Get data from request
        plan_id = request.data.get('plan_id')

        # Validate data and check if plan exists
        try:
            plan = SubscriptionPlan.objects.get(pk=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Invalid plan ID'}, status=400)

        # Check if user already has an active subscription
        user = request.user
        if Subscription.objects.filter(user=user, # ... check for active status):
            return Response({'error': 'User already has an active subscription'}, status=400)

        # Create and save new subscription
        subscription = Subscription.objects.create(user=user, plan=plan)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=201)

