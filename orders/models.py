import uuid
from django.db import models


class Order(models.Model):
    PAYMENT_METHODS = [
        ("airtel_money", "Airtel Money"),
        ("moov_money", "Moov Money"),
    ]
    STATUSES = [
        ("demo_created", "Demo — unpaid"),
        ("demo_approved", "Demo approval simulated — unpaid"),
    ]

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    bundle_code = models.CharField(max_length=24)
    bundle_name = models.CharField(max_length=64)
    data_volume = models.CharField(max_length=24, blank=True)
    amount_fcfa = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    phone_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=24, choices=STATUSES, default="demo_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.reference} · {self.bundle_name} · {self.amount_fcfa} FCFA"