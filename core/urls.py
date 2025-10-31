from django.urls import path
from .views import home, cookie_settings, accept_cookies

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path("accept-cookies/", accept_cookies, name="accept_cookies"),
    path("cookies/", cookie_settings, name="cookie_settings"),
]