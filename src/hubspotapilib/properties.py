from typing import Any, Union

from . import hubspot_client
from .schemas import AssociationName, HsPropertyResults, HsPropertyGroup


def read_all_properties(
    object_type: AssociationName, property: str = "", archived: bool = False
) -> HsPropertyResults[dict[str, Any]]:
    with hubspot_client() as client:
        request: dict[str, Union[str, bool]] = {"object_type": object_type, "archived": archived}
        if property:
            request["property"] = property
        res = client.crm.properties.core_api.get_all(**request)
        return res.to_dict()


def read_all_property_groups(
    object_type: AssociationName, archived: bool = False
) -> HsPropertyResults[HsPropertyGroup]:
    with hubspot_client() as client:
        request: dict[str, Union[str, bool]] = {"object_type": object_type, "archived": archived}
        res = client.crm.properties.groups_api.get_all(**request)
        return res.to_dict()


def read_single_property_group(object_type: AssociationName, group_name: str) -> HsPropertyGroup:
    with hubspot_client() as client:
        request: dict[str, Union[str, bool]] = {"group_name": group_name, "object_type": object_type}
        res = client.crm.properties.groups_api.get_by_name(**request)
        return res.to_dict()


def read_all_properties_in_group(
    object_type: AssociationName, group_name: str, archived: bool = False
) -> list[dict[str, Any]]:
    props = read_all_properties(object_type, archived=archived)
    if results := props.get("results"):
        group_properties = [prop for prop in results if prop["groupName"] == group_name]
        return group_properties
    raise Exception(f"No properties found for group {group_name} in {object_type}")
