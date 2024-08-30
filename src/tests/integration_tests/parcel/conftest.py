from typing import Any

import pytest
from django.contrib.auth.models import AbstractBaseUser
from model_bakery import baker

from parcel.models import Address, Article, UserShipment


@pytest.fixture
def articles() -> list[Article]:
    return baker.make(Article, _quantity=5)


@pytest.fixture
def article() -> Article:
    return baker.make(Article)


@pytest.fixture
def addresses() -> list[Address]:
    return baker.make(Address, _quantity=5)


@pytest.fixture
def address() -> Address:
    return baker.make(Address)


@pytest.fixture
def user_shipments(user: AbstractBaseUser) -> list[UserShipment]:
    return baker.make(UserShipment, user=user, _quantity=5)


@pytest.fixture
def admin_user_shipments(superuser: AbstractBaseUser) -> list[UserShipment]:
    return baker.make(UserShipment, user=superuser, _quantity=5)


@pytest.fixture
def prepared_user_shipment(
    user: AbstractBaseUser, article: Article, address: Address
) -> dict[str, Any]:
    return {
        "user": user.id,  # type: ignore[attr-defined]
        "article": article.id,
        "article_quantity": 1,
        "carrier": "USPS",
        "tracking_number": "123456789",
        "sender_address": address.id,
        "receiver_address": address.id,
    }
