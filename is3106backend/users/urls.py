from django.urls import path

from . import views

urlpatterns = [
  path('', views.HelloView.as_view(), name='hello'),
  path('create_user', views.create_user, name='create user'),
  path('delete_user', views.delete_user, name='delete user'),
  path('create_delivery_address', views.create_delivery_address, name='create a delivery address'),
  path('delete_delivery_address/<slug:pk>', views.delete_delivery_address, name='delete a delivery address'),
  path('get_delivery_addresses', views.get_delivery_addresses, name='get user delivery addresses'),
  path('check_session', views.check_session, name='check validity of jwt')
]