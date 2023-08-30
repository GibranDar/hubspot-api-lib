from pprint import pprint
from typing import Optional
from attrs import asdict

from hubspot.crm.deals import (
    SimplePublicObjectInput,
    PublicObjectSearchRequest,
    BatchReadInputSimplePublicObjectId,
)

from . import hubspot_client
from .associations import create_association
from .companies import read_company
from .contacts import read_contact
from .schemas import (
    Deal,
    Company,
    Contact,
    ListResponse,
    AssociationType,
    AssociationName,
    HsSearchRequest,
    SearchResults,
)

# CRUD


def create_deal(properties: dict[str, str]) -> Deal:
    with hubspot_client() as client:
        simple_pub_obj = SimplePublicObjectInput(properties=properties)
        res = client.crm.deals.basic_api.create(simple_pub_obj)
        deal: Deal = res.to_dict()
        return deal


def read_deal(deal_id: str, properties: list[str] = [], associations: list[AssociationName] = []) -> Deal:
    default_properties = ["dealname", "dealstage", "amount"]
    if properties:
        default_properties = default_properties + properties
    with hubspot_client() as client:
        res = client.crm.deals.basic_api.get_by_id(
            deal_id, properties=default_properties, associations=associations
        )
        deal: Deal = res.to_dict()
        return deal


def update_deal(deal_id: str, properties: dict[str, str]) -> Deal:
    with hubspot_client() as client:
        simple_pub_obj = SimplePublicObjectInput(properties=properties)
        res = client.crm.deals.basic_api.update(deal_id, simple_pub_obj)
        deal: Deal = res.to_dict()
        return deal


def delete_deal(deal_id: str):
    with hubspot_client() as client:
        res = client.crm.deals.basic_api.archive(deal_id=deal_id)
        return res


def list_deals(
    limit: int = 100, properties: list[str] = [], after: Optional[str] = None, archived: bool = False
) -> ListResponse[Deal]:
    with hubspot_client() as client:
        res = client.crm.deals.basic_api.get_page(
            limit=limit, properties=properties, archived=archived, after=after
        )
        deals: ListResponse[Deal] = res.to_dict()
        return deals


def search_deals(request: HsSearchRequest) -> SearchResults:
    with hubspot_client() as client:
        search_obj = asdict(request, recurse=True)
        pprint(search_obj, indent=2, sort_dicts=False)
        res = client.crm.deals.search_api.do_search(
            public_object_search_request=PublicObjectSearchRequest(**search_obj)
        )
        return res.to_dict()


def batch_read_deals(deal_ids: list[str], properties: list[str] = []) -> SearchResults:
    with hubspot_client() as client:
        res = client.crm.deals.batch_api.read(
            batch_read_input_simple_public_object_id=BatchReadInputSimplePublicObjectId(
                inputs=[{"id": id} for id in deal_ids], properties=properties
            )
        )
        return res.to_dict()


def associate_deal_with_company(deal_id: str, to_object_id: str):
    association_ref: AssociationType = {"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 5}
    res = create_association("deals", deal_id, "companies", to_object_id, association_ref)
    return res


def associate_deal_with_contact(deal_id: str, to_object_id: str):
    association_ref: AssociationType = {"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}
    res = create_association("deals", deal_id, "contacts", to_object_id, association_ref)
    return res


def get_deal_to_company(deal: Deal) -> Optional[Company]:
    if deal.get("associations") is None or not deal["associations"].get("companies"):
        return None
    if assocs := deal["associations"].get("companies"):
        for item in assocs["results"]:
            if item["type"] == "deal_to_company":
                company = read_company(item["id"], properties=["name"])
                return company
    return None


def get_deal_to_contact(deal: Deal) -> Optional[Contact]:
    if deal.get("associations") is None or not deal["associations"].get("contacts"):
        return None
    if assocs := deal["associations"].get("contacts"):
        for item in assocs["results"]:
            if item["type"] == "deal_to_contact":
                contact = read_contact(item["id"])
                return contact
    return None
