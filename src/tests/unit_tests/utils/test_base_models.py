from unittest.mock import patch

from django.utils import timezone

from .conftest import ConcreteBase


def test_save_sets_timestamp(base_instance: ConcreteBase) -> None:
    """Test that the save method sets the timestamp properly."""
    # Initial state
    base_instance.timestamp = None
    with patch("django.db.models.Model.save", return_value=None):
        base_instance.save()

    assert base_instance.timestamp is not None


def test_save_update_timestamp(base_instance: ConcreteBase) -> None:
    """
    Test that the save method updates the timestamp
    if update_timestamp is True.
    """
    # Initial state
    old_timestamp = timezone.now()
    base_instance.timestamp = old_timestamp

    with patch("django.db.models.Model.save", return_value=None):
        base_instance.save(update_timestamp=True)

    assert base_instance.timestamp > old_timestamp


def test_delete_soft(base_instance: ConcreteBase) -> None:
    """
    Test that the delete method sets the
    trashed field and updates the timestamp.
    """
    # Initial state
    base_instance.trashed = False
    base_instance.timestamp = timezone.now()
    initial_timestamp = base_instance.timestamp

    # Mock the return value of save and delete methods
    with patch("django.db.models.Model.save", return_value=None), patch(
        "django.db.models.Model.delete",
        return_value=(1, {"utils.ConcreteBase": 1}),
    ):
        count, _ = base_instance.delete()

    assert base_instance.trashed is True
    assert base_instance.timestamp > initial_timestamp
    assert count == 1


def test_delete_forced(base_instance: ConcreteBase) -> None:
    """Test that the forced delete method actually deletes the instance."""
    # Mock the return value of delete method
    with patch(
        "django.db.models.Model.delete",
        return_value=(1, {"utils.ConcreteBase": 1}),
    ):
        count, details = base_instance.delete(forced=True)

    assert count == 1
    assert details == {"utils.ConcreteBase": 1}
