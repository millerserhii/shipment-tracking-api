# mypy: disable-error-code=union-attr
import logging

from django.db import models
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.views import APIView


logger = logging.getLogger("main")


class CustomDjangoModelPermissions(  # type: ignore[misc]
    DjangoModelPermissions
):
    view_permissions: list[str] = ["%(app_label)s.view_%(model_name)s"]
    perms_map: dict[str, list[str]] = {
        "GET": view_permissions,
        "OPTIONS": view_permissions,
        "HEAD": view_permissions,
        "POST": DjangoModelPermissions.perms_map["POST"],
        "PUT": DjangoModelPermissions.perms_map["PUT"],
        "PATCH": DjangoModelPermissions.perms_map["PATCH"],
        "DELETE": DjangoModelPermissions.perms_map["DELETE"],
    }


class AllowObjOwner(BasePermission):  # type: ignore[misc]
    """
    Custom permission class to allow access only to the owners
    of an object.

    Attributes:
        owner_field (str): The name of the field on the object that
        indicates ownership.
    """

    owner_field: str = "user"

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method == "POST":
            owner_field_value = str(request.data.get(self.owner_field))
            user_id = str(request.user.pk)
            if owner_field_value == user_id:
                return True
            model = view.queryset.model  # type: ignore[attr-defined]
            required_perms = get_required_permissions(request.method, model)
            if not request.user.has_perms(required_perms):
                return False
        return request.user.is_authenticated

    def has_object_permission(
        self, request: Request, view: APIView, obj: type[models.Model]
    ) -> bool:
        required_permissions = get_required_permissions(
            request.method, obj  # type: ignore[arg-type]
        )
        has_perms = request.user.has_perms(required_permissions)
        if (
            hasattr(obj, self.owner_field)
            and hasattr(request, "user")
            and not has_perms
        ):
            try:
                owner = getattr(obj, self.owner_field)
                return owner == request.user
            except AttributeError:
                logger.error(
                    "Object %s does not have field %s",
                    obj,
                    self.owner_field,
                )
        return has_perms


class AllowObjOwnerReadOnly(AllowObjOwner):  # type: ignore[misc]
    def has_object_permission(
        self, request: Request, view: APIView, obj: type[models.Model]
    ) -> bool:
        required_permissions = get_required_permissions(
            request.method, obj  # type: ignore[arg-type]
        )
        has_perms = request.user.has_perms(required_permissions)
        if (
            hasattr(obj, self.owner_field)
            and hasattr(request, "user")
            and not has_perms
            and request.method in ["GET", "OPTIONS", "HEAD"]
        ):
            try:
                owner = getattr(obj, self.owner_field)
                return owner == request.user
            except AttributeError:
                logger.error(
                    "Object %s does not have field %s",
                    obj,
                    self.owner_field,
                )
        return has_perms


class IsSuperuserOrReadOnly(BasePermission):  # type: ignore[misc]
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in ["GET", "OPTIONS", "HEAD"]:
            return True
        return bool(
            request.user
            and request.user.is_superuser  # type: ignore[union-attr]
        )


def get_required_permissions(
    method: str, model: type[models.Model]
) -> list[str]:
    if method == "GET":
        return [f"{model._meta.app_label}.view_{model._meta.model_name}"]
    if method == "POST":
        return [f"{model._meta.app_label}.add_{model._meta.model_name}"]
    if method in ["PUT", "PATCH"]:
        return [f"{model._meta.app_label}.change_{model._meta.model_name}"]
    if method == "DELETE":
        return [f"{model._meta.app_label}.delete_{model._meta.model_name}"]
    return []
