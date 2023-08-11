from datetime import datetime
from typing import Optional, TypedDict, TypeVar, Literal, Union

# GENERICS

T = TypeVar("T")
HS = TypeVar("HS", bound=str)

# ASSOCIATIONS

Association = TypedDict("Association", {"id": str, "type": str})
HsObjectAssociations = TypedDict("HsObjectAssociations", {"results": list[Association]})
AssociatedHsObject = Literal["companies", "contacts", "deals"]
AssociationCategory = Literal["HUBSPOT_DEFINED", "USER_DEFINED", "INTEGRATOR_DEFINED"]
AssociationType = TypedDict(
    "AssociationType", {"associationCategory": AssociationCategory, "associationTypeId": int}
)
HsPropertyResults = TypedDict("HsPropertyResults", {"results": list[dict[str, str]]})


class HubspotObject(TypedDict):
    id: str
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]
    archived: bool
    associations: dict[AssociatedHsObject, HsObjectAssociations]


# DEALS


class HsDefaultDealProperties(TypedDict):
    hs_object_id: str
    hs_lastmodifieddate: str
    hs_deal_stage_probability: str
    hs_tcv: str
    dealname: str
    dealstage: str
    amount: str
    createdate: str
    description: str
    closedate: str
    pipeline: str


class Deal(HubspotObject):
    properties: HsDefaultDealProperties
    archived_at: Optional[datetime]


# COMPANIES


class HsCompanyProperties(TypedDict):
    name: str
    industry: str
    website: str
    phone: str
    city: str


class Company(HubspotObject):
    properties: HsCompanyProperties


# CONTACTS


class HsContactProperties(TypedDict):
    email: str
    firstname: str
    lastname: str
    company: str
    phone: str
    website: str
    createdate: str
    lastmodifieddate: str


class Contact(HubspotObject):
    properties: HsContactProperties


# SEARCH AND LIST OBJECTS

OBJ = TypeVar("OBJ", bound=HubspotObject)

SearchOperators = Literal[
    "EQ",
    "NEQ",
    "LT",
    "LTE",
    "GT",
    "GTE",
    "BETWEEN",
    "IN",
    "NOT_IN",
    "HAS_PROPERTY",
    "CONTAINS_TOKEN",
    "NOT_CONTAINS_TOKEN",
]


class HsSearchFilters(TypedDict):
    value: str
    values: list[str]
    propertyName: str
    operator: SearchOperators


class HsSearchRequest(TypedDict):
    filters: HsSearchFilters
    sorts: str
    query: str
    properties: list[str]
    limit: int
    after: int


ListResponseNextPage = TypedDict("ListResponseNextPage", {"after": str, "link": str})
ListResponsePaging = TypedDict("ListResponsePaging", {"next": ListResponseNextPage})
ListResponse = TypedDict("ListResponse", {"results": list[OBJ], "paging": ListResponsePaging})


class SearchResults(ListResponse[OBJ]):
    total: int


# HELPER FUNCTIONS


def create_search_filter(
    property_name: str, operator: SearchOperators, value: Union[str, list[str]]
) -> HsSearchFilters:
    value_key = "values" if isinstance(value, list) else "value"
    search_filters: HsSearchFilters = {
        "propertyName": property_name,
        "operator": operator,
        value_key: value,  # type:ignore
    }
    return search_filters
