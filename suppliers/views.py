from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from orders.models import Order
from .models import Supplier
from .services import send_order_to_supplier
from datetime import date

def send_to_supplier(request, order_id, supplier_id):
    order = get_object_or_404(Order, id=order_id, status__in=['paid','created'])
    supplier = get_object_or_404(Supplier, id=supplier_id, active=True)
    so = send_order_to_supplier(order, supplier)
    messages.info(request, f'Supplier status: {so.status}')
    return redirect('orders:success', order_id=order.id) # pyright: ignore[reportAttributeAccessIssue]


def terms_and_conditions(request):
    context = {
        "last_updated": date.today().strftime("%B %d, %Y"),
        "store_name": "YourStore",  # customize or load from settings/site config
        "support_email": "support@yourstore.com",
        "currency_label": "USD",    # adjust for your market
        "return_window_days": 14,   # match your policy
    }
    return render(request, "core/terms_and_conditions.html", context)

def privacy_policy(request):
    context = {
        "last_updated": date.today().strftime("%B %d, %Y"),
        "store_name": "YourStore",             # customize or load from settings/site config
        "support_email": "support@yourstore.com",
        "data_retention_months": 24,           # adjust to your policy
        "jurisdiction": "Nigeria",             # e.g., Nigeria, EU, UK, US
    }
    return render(request, "core/privacy_policy.html", context)

def shipping_returns(request):
    context = {
        "last_updated": date.today().strftime("%B %d, %Y"),
        "store_name": "YourStore",             # customize
        "support_email": "support@yourstore.com",
        "return_window_days": 14,              # adjust to your policy
        "currency_label": "USD",               # adjust for your market
    }
    return render(request, "core/shipping_returns.html", context)

def faq(request):
    faqs = [
        {
            "question": "How long does shipping take?",
            "answer": "Orders are processed within 2–5 business days. Delivery usually takes 7–21 business days depending on your location and supplier."
        },
        {
            "question": "Do you ship internationally?",
            "answer": "Yes, we ship worldwide. Customs duties and taxes may apply depending on your country."
        },
        {
            "question": "Can I track my order?",
            "answer": "Yes, once your order is shipped, you will receive a tracking number by email."
        },
        {
            "question": "What is your return policy?",
            "answer": "We accept returns for defective or damaged items reported within 14 days of delivery. Contact support before sending items back."
        },
        {
            "question": "Who do I contact for support?",
            "answer": "You can reach us at support@yourstore.com for any questions or issues."
        },
    ]
    context = {
        "last_updated": date.today().strftime("%B %d, %Y"),
        "faqs": faqs,
        "store_name": "YourStore",
    }
    return render(request, "core/faq.html", context)

def about_us(request):
    context = {
        "last_updated": date.today().strftime("%B %d, %Y"),
        "store_name": "YourStore",  # customize
        "mission": "To connect customers with quality products at affordable prices through a seamless dropshipping model.",
        "vision": "To become a trusted global e‑commerce brand that empowers customers with choice and convenience.",
        "support_email": "support@yourstore.com",
    }
    return render(request, "core/about_us.html", context)