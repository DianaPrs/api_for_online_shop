"""django_online_shop URL Configuration

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
from django.urls import path, include
from online_shop.views import ProductViewSet, OrderViewSet, ReviweViewSet, ProductCollectionViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')
router.register('product-reviews', ReviweViewSet, basename='product-reviews')
router.register('product-collections', ProductCollectionViewSet, basename='product-collections')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),   
]