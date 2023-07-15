import typing

from typing import TypeAlias, Union
from collections import defaultdict

from strawberry.types import Info
from strawberry_django.permissions import DjangoNoPermission, _desc
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from .base_extension import BasePermissionExtension
from ..utils import get_global_id_objects_from_kwargs

UserType: TypeAlias = Union["AbstractBaseUser", "AnonymousUser"]


class HasPermissionToInteract(BasePermissionExtension):
    """
    Extension class that checks if the user has permission to interact with the specified object(s).

    Example Usage:
        class MyModel(models.Model):
            OWNER_FIELD = BaseOwnerFieldEnum.USER.value <-- This is the field that stores the owner of the object

            @property
            def OWNER_FIELD(self):
                return self.created_by

        To use this extension, create a subclass of HasPermissionToInteract and implement the
        resolve_for_user method, calling check_obj_permissions for the relevant object(s) that
        the user intends to interact with.

    Attributes:
        DEFAULT_ERROR_MESSAGE (str): Default error message displayed when the user doesn't have permission.
        SCHEMA_DIRECTIVE_DESCRIPTION (str): Description of the schema directive.

    Methods:
        resolve_for_user(
            self,
            resolver: typing.Callable,
            user: UserType,
            *,
            info: Info,
            source: typing.Any,
            **kwargs: typing.Any
        ):
            Resolves the permission check for the user by invoking check_obj_permissions for the relevant objects.

    """

    DEFAULT_ERROR_MESSAGE: typing.ClassVar[str] = _(
        "You are not authorized to interact with this object"
    )
    SCHEMA_DIRECTIVE_DESCRIPTION: typing.ClassVar[str] = _desc(
        _(
            "Can only interact with objects that the user has permission to interact with"
        )
    )

    def resolve_for_user(
        self,
        resolver: typing.Callable,
        user: UserType,
        *,
        info: Info,
        source: typing.Any,
        permission_case_switcher: typing.Callable,
        **kwargs: typing.Any
    ):
        """
        Resolves the permission check for the user by invoking check_obj_permissions for the relevant objects.

        Args:
            resolver (typing.Callable): Resolver function for the field.
            user (UserType): The user for whom the permission is being checked.
            info (Info): Additional information related to the permission check.
            source (typing.Any): The source object from which the field is being resolved.
            **kwargs (typing.Any): Additional keyword arguments.

        Returns:
            typing.Any: The result of the resolver function.

        Raises:
            DjangoNoPermission: If the user doesn't have permission to interact with the object(s).

        """
        object_list = get_global_id_objects_from_kwargs(kwargs, [])
        model_map = defaultdict(list)
        for obj in object_list:
            model_name = obj.resolve_type(info)._django_type.model
            model_map[model_name].append(obj.node_id)
        objects = []
        for model, ids in model_map.items():
            # FIXME: optimize to only fetch required fields for permission check, probably owner field and id
            objects.extend(model.objects.filter(pk__in=ids))
        result = all(
            [
                permission_case_switcher.check_obj_permissions(info, instance)
                for instance in objects
            ]
        )
        if not result:
            raise DjangoNoPermission
        return resolver()
