import requests
import json
import os

from hubspotapilib.schemas import AssociationName, HsSearchTextQuery


def query(obj_type: AssociationName, request: HsSearchTextQuery):
    """
    Basic text query that searches the the following properties for each object and returns matches:
    - Deals: dealname, pipeline, dealstage, description, dealtype
    - Companies: website, phone, name, domain
    - Contacts: firstname, lastname, email, phone, hs_additional_emails, fax, mobilephone, company, hs_marketable_until_renewal
    """

    url = f"https://api.hubapi.com/crm/v3/objects/{obj_type}/search"
    headers = {"content-type": "application/json", "authorization": f"Bearer {os.getenv('HUBSPOT_API_KEY')}"}
    payload = json.dumps({"query": request.query, "limit": request.limit, "after": request.after})
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()
