import re

from hubspot.crm.companies import SimplePublicObjectInput

from . import hubspot_client
from .schemas import Company, ListResponse, HubspotObject



def create_company(properties: dict[str, str]) -> Company:
    with hubspot_client() as client:
        simple_pub_obj = SimplePublicObjectInput(properties=properties)
        res = client.crm.companies.basic_api.create(simple_pub_obj)
        company: Company = res.to_dict()
        return company


def read_company(
    company_id: str, properties: list[str] = [], associations: list[str] = [], archived=False
) -> Company:
    default_properties = ["name", "industry", "website"]
    if properties:
        default_properties = default_properties + properties
    with hubspot_client() as client:
        res = client.crm.companies.basic_api.get_by_id(
            company_id, properties=default_properties, associations=associations, archived=archived
        )
        company: Company = res.to_dict()
        return company


def update_company(company_id: str, properties: dict[str, str]) -> Company:
    with hubspot_client() as client:
        simple_pub_obj = SimplePublicObjectInput(properties=properties)
        res = client.crm.companies.basic_api.update(company_id, simple_pub_obj)
        company: Company = res.to_dict()
        return company


def list_companies(limit: int = 100, archived=False) -> ListResponse[Company]:
    default_properties = ["name", "industry", "website"]
    with hubspot_client() as client:
        res = client.crm.companies.basic_api.get_page(
            limit=limit, archived=archived, properties=default_properties
        )
        companies: ListResponse[Company] = res.to_dict()
        return companies


def search_companies(company_name: str) -> list[Company]:
    companies = list_companies().get("results", [])
    matches: list[Company] = []
    for company in companies:
        if re.search(rf"{company_name}", company["properties"]["name"], re.IGNORECASE):
            matches.append(company)
    return matches


def get_or_create_company(properties: dict[str, str]) -> HubspotObject:
    matches = search_companies(properties["name"])
    if len(matches) > 0:
        company = matches[0]
        return company
    else:
        company = create_company(properties)
        return company
