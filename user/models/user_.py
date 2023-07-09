from django.contrib.auth.models import AbstractUser
from django.db import models
from shared.models import upload_name


class User(AbstractUser):
    class SubscriptionChoice(models.TextChoices):
        free = "Free", "free"
        premium = "Premium", "premium"

    class RoleChoice(models.TextChoices):
        admin = "Admin", "admin"
        moderator = "Moderator", "moderator"
        user = "User", "user"

    class StatusChoice(models.TextChoices):
        banned = "Banned", "banned"
        approved = "Approved", "approved"

    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to=upload_name)
    balance = models.DecimalField(max_digits=10000000, decimal_places=2, default=0)
    subscription = models.CharField(max_length=255, choices=SubscriptionChoice.choices, default=SubscriptionChoice.free)
    role = models.CharField(max_length=255, choices=RoleChoice.choices, default=RoleChoice.user)
    status = models.CharField(max_length=255, choices=StatusChoice.choices, default=StatusChoice.approved)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'

