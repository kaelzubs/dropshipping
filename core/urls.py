from django.urls import path
from .views import home, cookie_settings

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path("cookies/", cookie_settings, name="cookie_settings"),
]