from typing import Any

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from parcel.models import Address, Article, UserShipment


@pytest.mark.django_db
def test_address_list(api_client: APIClient, addresses: list[Address]) -> None:
    url = reverse("address-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    results = response.data.get("results", [])
    assert len(results) == 5
    fixture_ids = sorted([str(address.id) for address in addresses])
    response_ids = sorted([result["id"] for result in results])
    assert fixture_ids == response_ids


@pytest.mark.django_db
def test_article_list(api_client: APIClient, articles: list[Article]) -> None:
    url = reverse("article-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    results = response.data.get("results", [])
    assert len(results) == 5
    fixture_ids = sorted([str(item.id) for item in articles])
    response_ids = sorted([result["id"] for result in results])
    assert fixture_ids == response_ids


@pytest.mark.django_db
def test_address_detail(
    api_client: APIClient, addresses: list[Address]
) -> None:
    url = reverse("address-detail", args=[addresses[0].id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.data.get("country") == addresses[0].country


@pytest.mark.django_db
def test_article_detail(
    api_client: APIClient, articles: list[Article]
) -> None:
    url = reverse("article-detail", args=[articles[0].id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.data.get("name") == articles[0].name


@pytest.mark.django_db
def test_address_post(api_client: APIClient) -> None:
    url = reverse("address-list")
    response = api_client.post(url)

    assert response.status_code == 405


@pytest.mark.django_db
def test_article_post(api_client: APIClient) -> None:
    url = reverse("article-list")
    response = api_client.post(url)

    assert response.status_code == 405


@pytest.mark.django_db
def test_address_put_patch_delete(
    api_client: APIClient, addresses: list[Address]
) -> None:
    url = reverse("address-detail", args=[addresses[0].id])
    response = api_client.put(url)
    assert response.status_code == 405

    response = api_client.patch(url)
    assert response.status_code == 405

    response = api_client.delete(url)
    assert response.status_code == 405


@pytest.mark.django_db
def test_article_put_patch_delete(
    api_client: APIClient, articles: list[Article]
) -> None:
    url = reverse("article-detail", args=[articles[0].id])
    response = api_client.put(url)
    assert response.status_code == 405

    response = api_client.patch(url)
    assert response.status_code == 405

    response = api_client.delete(url)
    assert response.status_code == 405


@pytest.mark.django_db
def test_admin_user_shipment_list(
    auth_api_client_superuser: APIClient,
    user_shipments: list[UserShipment],
    admin_user_shipments: list[UserShipment],
) -> None:
    """
    Test that an admin user can see all shipments.
    """
    url = reverse("usershipment-list")
    response = auth_api_client_superuser.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    results = response.data.get("results", [])
    assert len(results) == 10
    fixture_ids = sorted(
        [str(item.id) for item in user_shipments + admin_user_shipments]
    )
    response_ids = sorted([result["id"] for result in results])
    assert fixture_ids == response_ids


@pytest.mark.django_db
def test_user_shipment_list(
    auth_api_client: APIClient,
    user_shipments: list[UserShipment],
    admin_user_shipments: list[  # pylint: disable=unused-argument
        UserShipment
    ],
) -> None:
    """
    Test that a user can only see their own shipments.
    """
    url = reverse("usershipment-list")
    response = auth_api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, dict)
    results = response.data.get("results", [])
    assert len(results) == 5
    fixture_ids = sorted([str(item.id) for item in user_shipments])
    response_ids = sorted([result["id"] for result in results])
    assert fixture_ids == response_ids


@pytest.mark.django_db
def test_user_shipment_detail(
    auth_api_client: APIClient, user_shipments: list[UserShipment]
) -> None:
    url = reverse("usershipment-detail", args=[user_shipments[0].id])
    response = auth_api_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.data.get("status") == user_shipments[0].status


@pytest.mark.django_db
def test_get_user_shipment_detail_not_owned(
    auth_api_client: APIClient, admin_user_shipments: list[UserShipment]
) -> None:
    url = reverse("usershipment-detail", args=[admin_user_shipments[0].id])
    response = auth_api_client.get(url)

    assert response.status_code == 403
    assert isinstance(response.data, dict)
    assert (
        response.data.get("detail")
        == "You do not have permission to perform this action."
    )


@pytest.mark.django_db
def test_user_shipment_post_without_permissions(
    auth_api_client: APIClient,
) -> None:
    url = reverse("usershipment-list")
    response = auth_api_client.post(url)

    assert response.status_code == 403
    assert isinstance(response.data, dict)
    assert (
        response.data.get("detail")
        == "You do not have permission to perform this action."
    )


@pytest.mark.django_db
def test_user_shipment_post_with_permissions(
    auth_api_client_superuser: APIClient,
    prepared_user_shipment: dict[str, Any],
) -> None:
    url = reverse("usershipment-list")
    response = auth_api_client_superuser.post(url, prepared_user_shipment)

    assert response.status_code == 201
    assert isinstance(response.data, dict)
    assert (
        response.data.get("tracking_number")
        == prepared_user_shipment["tracking_number"]
    )


@pytest.mark.django_db
def test_edit_own_shipment_no_permissions(
    auth_api_client: APIClient, user_shipments: list[UserShipment]
) -> None:
    url = reverse("usershipment-detail", args=[user_shipments[0].id])
    response = auth_api_client.put(url)

    assert response.status_code == 403
    assert isinstance(response.data, dict)
    assert (
        response.data.get("detail")
        == "You do not have permission to perform this action."
    )


@pytest.mark.django_db
def test_edit_shipment_with_permissions(
    auth_api_client_superuser: APIClient, user_shipments: list[UserShipment]
) -> None:
    url = reverse("usershipment-detail", args=[user_shipments[0].id])
    response = auth_api_client_superuser.patch(
        url, {"tracking_number": "QWER1234"}
    )

    assert response.status_code == 200
    assert isinstance(response.data, dict)
    assert response.data.get("tracking_number") == "QWER1234"


@pytest.mark.django_db
def test_delete_own_shipment_no_permissions(
    auth_api_client: APIClient, user_shipments: list[UserShipment]
) -> None:
    url = reverse("usershipment-detail", args=[user_shipments[0].id])
    response = auth_api_client.delete(url)

    assert response.status_code == 403
    assert isinstance(response.data, dict)
    assert (
        response.data.get("detail")
        == "You do not have permission to perform this action."
    )


@pytest.mark.django_db
def test_delete_shipment_with_permissions(
    auth_api_client_superuser: APIClient, user_shipments: list[UserShipment]
) -> None:
    url = reverse("usershipment-detail", args=[user_shipments[0].id])
    response = auth_api_client_superuser.delete(url)

    assert response.status_code == 204
    assert response.data is None
