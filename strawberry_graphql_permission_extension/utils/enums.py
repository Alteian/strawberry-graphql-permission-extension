from enum import Enum


class BaseOwnerFieldEnum(Enum):
    """
    BaseOwnerFieldEnum is an enum that can be used to define the fields that are used to
    identify the owner of a model.

    Example usage:
        class MyOwnerFieldEnum(BaseOwnerFieldEnum):
            CUSTOM_FIELD = "custom_field"

        my_owner_field = MyOwnerFieldEnum.CUSTOM_FIELD.value

    """

    pass
