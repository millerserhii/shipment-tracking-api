from typing import Any

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.permissions import AllowObjOwner, CustomDjangoModelPermissions


class BaseUserOwnedViewSet(ModelViewSet):
    permission_classes = [AllowObjOwner]

    def get_list_queryset(self) -> QuerySet[Any]:
        queryset: QuerySet[Any] = super().get_queryset()  # type: ignore[misc]
        user = self.request.user
        if user.has_perms(  # type: ignore[union-attr]
            CustomDjangoModelPermissions.view_permissions
        ):
            return queryset
        return queryset.filter(user=user)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset: QuerySet[Any] = self.filter_queryset(
            self.get_list_queryset()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
