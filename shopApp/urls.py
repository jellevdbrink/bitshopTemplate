"""
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
from django.conf.urls.static import static
from django.urls import path

from bitshopTemplate import settings
from shopApp import views

urlpatterns = [
    path('cart/add/<int:prod_id>/', views.cart_add, name='cart_add'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('cart/item_increment/<str:key>/', views.cart_item_increment, name='cart_item_increment'),
    path('cart/item_decrement/<str:key>/', views.cart_item_decrement, name='cart_item_decrement'),
    path('cart/item_remove/<str:key>/', views.cart_item_remove, name='cart_item_remove'),
    path('cart/', views.cart_view, name='cart'),

    path('bestelling/', views.bestelling, name='bestelling'),

    path('nieuwe_klant/', views.nieuwe_klant, name='nieuwe_klant'),

    path('filter/<str:cat>', views.product_filter, name='filter'),
    path('', views.product_filter, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
