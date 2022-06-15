"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('home-decor/', views.HomeDecor, name='home-decor'),
    path('create-post/', views.CreatePostView.as_view(), name='create-post'),
    path('my-post/', views.MyPostView.as_view(), name='my-post'),
    path('my-edit/id=<int:id>', views.MyEditView.as_view(), name='my-edit'),
    path('my-delete/id=<int:id>', views.MyDeleteView.as_view(), name='my-delete'),
    path('search/', views.search_page, name='search_result'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('buy-now-inquiry/<int:id>', views.BuyNowView.as_view(), name='buy-now-inquiry'),
    path('my-order-list', views.MyOrderView.as_view(), name='my-order-list'),
    path('my-order-accept', views.MyOrderAcceptView.as_view(), name='my-order-accept'),
    path('my-purchased/', views.my_purchase, name='my-purchased'),
]
