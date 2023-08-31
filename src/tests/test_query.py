import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.schemas import HsSearchTextQuery
from hubspotapilib.query import query


def test_query():
    q = "M"
    request = HsSearchTextQuery(query=q)
    response = query("deals", request)
    pprint(response)
    for deal in response["results"]:
        assert q in deal["properties"]["dealname"].lower()
