import typing
import functools

from asgiref.sync import sync_to_async
from strawberry.types import Info
from strawberry.utils.await_maybe import await_maybe
from strawberry_django.permissions import (
    DjangoPermissionExtension,
    DjangoNoPermission,
)
from strawberry_django.resolvers import django_resolver
from strawberry.extensions.field_extension import (
    AsyncExtensionResolver,
    SyncExtensionResolver,
)


class BasePermissionExtension(DjangoPermissionExtension):
    @django_resolver(qs_hook=None)
    def resolve(
        self,
        next_: SyncExtensionResolver,
        source: typing.Any,
        info: Info,
        **kwargs: typing.Dict[str, typing.Any],
    ) -> typing.Any:
        user = info.context.user

        user.is_anonymous  # noqa: B018

        try:
            retval = self.resolve_for_user(
                functools.partial(next_, source, info, **kwargs),
                user,
                info=info,
                source=source,
                **kwargs,
            )
        except DjangoNoPermission as e:
            retval = self.handle_no_permission(e, info=info)

        return retval

    async def resolve_async(
        self,
        next_: AsyncExtensionResolver,
        source: typing.Any,
        info: Info,
        **kwargs: typing.Dict[str, typing.Any],
    ) -> typing.Any:
        user = info.context.user

        # make sure the user is loaded
        await sync_to_async(getattr)(user, "is_anonymous")

        try:
            retval = await await_maybe(
                self.resolve_for_user(
                    functools.partial(next_, source, info, **kwargs),
                    user,
                    info=info,
                    source=source,
                    **kwargs,
                ),
            )
        except DjangoNoPermission as e:
            retval = self.handle_no_permission(e, info=info)

        return retval
