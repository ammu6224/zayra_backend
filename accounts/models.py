from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="accounts_user_set",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="accounts_user_permissions_set",
        blank=True,
    )

    def __str__(self):
        return self.username
