from django.contrib.auth import get_user_model
from rest_framework import serializers
import re

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def validate_password(self, value):
        """Enforce strong password policy"""
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        if not re.search(r"[@$!%*?&]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character (@$!%*?&)."
            )
        return value

    def create(self, validated_data):
        """Create user with hashed password but keep inactive until email verified"""
        user = User.objects.create_user(**validated_data, is_active=False)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)
    confirm_password = serializers.CharField(
        write_only=True, required=False, min_length=8
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "new_password",
            "confirm_password",
            "role",
        ]
        read_only_fields = ["role"]  # Customers cannot change roles

    def validate(self, data):
        """Ensure passwords match when updating"""
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError(
                    {"confirm_password": "Passwords do not match."}
                )

        return data

    def update(self, instance, validated_data):
        """Handle password update properly"""
        validated_data.pop("confirm_password", None)

        if "new_password" in validated_data:
            instance.set_password(validated_data.pop("new_password"))

        return super().update(instance, validated_data)


# ✅ Email Verification Serializer
class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for verifying user email"""

    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if user with this email exists"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


# ✅ Password Reset Request Serializer
class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting a password reset email"""

    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if user exists before sending reset link"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


# ✅ Password Reset Serializer
class PasswordResetSerializer(serializers.Serializer):
    """Serializer for resetting user password"""

    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        """Ensure both passwords match"""
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return data
