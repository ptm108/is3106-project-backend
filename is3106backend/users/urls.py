from django.urls import path

from . import views

urlpatterns = [
  path('', views.HelloView.as_view(), name='hello'),
  path('delete_user', views.delete_user, name="delete user")
]