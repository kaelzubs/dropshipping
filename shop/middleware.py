import json

class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raw = request.COOKIES.get("cookie_consent")
        consent = {}
        if raw:
            try: consent = json.loads(raw)
            except Exception: consent = {}
        request.cookie_consent = consent
        response = self.get_response(request)

        # Example: if you set any marketing cookies server-side, clear them if not consented
        if not consent.get("marketing"):
            response.delete_cookie("marketing_cookie_name")

        return response