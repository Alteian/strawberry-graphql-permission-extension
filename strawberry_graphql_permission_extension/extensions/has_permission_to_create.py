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
    """
    Extension class that checks if the user has permission to create an object.

    Example Usage:
        class MyModel(models.Model):
            CREATE_ALLOWED_ROLES = [IsUser]

            # ...

        In this example, the MyModel class defines a list of CREATE_ALLOWED_ROLES, which consists
        of subclasses of Role (such as IsUser) that implement the has_permission method.

    Attributes:
        DEFAULT_ERROR_MESSAGE (str): Default error message displayed when the user doesn't have permission.
        SCHEMA_DIRECTIVE_DESCRIPTION (str): Description of the schema directive.

    Methods:
        __init__(self, model: "models.Model", **kwargs: typing.Any):
            Initializes the HasPermissionToCreate extension with the specified model.

        resolve_for_user(
            self,
            resolver: typing.Callable,
            user: UserType,
            *,
            info: Info,
            source: typing.Any,
            **kwargs: typing.Any
        ):
            Resolves the permission check for the user by invoking has_permission_to_create_object.

    """

    DEFAULT_ERROR_MESSAGE: typing.ClassVar[str] = _(
        "You are not authorized to create this object"
    )
    SCHEMA_DIRECTIVE_DESCRIPTION: typing.ClassVar[str] = _desc(
        _("Can only create objects that the user has permission to create")
    )

    def __init__(self, model: "models.Model", **kwargs: typing.Any):
        """
        Initializes the HasPermissionToCreate extension with the specified model.

        Args:
            model (models.Model): The model for which the permission is being checked.
            **kwargs (typing.Any): Additional keyword arguments.

        """
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
        """
        Resolves the permission check for the user by invoking has_permission_to_create_object.

        Args:
            resolver (typing.Callable): Resolver function for the field.
            user (UserType): The user for whom the permission is being checked.
            info (Info): Additional information related to the permission check.
            source (typing.Any): The source object from which the field is being resolved.
            **kwargs (typing.Any): Additional keyword arguments.

        Returns:
            typing.Any: The result of the resolver function.

        Raises:
            DjangoNoPermission: If the user doesn't have permission to create the object.

        """
        if has_permission_to_create_object(self.model, info):
            return resolver()
        else:
            raise DjangoNoPermission(self.message)
