import csv
from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from parcel.models import Address, Article, UserShipment


# Create a custom management command to encapsulate the population logic
class Command(BaseCommand):
    help = "Populate the database with shipment data from CSV."

    def handle(self, *args: Any, **options: Any) -> None:
        filepath = "src/resources/shipment_data.csv"
        user_model = get_user_model()

        # Assuming all shipments are for the same user for simplicity
        user = user_model.objects.first()
        if not user:
            self.stdout.write(
                self.style.ERROR("No user found in the database.")
            )
            return

        with open(filepath, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            with transaction.atomic():
                for row in reader:
                    tracking_number = row["tracking_number"]
                    carrier = row["carrier"]
                    sender_address = self.get_or_create_address(
                        row["sender_address"]
                    )
                    receiver_address = self.get_or_create_address(
                        row["receiver_address"]
                    )
                    article = self.get_or_create_article(
                        row["article_name"],
                        row["article_price"],
                        row["SKU"],
                    )
                    status = row["status"]

                    shipment = UserShipment(
                        user=user,
                        article=article,
                        article_quantity=row["article_quantity"],
                        tracking_number=tracking_number,
                        carrier=carrier,
                        status=status,
                        sender_address=sender_address,
                        receiver_address=receiver_address,
                    )
                    shipment.save()
                self.stdout.write(
                    self.style.SUCCESS("Database populated successfully.")
                )

    def get_or_create_address(self, address_str: str) -> Address:
        street, postal_code, city, country = map(
            str.strip, address_str.split(",")
        )
        address, _ = Address.objects.get_or_create(
            street=street,
            city=city,
            country=country,
            postal_code=postal_code,
        )
        return address

    def get_or_create_article(
        self, name: str, price: str, sku: str
    ) -> Article:
        article, _ = Article.objects.get_or_create(
            name=name,
            price=Decimal(price),
            sku=sku,
        )
        return article
