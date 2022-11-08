from rest_framework import serializers
from .models import *

# An endpoint to subscribe a customer to a tea subscription
# An endpoint to cancel a customer's tea subscription
# An endpoint to see all of a customer's subscriptions(active and cancelled)

class SubscriptionSerializer(serializers.ModelSerializer):
  # customers = 'CustomerSerializer'
  class Meta: 
    model = Subscription
    fields = ['id', 'title', 'price', 'status', 'frequency', 'customers']

class CustomerSerializer(serializers.ModelSerializer):
  # subscriptions = SubscriptionSerializer(many=True)
  class Meta: 
    model = Customer 
    fields = ['id', 'first_name', 'last_name', 'email', 'address']

  # def create(self, validated_data):
  #   subscriptions_data = validated_data.pop('subscriptions')
  #   customer = Customer.objects.create(**validated_data)
  #   for subscription_data in subscriptions_data:
  #     Subscription.objects.create(customer = customer, **subscription_data)
