from enum import unique
from django.db import models

class Tea(models.Model):#has_many :subscriptions
  title = models.CharField(max_length = 100)
  description = models.CharField(max_length = 1000)
  temperature = models.IntegerField()
  brew_time = models.IntegerField()

class Customer(models.Model):#has_many :subscriptions
  first_name = models.CharField(max_length = 100)
  last_name = models.CharField(max_length = 100)
  email = models.EmailField(max_length = 300)
  address = models.CharField(max_length = 500)

class Subscription(models.Model):#belongs_to :customers, :tea
  status_choice = {
    ('active', 'active'),
    ('cancelled', 'cancelled')
  }

  title = models.CharField(max_length = 100)
  price = models.FloatField()
  status = models.CharField(max_length = 100, choices = status_choice)
  frequency = models.CharField(max_length = 100)
  customers = models.ForeignKey(Customer, related_name = 'subscriptions', blank = True, null = True, on_delete = models.CASCADE)
  teas = models.ForeignKey(Tea, blank = True, null = True, on_delete = models.CASCADE)

