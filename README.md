# strawberry-graphql-permission-extension

This repository provides an extension for managing RBAC permissions in Django using Strawberry GraphQL Django.

## Features
- `HasPermissionToInteract`: Extension for checking user permissions to interact with objects.
- `HasPermissionToCreate`: Extension for checking user permissions to create objects.
- `Role`: Base class for defining custom roles.
- `BaseOwnerFieldEnum`: Base class for defining custom cases of ownership of objects.

## Usage

1. Defining custom Roles

```python
from strawberry_graphql_permission_extension.utils import Role

class IsUser:
    @staticmethod
    def has_permission(info) -> bool:
        user = info.context.user
        return user.role == UserRoleChoices.USER
```
2. Implementing `BaseOwnerFieldEnum`
Based on cases of ownership of objects

```python
from strawberry_graphql_permission_extension import BaseOwnerFieldEnum

class OwnerFieldEnum(BaseOwnerFieldEnum):
    USER = "user" <-- link to the user field in the model
    CREATED_BY = "created_by" 
    ORGANIZATION = "organization"
```

3. Creating custom cases for checking permissions

```python
from strawberry_graphql_permission_extension.utils import PermissionCaseSwitcher

def resolve_case_anonymous() -> bool:
    return False

def resolve_case_user(info, instance) -> bool:
    if isinstance(instance, get_user_model()):
        user = instance
    else:
        if field := getattr(instance, "OWNER_FIELD", False):
            user = getattr(instance, field)
    if user and user == info.context.user:
        return True
    return False

class MyPermissionCaseSwitcher(PermissionCaseSwitcher):
    
    def case_anonymous(self) -> bool:
        return resolve_case_anonymous()
    
    def case_user(self, info, instance, case: str) -> bool:
        return resolve_case_user(self.info, self.instance)

    @classmethod
    def resolve_case(cls, info, instance):
        if info.context.user.is_anonymous:
            return cls.case_anonymous()
        elif instance.OWNER_FIELD == OwnerFieldEnum.USER.value:
            return cls.case_user(info, instance, case="user")
        ...
```

4. Declaring permissions on the model

```python
from django.db import models

class MyModel(models.Model):
    OWNER_FIELD = OwnerFieldEnum.USER
    CREATE_ALLOW_ROLES = [IsUser, ...]
    ...
```

5. Using the extenstion
```python
@strawberry.type(extensitons=[HasPermissionToInteract()])
def update_user(self, info, input: UpdateUserInput) -> UpdateUserPayload:
    ...

@strawberry.field(extensitons=[HasPermissionToCreate(Product)])
def create_product(self, info, input: CreateProductInput) -> CreateProductPayload:
    ...
```
