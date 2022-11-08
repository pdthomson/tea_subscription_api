from django.test import TestCase
from tea_subscription_api import *
from tea_subscription_api.models import Tea
from tea_subscription_api.models import Customer
from tea_subscription_api.models import Subscription

class TeaTestCase(TestCase):

  def test_tea_model(tea_object):
    tea = Tea.objects.create(title = 'Sleepy-time', description = 'makes you sweepy', temperature = 20, brew_time = 60)

    tea_object.assertEqual(str(tea.title), 'Sleepy-time')
    tea_object.assertEqual(str(tea.description), 'makes you sweepy')
    tea_object.assertEqual(int(tea.temperature), 20)
    tea_object.assertEqual(int(tea.brew_time), 60)

class CustomerTestCase(TestCase): 

  def test_customer_model(customer_object):
    customer = Customer.objects.create(first_name = 'Beannah', last_name = 'Durke', email = 'stompfrogsallday365@hotmail.com', address = '1234 downtown Bite me Blvd, Denver, CO 123456')

    customer_object.assertEqual(str(customer.first_name), 'Beannah')
    customer_object.assertEqual(str(customer.last_name), 'Durke')
    customer_object.assertEqual(str(customer.email), 'stompfrogsallday365@hotmail.com')
    customer_object.assertEqual(str(customer.address), '1234 downtown Bite me Blvd, Denver, CO 123456')

class SubscriptionTestCase(TestCase):
  
  def test_subscription_model(subscription_object):
    subscription = Subscription.objects.create(title = 'tea-mania', price = 22.5, status = 'active', frequency = 'monthly')

    subscription_object.assertEqual(str(subscription.title), 'tea-mania')
    subscription_object.assertEqual(float(subscription.price), 22.5)
    subscription_object.assertEqual(str(subscription.status), 'active')
    subscription_object.assertEqual(str(subscription.frequency), 'monthly')

