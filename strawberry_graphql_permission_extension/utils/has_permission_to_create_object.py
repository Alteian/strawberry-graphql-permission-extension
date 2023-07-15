from typing import TYPE_CHECKING
from strawberry.types import Info

if TYPE_CHECKING:
    from django.db import models


@staticmethod
def has_permission_to_create_object(model: "models.Model", info: Info) -> bool:
    """
    Checks if the current user has permission to create an object of the specified model.

    Args:
        model (models.Model): The model class for which the permission is being checked.
        info (strawberry.types.Info): Additional information related to the permission check.

    Returns:
        bool: True if the user has permission to create the object, False otherwise.

    Raises:
        NotImplementedError: If the model does not implement the `CREATE_ALLOWED_ROLES` attribute.

    """
    if hasattr(model, "CREATE_ALLOWED_ROLES"):
        return any(
            [role.has_permission(info) for role in model.CREATE_ALLOWED_ROLES]
        )
    raise NotImplementedError(
        f"CREATE_ALLOWED_ROLES not implemented for {model.__name__}"
    )
