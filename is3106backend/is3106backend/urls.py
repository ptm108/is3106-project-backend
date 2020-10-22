"""is3106backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    # authentication endpoints
    path('admin/', admin.site.urls),
    path('auth', include('users.urls')),

    # recipe endpoints
    path('recipes', include('recipes.urls')),

    # orders endpoints
    path('groupbuys', include('orders.urls')),

    # rest framework end points
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # simple jwt endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
