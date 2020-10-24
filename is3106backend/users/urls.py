from django.urls import path

from . import views

urlpatterns = [
  path('', views.user_view, name='create user'),
  path('/<slug:pk>', views.protected_user_view, name=' get, delete, update users profile and change password'),
  path('/<slug:pk>/delivery-address', views.protected_user_delivery_address_view, name='create a delivery address and get all delivery addresses'),
  path('/<slug:pk>/delivery-address/<slug:da_id>', views.protected_user_delivery_address_delete_view, name='delete a delivery address'),
  path('/check_session', views.check_session, name='check validity of jwt'), 
]