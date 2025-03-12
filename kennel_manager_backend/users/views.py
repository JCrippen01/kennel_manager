from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
from .permissions import IsAdmin, IsStaff, IsCustomer
from .tokens import account_activation_token
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Generate JWT tokens for authentication."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            send_verification_email(user, request)
            return Response(
                {"message": "User registered successfully. Please verify your email."},
                status=status.HTTP_201_CREATED,
            )
        except IntegrityError:
            return Response(
                {"error": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    logger.warning("Invalid registration attempt", extra={"data": serializer.errors})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_verification_email(user, request):
    """Send email verification link."""
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse("verify-email", kwargs={"uidb64": uid, "token": token})
    verification_url = f"http://{domain}{link}"

    send_mail(
        "Verify your email",
        f"Click the link to verify your email: {verification_url}",
        "noreply@yourdomain.com",
        [user.email],
        fail_silently=False,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    """Verify user email via token."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({"error": "Invalid verification link."}, status=400)

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully."}, status=200)
    return Response({"error": "Invalid or expired token."}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    """Request password reset via email."""
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        send_password_reset_email(user, request)
        return Response({"message": "Password reset email sent."}, status=200)
    return Response(serializer.errors, status=400)


def send_password_reset_email(user, request):
    """Send password reset email."""
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse("password-reset-confirm", kwargs={"uidb64": uid, "token": token})
    reset_url = f"http://{domain}{link}"

    send_mail(
        "Reset your password",
        f"Click the link to reset your password: {reset_url}",
        "noreply@yourdomain.com",
        [user.email],
        fail_silently=False,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, uidb64, token):
    """Reset user password via email token."""
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid reset link."}, status=400)

        if account_activation_token.check_token(user, token):
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password reset successfully."}, status=200)
        return Response({"error": "Invalid or expired token."}, status=400)
    return Response(serializer.errors, status=400)
