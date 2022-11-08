import unittest
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status
from django.test import TestCase
from tea_subscription_api import *
from tea_subscription_api.models import *
from tea_subscription_api.serializers import SubscriptionSerializer
from tea_subscription_api.serializers import CustomerSerializer


class BaseTest(APITestCase):
  client = APIClient()

class CustomerSerializerTestCase(BaseTest):# using @unittest.skip('reason') will skip tests but had to import unittest at the top of class    
  def test_customer_serializer_has_correct_keys(self):
    customer_att = {
      'id': 1,
      'first_name': 'pachary',
      'last_name': 'zrince',
      'email': 'Ilovelittlekatanas@hotkatana.com',
      'address': 'katana ln, maldorf, Waryland'
    }

    customer = Customer.objects.create(**customer_att)
    serialized_customer = CustomerSerializer(instance = customer)
    data = serialized_customer.data

    self.assertEqual(set(data.keys()), set(['id', 'first_name', 'last_name', 'email', 'address']))

  def test_see_customer_subscriptions_by_customer_id(self):
    customer = Customer(
      id = 2,
      first_name = 'Hai',
      last_name = 'Sall',
      email = 'sailt&peppa@saimall.com',
      address = 'this place Seattle, WA'
    )
    customer.save()

    subscription = Subscription(
      id = 1,
      title = 'Tea Partay',
      price = 50.99,
      status = 'active',
      frequency = 'monthly',
      customers = customer
    )

    subscription.save()

    subscription2 = Subscription(
      id = 2,
      title = 'Tea Time Partay',
      price = 50.99,
      status = 'active',
      frequency = 'bi-weekly',
      customers = customer
    )

    subscription2.save()

    response = self.client.get(f'/api/v1/customers/{customer.id}/subscriptions/', format = 'json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 2)
    self.assertEqual(response.data[0]['id'], subscription.id)
    self.assertEqual(response.data[0]['title'], subscription.title)
    self.assertEqual(response.data[0]['price'], subscription.price)
    self.assertEqual(response.data[0]['status'], subscription.status)
    self.assertEqual(response.data[0]['frequency'], subscription.frequency)
    self.assertEqual(response.data[1]['id'], subscription2.id)
    self.assertEqual(response.data[1]['title'], subscription2.title)
    self.assertEqual(response.data[1]['price'], subscription2.price)
    self.assertEqual(response.data[1]['status'], subscription2.status)
    self.assertEqual(response.data[1]['frequency'], subscription2.frequency)


  def test_greeting_page(self): 
    response = self.client.get(f'/api/v1/')

    self.assertEqual(response.status_code, 200)
    self.assertNotEqual(response.status_code, 404)

  def test_only_returns_correct_customer_subscription(self):
    customer = Customer(
      id = 2,
      first_name = 'Hai',
      last_name = 'Sall',
      email = 'sailt&peppa@saimall.com',
      address = 'this place Seattle, WA'
    )
    customer.save()

    subscription = Subscription(
      id = 1,
      title = 'Tea Partay',
      price = 50.99,
      status = 'active',
      frequency = 'monthly',
      customers = customer
    )

    subscription.save()

    subscription2 = Subscription(
      id = 2,
      title = 'Tea Time Partay',
      price = 24.97,
      status = 'cancelled',
      frequency = 'bi-weekly'
    )

    subscription2.save()

    response = self.client.get(f'/api/v1/customers/{customer.id}/subscriptions/', format = 'json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['id'], subscription.id)
    self.assertEqual(response.data[0]['title'], subscription.title)
    self.assertEqual(response.data[0]['price'], subscription.price)
    self.assertEqual(response.data[0]['status'], subscription.status)
    self.assertEqual(response.data[0]['frequency'], subscription.frequency)
    self.assertNotEqual(response.data[0]['id'], subscription2.id)
    self.assertNotEqual(response.data[0]['title'], subscription2.title)
    self.assertNotEqual(response.data[0]['price'], subscription2.price)
    self.assertNotEqual(response.data[0]['status'], subscription2.status)
    self.assertNotEqual(response.data[0]['frequency'], subscription2.frequency)

  def test_patch_request_update_customer_suscription(self):
    customer = Customer(
      id = 2,
      first_name = 'Hai',
      last_name = 'Sall',
      email = 'sailt&peppa@saimall.com',
      address = 'this place Seattle, WA'
    )
    customer.save()

    subscription = Subscription(
      id = 1,
      title = 'Tea Partay',
      price = 50.99,
      status = "active",
      frequency = 'monthly',
      customers = customer
    )

    subscription.save()

    self.assertEqual(subscription.status, 'active')

    cancel_subscription = {
      'status': 'cancelled'
    }

    updated_response = self.client.patch(f'/api/v1/customers/{customer.id}/subscriptions/{subscription.id}/', cancel_subscription, format = 'json')

    self.assertEqual(updated_response.status_code, 200)

    self.assertNotEqual(updated_response.data['status'], subscription.status)
    self.assertEqual(updated_response.data['status'], 'cancelled')
    self.assertEqual(updated_response.data['id'], subscription.id)
    self.assertEqual(updated_response.data['title'], subscription.title)
    self.assertEqual(updated_response.data['price'], subscription.price)
    self.assertEqual(updated_response.data['frequency'], subscription.frequency)
    self.assertEqual(Subscription.objects.all().count(), 1)
    self.assertEqual(Customer.objects.all().count(), 1)

  def test_customer_adds_a_subscription(self):
    customer = Customer(
    id = 2,
    first_name = 'Hai',
    last_name = 'Sall',
    email = 'sailt&peppa@saimall.com',
    address = 'this place Seattle, WA'
    )
    customer.save()

    subscription_request = { 
      'id': 1,
      'title': 'Tea Partay',
      'price': 50.99,
      'status': "active",
      'frequency': 'monthly'
    }

    response_before_post = self.client.get(f'/api/v1/customers/{customer.id}/subscriptions/', format = 'json')

    self.assertEqual(response_before_post.status_code, 200)
    self.assertEqual(len(response_before_post.data), 0)
    self.assertEqual(Subscription.objects.all().count(), 0)
    self.assertEqual(Customer.objects.all().count(), 1)

    updated_response = self.client.post(f'/api/v1/customers/{customer.id}/subscription/', subscription_request,  format = 'json')

    self.assertEqual(updated_response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(updated_response.data['id'], subscription_request["id"])
    self.assertEqual(updated_response.data['title'], subscription_request['title'])
    self.assertEqual(updated_response.data['price'], subscription_request['price'])
    self.assertEqual(updated_response.data['frequency'], subscription_request['frequency'])

    response_after_post = self.client.get(f'/api/v1/customers/{customer.id}/subscriptions/', format = 'json')

    self.assertEqual(response_after_post.status_code, 200)
    self.assertEqual(len(response_after_post.data), 1)
    self.assertEqual(Subscription.objects.all().count(), 1)
    self.assertEqual(Customer.objects.all().count(), 1)


# subscription2.customers is None, this is a valued way of testing that there is no customer in a specific subscription