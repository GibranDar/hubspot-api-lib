from typing import Union

from . import hubspot_client
from .schemas import AssociatedHsObject, HsPropertyResults


def real_all_properties(
    object_type: AssociatedHsObject, property: str = "", archived: bool = False
) -> HsPropertyResults:
    with hubspot_client() as client:
        request: dict[str, Union[str, bool]] = {"object_type": object_type, "archived": archived}
        if property:
            request["property"] = property
        res = client.crm.properties.core_api.get_all(**request)
        properties: HsPropertyResults = res.to_dict()
        return properties
