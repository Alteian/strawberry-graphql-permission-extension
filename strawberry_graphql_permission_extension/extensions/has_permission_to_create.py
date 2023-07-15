import typing
from typing import TypeAlias, Union

from strawberry.types import Info
from django.utils.translation import gettext_lazy as _
from strawberry_django.permissions import DjangoNoPermission, _desc

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db import models
    from django.contrib.auth.models import AbstractBaseUser, AnonymousUser


from .base_extension import BasePermissionExtension
from ..utils import has_permission_to_create_object

UserType: TypeAlias = Union["AbstractBaseUser", "AnonymousUser"]


class HasPermissionToCreate(BasePermissionExtension):
    DEFAULT_ERROR_MESSAGE: typing.ClassVar[str] = _(
        "You are not authorized to create this object"
    )
    SCHEMA_DIRECTIVE_DESCRIPTION: typing.ClassVar[str] = _desc(
        _("Can only create objects that the user has permission to create")
    )

    def __init__(self, model: "models.Model", **kwargs: typing.Any):
        super().__init__(**kwargs)
        self.model = model

    def resolve_for_user(
        self,
        resolver: typing.Callable,
        user: UserType,
        *,
        info: Info,
        source: typing.Any,
        **kwargs: typing.Any
    ):
        if has_permission_to_create_object(self.model, info):
            return resolver()
        else:
            raise DjangoNoPermission(self.message)
