from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
from django.db.models import Q
from django.http import HttpResponse
import json
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator



def home(request):
    products = Product.objects.filter(is_active=True)[:12]
    return render(request, 'core/home.html', {'products': products})


def search_product(request):
    query = request.GET.get('q', '').strip()
    if not query:
        products = Product.objects.none()
    else:
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()
    products = Product.objects.filter(is_active=True).order_by('-id')
    paginator = Paginator(products, 4)  # 12 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/search.html', {'products': products, 'query': query, 'page_obj': page_obj})


CONSENT_COOKIE_NAME = "cookie_consent"
CONSENT_MAX_AGE = 365 * 24 * 60 * 60  # one year

def cookie_settings(request):
    """
    Render a cookie settings page and allow users to update their preferences.
    """
    if request.method == "POST":
        data = {
            "essential": True,  # always true; essential cookies cannot be disabled
            "analytics": bool(request.POST.get("analytics")),
            "marketing": bool(request.POST.get("marketing")),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": 1,
        }
        response = redirect("cookie_settings")
        response.set_cookie(
            CONSENT_COOKIE_NAME,
            json.dumps(data),
            max_age=CONSENT_MAX_AGE,
            secure=True,          # set True in production with HTTPS
            samesite="Lax",
            httponly=False        # must be readable by JS to gate scripts client-side
        )
        return response

    # Read current preferences if present
    raw = request.COOKIES.get(CONSENT_COOKIE_NAME)
    prefs = {"essential": True, "analytics": False, "marketing": False}
    if raw:
        try:
            prefs.update(json.loads(raw))
        except Exception:
            pass

    return render(request, "partials/cookie_settings.html", {"prefs": prefs})

def restricted_view(request):
    raise PermissionDenied