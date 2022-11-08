from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
import json 
from django.http import JsonResponse 
from django.http import HttpResponse  
from django.http import HttpRequest
from rest_framework import generics
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view

@api_view(["GET"])

def ApiOverview(request):
  api_urls = {
    'See ALL Customer Subscriptions': 'customers/<int:customer_id>/subscriptions/',
    'Update Subscription': 'customers/<int:customer_id>/subscriptions/<int:subscription_id>/',
    'Enroll a customer to a Subscription': 'customers/<int:customer_id>/subscriptions/'
  }

  return Response(api_urls)

@api_view(["PATCH"])# An endpoint to cancel a customer’s tea subscription

def update_subscription(request, **kwargs):
  subscription = Subscription.objects.get(customers=kwargs['customer_id'], id=kwargs['subscription_id'])
  serializer = SubscriptionSerializer(subscription, request.data, partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  else:
    return Response(status=status.HTTP_404_NOT_FOUND) 

@api_view(["POST"])# An endpoint to subscribe a customer to a tea subscription

def subscribe_a_customer(request, **kwargs):
  customer = Customer.objects.filter(id=kwargs['customer_id'])[0]#this gets rid of an instantiante error
  subscription_data=request.data

  subscription = Subscription(
    id = subscription_data['id'],
    title = subscription_data['title'],
    price = subscription_data['price'],
    status = subscription_data['status'],
    frequency = subscription_data['frequency'],
    customers = customer
  )
  subscription.save()

  return Response({
    'id': subscription.id,
    'title': subscription.title,
    'price': subscription.price,
    'status': subscription.status,
    'frequency': subscription.frequency
  }, status=201)

@api_view(["GET"])# An endpoint to see all of a customer’s subsciptions (active and cancelled)

def customer_subscriptions(request, **kwargs):
    subscriptions = Subscription.objects.filter(customers=kwargs['customer_id'])
    serializer = SubscriptionSerializer(subscriptions, many=True)

    return Response(serializer.data)

