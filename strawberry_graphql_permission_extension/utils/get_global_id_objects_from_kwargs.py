import typing

from strawberry.relay import GlobalID


def get_global_id_objects_from_kwargs(
    d: dict, global_ids: typing.List[GlobalID] = []
) -> typing.List[GlobalID]:
    for value in d.values():
        if isinstance(value, GlobalID):
            global_ids.append(value)
        elif isinstance(value, list) and all(
            isinstance(item, GlobalID) for item in value
        ):
            global_ids.extend(value)
        elif isinstance(value, dict):
            get_global_id_objects_from_kwargs(value, global_ids)
        elif isinstance(value, list) and all(
            isinstance(item, dict) for item in value
        ):
            for item in value:
                get_global_id_objects_from_kwargs(item, global_ids)
    return global_ids
