class Role:
    """
    Base class for defining user roles and their permission logic.

    To define a specific role, subclass the Role class and implement the 'has_permission' method.

    Example:
        class IsUser(Role):
            @staticmethod
            def has_permission(info) -> bool:
                user = info.context.user
                return user.role == UserRoleChoices.USER

        In this example, the IsUser class is a subclass of Role and overrides the has_permission method
        with custom permission logic that checks if the user's role is equal to UserRoleChoices.CUSTOMER.

    Methods:
        has_permission(info):
            Check if the user has the required permission based on the role.
            Override this method in your Role subclass to define custom permission logic.

    Raises:
        NotImplementedError: If the has_permission method is not implemented in the subclass.

    """

    @staticmethod
    def has_permission(info) -> bool:
        """
        Check if the user has the required permission based on the role.

        Args:
            info: Additional information related to the permission check.

        Returns:
            bool: True if the user has the required permission, False otherwise.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError(
            "You must implement the 'has_permission' method in your Role subclass."
        )
