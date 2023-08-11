import contextlib
import os

import hubspot
from hubspot.crm.deals import ApiException


@contextlib.contextmanager
def hubspot_client():
    try:
        oauth_key = os.getenv(f"HUBSPOT_API_KEY")
        client = hubspot.Client.create(access_token=oauth_key)
        yield client
    except ApiException as e:
        raise Exception(e)
