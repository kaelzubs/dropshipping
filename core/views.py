from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
import json
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

CONSENT_COOKIE_NAME = "cookie_consent"
CONSENT_MAX_AGE = 365 * 24 * 60 * 60  # one year

def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    return render(request, 'core/home.html', {'products': products})

def accept_cookies(request):
    response = HttpResponseRedirect("/")
    response.set_cookie("cookie_consent", "yes", max_age=31536000)  # 1 year
    return response

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