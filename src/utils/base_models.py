import uuid
from typing import Any

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class BaseManager(models.Manager["Base"]):
    """
    Base Manager for Base model
    returns all items which are not trashed
    """

    def get_queryset(self) -> models.QuerySet["Base"]:
        return super().get_queryset().filter(trashed=False)


class Base(models.Model):
    """
    Base parent model for all the models
    Includes timestamp for each create or update operation
    Includes trashed field for soft delete
    """

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    timestamp = models.DateTimeField(blank=True, db_index=True)
    trashed = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()
    # bare_objects is used to get all the objects including trashed ones
    bare_objects: Any = models.Manager()

    # Purely for mypy type checking
    Serializer: Any = None

    class Meta:
        abstract = True

    def __enter__(self) -> "Base":
        self.refresh_from_db()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is None:
            self.full_clean()
            self.save()

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.timestamp:
            self.timestamp = timezone.now()

        update_timestamp = kwargs.pop("update_timestamp", False)
        if update_timestamp:
            self.timestamp = timezone.now()

        super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        self._forced_delete = kwargs.pop(  # pylint: disable=attribute-defined-outside-init,line-too-long   # noqa
            "forced", False
        )
        if self._forced_delete:
            return super().delete(*args, **kwargs)
        self.trashed = True
        self.save(update_timestamp=True)
        return 1, {"backend.Base": 1}


class BaseHistory(Base):
    """
    Base parent model for all the models
    Includes timestamp for each create or update operation
    Includes trashed field for soft delete
    """

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
