from django.urls import path

from . import views

urlpatterns = [
  path('', views.DefaultView.as_view(), name='default'),
  path('create_recipe', views.create_recipe, name="create recipe"),
  path('delete_recipe/<slug:pk>', views.delete_recipe, name="delete recipe"),
  path('undelete_recipe/<slug:pk>', views.undelete_recipe, name="undelete recipe"),
  path('get_recipes', views.get_recipes, name="get my recipes"),
]