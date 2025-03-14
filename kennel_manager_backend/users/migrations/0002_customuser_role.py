# Generated by Django 5.1.6 on 2025-03-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("staff", "Staff"),
                    ("customer", "Customer"),
                ],
                default="customer",
                max_length=20,
            ),
        ),
    ]
