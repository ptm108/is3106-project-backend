from django.urls import path

from . import views

urlpatterns = [
  path('', views.DefaultView.as_view(), name='default'),
  path('create_recipe', views.create_recipe, name="create recipe"),
]