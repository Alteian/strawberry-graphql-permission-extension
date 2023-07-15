class PermissionCaseSwitcher:
    """
    A switcher class that allows users to define and implement their own case resolvers.

    To use this switcher, subclass the PermissionCaseSwitcher and implement custom case resolvers based on your needs.

    Example:
        class MyPermissionCaseSwitcher(PermissionCaseSwitcher):
            def case_user(self):
                # Custom implementation for the 'user' case
                return self.resolve_user(self.info, self.instance)

        To check object permissions using your custom switcher, call `check_obj_permissions`:

        permissions = check_obj_permissions(info, instance)

    Note:
        - The switcher relies on the naming convention 'case_<case_name>' for the case resolvers.
        - The 'switch' method automatically selects and invokes the appropriate case resolver based on the 'case' attribute.

    Methods:
        switch():
            Invokes the appropriate case resolver based on the 'case' attribute.

    Class Methods:
        resolve_case(info, instance):
            Resolves the case based on the provided information and instance.
            This method is responsible for determining which case resolver to use.
            Override this method in your subclass with custom implementation.

    Subclassing Tips:
        - Create a subclass of PermissionCaseSwitcher.
        - Implement your own case resolvers following the naming convention 'case_<case_name>'.
        - Override the 'resolve_case' class method to determine the case based on the information and instance.
        - You can add additional methods or attributes to your subclass as needed.

    Raises:
        NotImplementedError: If the 'resolve_case' method is not implemented in the subclass.

    """

    def __init__(self, info, instance, case):
        self.info = info
        self.instance = instance
        self.case = case

    def switch(self):
        return getattr(self, f"case_{self.case}")()

    @classmethod
    def resolve_case(cls, info, instance):
        """
        Resolves the case based on the provided information and instance.

        This method is responsible for determining which case resolver to use.
        Override this method in your subclass with custom implementation.

        Args:
            info: Additional information related to the permission check.
            instance: The instance on which the permission is being checked.

        Returns:
            The resolved case.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.

        """
        raise NotImplementedError(
            "You must implement case resolvers and cases"
        )

    @classmethod
    def check_obj_permissions(cls, info, instance):
        return cls.resolve_case(info, instance)
