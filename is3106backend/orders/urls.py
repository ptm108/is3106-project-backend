from django.urls import path

from . import views

urlpatterns = [
  path('', views.protected_order_view, name='Get user orders'),
]