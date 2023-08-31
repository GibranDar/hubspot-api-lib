from datetime import datetime
from typing import Optional, TypedDict, TypeVar, Literal, Union, Any
from attrs import define, field, validators

# GENERICS

T = TypeVar("T")
HS = TypeVar("HS", bound=str)

# ASSOCIATIONS

Association = TypedDict("Association", {"id": str, "type": str})
HsObjectAssociationResults = TypedDict("HsObjectAssociationResults", {"results": list[Association]})
AssociationName = Literal["companies", "contacts", "deals"]
AssociationCategory = Literal["HUBSPOT_DEFINED", "USER_DEFINED", "INTEGRATOR_DEFINED"]
AssociationType = TypedDict(
    "AssociationType", {"associationCategory": AssociationCategory, "associationTypeId": int}
)


class HsPropertyResults(TypedDict):
    results: list[dict]


class HsPropertyGroup(TypedDict):
    archived: bool
    display_order: int
    label: str
    name: str


class HubspotObject(TypedDict):
    id: str
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]
    archived: bool
    associations: dict[AssociationName, HsObjectAssociationResults]


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
    "NOT_HAS_PROPERTY",
    "CONTAINS_TOKEN",  # token categorised as a whole word, does not partial match
    "NOT_CONTAINS_TOKEN",
]


def validate_search_value(instance, attribute, value):
    """Validate that only one of value, highValue, or values is set."""

    if instance.operator in ["IN", "NOT_IN"]:
        if instance.values is None:
            raise ValueError("If operator is 'IN' or 'NOT_IN', then 'values' must be set.")

    if instance.operator in ["HAS_PROPERTY", "NOT_HAS_PROPERTY"]:
        if (instance.values != None) or (instance.value != None) or (instance.highValue != None):
            raise ValueError(
                "If operator is 'HAS_PROPERTY' or 'NOT_HAS_PROPERTY', then all value fields must be None."
            )

    if instance.operator == "BETWEEN":
        if instance.value is None or instance.highValue is None:
            raise ValueError("If operator is 'BETWEEN', then 'value' and 'highValue' must both be set.")
    else:
        if instance.value is not None and instance.highValue is not None:
            raise ValueError(
                f"If 'value' is set, then 'highValue' should be None. Got value: {instance.value}, highValue: {instance.highValue}"
            )
        if instance.highValue is not None and instance.values is not None:
            raise ValueError(
                f"If 'highValue' is set, then 'values' should be None. Got highValue: {instance.highValue}, values: {instance.values}"
            )
        if instance.values is not None and instance.value is not None:
            raise ValueError(
                f"If 'values' is set, then 'value' should be None. Got value: {instance.value}, values: {instance.values}"
            )


@define(kw_only=True)
class HsSearchFilterQuery:
    propertyName: str
    operator: SearchOperators
    value: Optional[str] = field(default=None, validator=validate_search_value)
    highValue: Optional[str] = field(default=None, validator=validate_search_value)
    values: Optional[list[str]] = field(default=None, validator=validate_search_value)


@define(kw_only=True)
class HsSearchFilters:
    """Read more https://developers.hubspot.com/docs/api/crm/search#filter-search-results"""

    filters: list[HsSearchFilterQuery] = field(factory=list, validator=validators.max_len(3))


@define(kw_only=True)
class HsSearchTextQuery:
    query: str = field(validator=validators.instance_of(str))
    limit: int = field(default=100, validator=validators.instance_of(int))
    after: int = field(default=0, validator=validators.instance_of(int))


@define(kw_only=True)
class HsSearchRequest:
    filter_groups: list[HsSearchFilters] = field(factory=list, validator=validators.max_len(3))
    sorts: list[str] = field(
        factory=list, validator=validators.deep_iterable(member_validator=validators.instance_of(str))
    )
    properties: list[str] = field(
        validator=validators.deep_iterable(
            iterable_validator=validators.instance_of(list), member_validator=validators.instance_of(str)
        )
    )
    query: Optional[str] = field(default=None, validator=validators.optional(validators.instance_of(str)))
    limit: int = field(default=100, validator=validators.instance_of(int))
    after: int = field(default=0, validator=validators.instance_of(int))


ListResponseNextPage = TypedDict("ListResponseNextPage", {"after": str, "link": Optional[str]})
ListResponsePaging = TypedDict("ListResponsePaging", {"next": ListResponseNextPage})
ListResponse = TypedDict("ListResponse", {"results": list[OBJ], "paging": ListResponsePaging})


class SearchResultsBase(TypedDict, total=False):
    total: int
    results: list[Any]


class SearchResults(SearchResultsBase):
    paging: ListResponsePaging
