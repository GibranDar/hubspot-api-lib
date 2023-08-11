import requests
import json
import os

from .schemas import AssociationType, AssociatedHsObject


def create_association(
    from_obj_type: AssociatedHsObject,
    from_obj_id: str,
    to_obj_type: AssociatedHsObject,
    to_obj_id: str,
    association_ref: AssociationType,
):
    url = f"https://api.hubapi.com/crm/v4/objects/{from_obj_type}/{from_obj_id}/associations/{to_obj_type}/{to_obj_id}"
    payload = json.dumps([association_ref])
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('HUBSPOT_API_KEY')}",
    }
    response = requests.request("PUT", url, data=payload, headers=headers)
    return response.json()


def delete_association(
    from_obj_type: AssociatedHsObject, from_obj_id: str, to_obj_type: AssociatedHsObject, to_obj_id: str
):
    url = f"https://api.hubapi.com/crm/v4/objects/{from_obj_type}/{from_obj_id}/associations/{to_obj_type}/{to_obj_id}"
    headers = {"accept": "application/json", "authorization": f"Bearer {os.getenv('HUBSPOT_API_KEY')}"}
    response = requests.request("DELETE", url, headers=headers)
    return response


def update_object(obj_id: str, object_type: AssociatedHsObject, properties: dict[str, str]):
    url = f"https://api.hubapi.com/crm/v4/objects/{object_type}/{obj_id}"
    payload = json.dumps({"properties": properties})
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('HUBSPOT_API_KEY')}",
    }
    response = requests.request("PATCH", url, data=payload, headers=headers)
    return response.json()
