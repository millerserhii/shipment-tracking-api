from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    DecimalField,
    ForeignKey,
    PositiveSmallIntegerField,
    TextChoices,
)

from utils.base_models import BaseHistory


UserModel = get_user_model()


class Address(BaseHistory):
    street = CharField(max_length=100)
    city = CharField(max_length=100)
    country = CharField(max_length=100)
    postal_code = CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"{self.street} {self.postal_code}, {self.city}, {self.country}"


class Article(BaseHistory):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    sku = CharField(max_length=30)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Articles"


class UserShipment(BaseHistory):
    """
    Model to store user's shipments
    """

    class Status(TextChoices):
        """
        Choices for limit periods
        """

        IN_TRANSIT = "in-transit", "In Transit"
        INBOUND_SCAN = "inbound-scan", "Inbound Scan"
        DELIVERY = "delivery", "Out for Delivery"
        TRANSIT = "transit", "In Transit"
        SCANNED = "scanned", "Scanned"

    user = ForeignKey(UserModel, on_delete=CASCADE)
    article = ForeignKey(Article, on_delete=PROTECT)
    article_quantity = PositiveSmallIntegerField(default=1)
    tracking_number = CharField(max_length=100)
    carrier = CharField(max_length=100)
    status = CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_TRANSIT,
    )
    sender_address = ForeignKey(
        Address, on_delete=PROTECT, related_name="sender_shipments"
    )
    receiver_address = ForeignKey(
        Address, on_delete=PROTECT, related_name="receiver_shipments"
    )

    class Meta:
        verbose_name_plural = "User Shipments"

    def __str__(self) -> str:
        return f"{self.user}: {self.tracking_number} - {self.status}"
