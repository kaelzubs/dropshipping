from django.urls import path
from .views import home, search_product, cookie_settings

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('search-result/', search_product, name='search'),
    path("cookies/", cookie_settings, name="cookie_settings"),

]