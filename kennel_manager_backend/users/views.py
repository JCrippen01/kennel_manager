from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
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
    """Register a new user and send email verification."""
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
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            return Response(
                {"error": "An unexpected error occurred. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    logger.warning("Invalid registration attempt", extra={"data": serializer.errors})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Authenticate a user and return fresh JWT tokens."""
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        # ✅ Always generate a fresh token set
        tokens = get_tokens_for_user(user)
        return Response(
            {
                "message": "Login successful",
                "username": user.username,
                "access": tokens["access"],  # Fresh Access Token
                "refresh": tokens["refresh"],  # Fresh Refresh Token
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout user by blacklisting the refresh token."""
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Retrieve user profile details."""
    user = request.user
    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Allow users to update their profile information."""
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Profile updated successfully", "user": serializer.data},
            status=status.HTTP_200_OK,
        )
    logger.warning(
        "Profile update failed", extra={"user": user.id, "errors": serializer.errors}
    )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    """Admin dashboard endpoint."""
    return Response(
        {"message": "Welcome to the admin dashboard."}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def staff_dashboard(request):
    """Staff dashboard endpoint."""
    if request.user.role != "staff":
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    return Response(
        {"message": "Welcome to the staff dashboard."}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def customer_dashboard(request):
    """Customer dashboard endpoint."""
    if request.user.role != "customer":
        return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)
    return Response(
        {"message": "Welcome to the customer dashboard."}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_users(request):
    """Admin endpoint to list all registered users."""
    users = User.objects.all().values("id", "username", "email", "is_active", "role")
    return Response({"users": list(users)}, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def update_user_role(request, user_id):
    """Admin function to update a user's role."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    new_role = request.data.get("role")
    if new_role not in ["admin", "staff", "customer"]:
        return Response(
            {"error": "Invalid role specified."}, status=status.HTTP_400_BAD_REQUEST
        )

    user.role = new_role
    user.save()
    return Response(
        {"message": "User role updated successfully."}, status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    """Admin function to delete a user."""
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


def send_verification_email(user, request):
    """Send email verification link to the user."""
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse("verify-email", kwargs={"uidb64": uid, "token": token})
    verification_url = f"http://{domain}{link}"

    try:
        send_mail(
            "Verify your email",
            f"Click the link to verify your email: {verification_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Email verification failed: {e}")


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


def send_password_reset_email(user, request):
    """Send password reset email."""
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    link = reverse("password-reset-confirm", kwargs={"uidb64": uid, "token": token})
    reset_url = f"http://{domain}{link}"

    try:
        send_mail(
            "Reset your password",
            f"Click the link to reset your password: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Password reset email failed: {e}")


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
