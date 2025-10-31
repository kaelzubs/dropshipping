from django.shortcuts import render, redirect
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from .utils.mailchimp import subscribe_user
from rest_framework_simplejwt.tokens import AccessToken
from .forms import CustomUserCreationForm, LoginForm
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
# def register_template(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.is_active = False
#         user.save()

#         token = AccessToken.for_user(user)
#         verify_url = request.build_absolute_uri(reverse("verify_email")) + f"?token={str(token)}"

#         send_mail(
#             subject="Verify your email",
#             message=f"Click the link to verify your account: {verify_url}",
#             from_email="noreply@yourstore.com",
#             recipient_list=[email],
#         )

#         return render(request, "accounts/registration_pending.html", {"email": email})

#     return render(request, "accounts/register.html")
# accounts/views.py

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # require email verification
            user.save()

            token = AccessToken.for_user(user)
            verify_link = request.build_absolute_uri(
                reverse("accounts:verify_email")
            ) + f"?token={str(token)}"

            send_mail(
                subject="Verify your email - YourStore",
                message=f"Welcome to YourStore!\n\nClick to verify: {verify_link}\n\nThis link expires in 1 hour.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            return render(request, "accounts/registration_pending.html", {"email": user.email})
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})

def verify_email(request):
    token = request.GET.get("token")
    if not token:
        return render(request, "accounts/verification_failed.html")

    try:
        access = AccessToken(token)
        user_id = access["user_id"]
        user = User.objects.get(id=user_id)
        if not user.is_active:
            user.is_active = True
            user.save()
        return render(request, "accounts/verification_success.html", {"user": user})
    except Exception:
        return render(request, "accounts/verification_failed.html")


# def jwt_login(request):
#     form = CustomUserCreationForm(request.POST)
#     if form.is_valid():
#         user = form.save(commit=False)
#         user.is_active = False  # require email verification
#         user.save()

#         token = AccessToken.for_user(user)

#         if user is not None:
#             # Issue JWT tokens
#             refresh = RefreshToken.for_user(user)
#             login(request, user, token)
#             # You could store tokens in cookies or return JSON
#             return render(request, "accounts/login_success.html", {
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#             })
#         else:
#             # Invalid credentials → show error and suggest reset
#             return render(request, "accounts/login.html", {
#                 "error": "Invalid username or password. You can reset your password below."
#             })

#     return render(request, "accounts/login.html")

def jwt_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Issue JWT tokens
                    login(request, user)
                    return redirect("core:home")  # replace with your dashboard/home
                else:
                    messages.error(request, "Your email is not verified. Please check your inbox.")
            else:
                messages.error(request, "Invalid username or password. Click on the link below to reset password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_template(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('accounts:login')

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            # uri_path = "{% url 'accounts:reset_password' %}"
            reset_link = request.build_absolute_uri(f"/accounts/reset/{uid}/{token}/")
            send_mail(
                "Password Reset",
                f"Click here to reset your password: {reset_link}",
                "support@yourstore.com",
                [email],
            )
        except User.DoesNotExist:
            pass  # don't reveal if email exists
        return render(request, "accounts/password_reset_request_done.html")
    return render(request, "accounts/password_reset_request.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return render(request, "accounts/password_reset_invalid.html")

    if not token_generator.check_token(user, token):
        return render(request, "accounts/password_reset_invalid.html")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        user.set_password(new_password)
        user.save()
        return render(request, "accounts/password_reset_complete.html")

    return render(request, "accounts/password_reset_confirm.html", {"uidb64": uidb64, "token": token})

def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        result = subscribe_user(email)

        if result['success']:
           return redirect("accounts:mailchimp_confirm")
        elif result['reason']:
            # email already subscribed
            return render(request, "accounts/mailchimp_failed.html", {
                "reason": "exists",
                "email": email,
            })
        elif result['pending']:
            # email already subscribed
            return render(request, "accounts/mailchimp_failed.html", {
                "reason": "pending",
                "email": email,
            })
        else:
            # some other error
            return render(request, "accounts/mailchimp_failed.html", {
                "reason": "other",
                "email": email,
            })

    return render(request, "accounts/newsletter_form.html")


def mailchimp_confirm(request):
    return render(request, "accounts/mailchimp_confirm.html")

def mailchimp_failed(request):
    return render(request, "accounts/mailchimp_failed.html")

# def contact(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         subject = request.POST.get("subject")
#         message = request.POST.get("message")

#         full_message = f"From: {name} <{email}>\n\n{message}"

#         send_mail(
#             subject,
#             full_message,
#             "support@yourstore.com",  # from
#             ["support@yourstore.com"],  # to
#         )
#         return render(request, "accounts/contact_success.html", {"name": request.POST.get("name")})

#     return render(request, "accounts/contact.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "accounts/contact.html", {"error": "Invalid email address."})

        full_message = f"From: {name} <{email}>\n\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                "support@yourstore.com",
                ["support@yourstore.com"],
                headers={"Reply-To": email},
            )
            return render(request, "accounts/contact_success.html", {"name": name})
        except Exception:
            return render(request, "accounts/contact.html", {"error": "Message could not be sent. Please try again."})

    return render(request, "accounts/contact.html")