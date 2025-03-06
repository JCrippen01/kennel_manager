from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_name.models import Kennel


class Command(BaseCommand):
    help = "Create user groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Create user group
        user_group, created = Group.objects.get_or_create(name="user")
        if created:
            self.stdout.write(self.style.SUCCESS("User group created"))

        # Create admin group
        admin_group, created = Group.objects.get_or_create(name="admin")
        if created:
            self.stdout.write(self.style.SUCCESS("Admin group created"))

        # Assign permissions to admin group
        content_type = ContentType.objects.get_for_model(Kennel)
        permissions = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Permissions assigned to admin group"))
