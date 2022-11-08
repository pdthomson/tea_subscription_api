import unittest
from django.test import TestCase
from tea_subscription_api import *
from tea_subscription_api.models import *
from tea_subscription_api.serializers import SubscriptionSerializer

class SubscriptionSerializerTestCase(TestCase):

  def setUp(self):
    self.subscription_attributes = {
      'id': 1,
      'title': 'Tea-time',
      'price': 22.50,
      'status': 'active',
      'frequency': 'bi-weekly' 
    }

    self.serializer_data = {
      'id': 1,
      'title': 'Tea-House',
      'price': 38.75,
      'status': 'cancelled',
      'frequency': 'monthly' 
    }

    self.subscription = Subscription.objects.create(**self.subscription_attributes)
    self.serializer = SubscriptionSerializer(instance=self.subscription)

  def test_subscription_serializer_has_correct_keys(self):
    data = self.serializer.data
    
    self.assertEqual(set(data.keys()), set(['id', 'title', 'price', 'status', 'frequency', 'customers']))

  def test_subscription_field_contents(self):
    data = self.serializer.data 

    self.assertEqual(data['id'], self.subscription_attributes['id'])
    self.assertEqual(data['title'], self.subscription_attributes['title'])
    self.assertEqual(data['price'], self.subscription_attributes['price'])
    self.assertEqual(data['status'], self.subscription_attributes['status'])
    self.assertEqual(data['frequency'], self.subscription_attributes['frequency'])

  def test_sad_path_serializer(self):
    data = self.serializer.data 

    self.assertNotEqual(data['title'], self.serializer_data['title'])
    self.assertNotEqual(data['price'], self.serializer_data['price'])
    self.assertNotEqual(data['status'], self.serializer_data['status'])
    self.assertNotEqual(data['frequency'], self.serializer_data['frequency'])

  def test_status_must_be_in_choices(self):
    self.subscription_attributes['status'] = 'thinking about it'

    serializer = SubscriptionSerializer(instance=self.subscription, data=self.subscription_attributes)

    self.assertFalse(serializer.is_valid())
    self.assertEqual(set(serializer.errors.keys()), set(['status']))

