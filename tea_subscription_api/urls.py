from django.urls import path
# from .views import CustomerSubscriptionsView
from . import views

urlpatterns = [
  path('customers/<int:customer_id>/subscriptions/<int:subscription_id>/', views.update_subscription, name='update_subscription'),
  path('customers/<int:customer_id>/subscription/', views.subscribe_a_customer, name='subscribe_a_customer'),
  path('customers/<int:customer_id>/subscriptions/', views.customer_subscriptions, name='customer_subscriptions'),
  path('', views.ApiOverview, name='home')
]