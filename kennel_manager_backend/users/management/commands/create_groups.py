from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create user groups and assign permissions"

    def handle(self, *args, **kwargs):
        user_group, created = Group.objects.get_or_create(name="user")
        admin_group, created = Group.objects.get_or_create(name="admin")
        content_type = ContentType.objects.get_for_model(User)
        permissions = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.set(permissions)
