from . import hubspot_client
from .schemas import AssociatedHsObject, HsPropertyResults


def real_all_properties(object_type: AssociatedHsObject, archived: bool = False) -> HsPropertyResults:
    with hubspot_client() as client:
        res = client.crm.properties.core_api.get_all(object_type, archived=archived)
        properties: HsPropertyResults = res.to_dict()
        return properties
