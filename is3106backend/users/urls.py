from django.urls import path

from . import views

urlpatterns = [
  path('', views.user_view, name='create user'),
  path('/user', views.protected_user_view, name=' get and delete user'),
  path('/user/<slug:pk>', views.protected_user_update_view, name='update users profile and change password'),
  path('/delivery-address', views.protected_user_delivery_address_view, name='create a delivery address and get all delivery addresses'),
  path('/delivery-address/<slug:pk>', views.protected_user_delivery_address_delete_view, name='delete a delivery address'),
  path('/check_session', views.check_session, name='check validity of jwt'), 
]