from django.db import models
from django.conf import settings


class Payment(models.Model):

    STATUS_CHOICES = [
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    amount = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.amount}"