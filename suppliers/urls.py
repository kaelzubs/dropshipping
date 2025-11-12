from django.urls import path
from .views import send_to_supplier, terms_and_conditions, privacy_policy, shipping_returns, faq, about_us

app_name = 'suppliers'
urlpatterns = [
    path("terms/", terms_and_conditions, name="terms"),
    path("privacy/", privacy_policy, name="privacy"),
    path("shipping-returns/", shipping_returns, name="shipping_returns"),
    path("faq/", faq, name="faq"),
    path("about/", about_us, name="about_us"),
    path('send/<int:order_id>/<int:supplier_id>/', send_to_supplier, name='send'),
]