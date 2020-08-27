from django.urls import path

from . import views

urlpatterns = [
  path('', views.HelloView.as_view(), name='hello'),
  path('create_user', views.create_user, name="create user"),
  path('delete_user', views.delete_user, name="delete user")
]