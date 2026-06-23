from django.db import models
from django.conf import settings


class Product(models.Model):
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    # Customer sees this price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Minimum price vendor accepts
    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title