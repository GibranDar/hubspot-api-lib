import re

from hubspot.crm.deals import SimplePublicObjectInput

from . import hubspot_client
from .schemas import Contact, ListResponse, HubspotObject


def create_contact(properties: dict[str, str]) -> Contact:
    with hubspot_client() as client:
        if email := properties.get("email"):
            website: str = email.split("@")[1]
        simple_pub_obj = SimplePublicObjectInput(properties=dict(**properties, website=website))
        res = client.crm.contacts.basic_api.create(simple_pub_obj)
        contact: Contact = res.to_dict()
        return contact


def read_contact(contact_id: str, properties: list[str] = [], associations: list[str] = []) -> Contact:
    default_properties = ["firstname", "lastname", "email", "phone"]
    if properties:
        default_properties = default_properties + properties
    with hubspot_client() as client:
        res = client.crm.contacts.basic_api.get_by_id(
            contact_id, properties=default_properties, associations=associations
        )
        contact: Contact = res.to_dict()
        return contact


def update_contact(contact_id: str, properties: dict[str, str]) -> Contact:
    with hubspot_client() as client:
        simple_pub_obj = SimplePublicObjectInput(properties=properties)
        res = client.crm.contacts.basic_api.update(contact_id, simple_pub_obj)
        company: Contact = res.to_dict()
        return company


def list_contacts(limit: int = 100, archived: bool = False) -> ListResponse[Contact]:
    default_properties = ["firstname", "lastname", "email"]
    with hubspot_client() as client:
        res = client.crm.contacts.basic_api.get_page(
            limit=limit, archived=archived, properties=default_properties
        )
        contacts: ListResponse[Contact] = res.to_dict()
        return contacts


def search_contacts(email: str) -> list[Contact]:
    contacts = list_contacts().get("results", [])
    matches: list[Contact] = []
    for contact in contacts:
        if re.search(rf"{email}", contact["properties"]["email"], re.IGNORECASE):
            matches.append(contact)
    return matches


def get_or_create_contact(properties: dict[str, str]) -> HubspotObject:
    matches = search_contacts(properties["email"])
    if len(matches) > 0:
        contact = matches[0]
        return contact
    else:
        contact = create_contact(properties)
        return contact
