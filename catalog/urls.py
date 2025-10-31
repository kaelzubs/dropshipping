from django.urls import path
from .views import product_list, product_detail, search_product

app_name = 'catalog'

urlpatterns = [
    path('', product_list, name='list'),
    path('search-result/', search_product, name='search'),
    path('<slug:slug>/', product_detail, name='detail'),
]