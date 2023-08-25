import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.properties import read_all_properties_in_group
from hubspotapilib.deals import batch_read_deals


@pytest.fixture
def deal_ids() -> list[str]:
    return ["8637226475", "8637226478", "8636983011", "8636983010"]


@pytest.fixture
def properties() -> list[str]:
    group_property_info = read_all_properties_in_group("deals", "re-defined")
    properties = [prop["name"] for prop in group_property_info]
    return properties


def test_batch_read_deals(deal_ids, properties):
    response = batch_read_deals(deal_ids, properties)
    pprint(response, indent=2, sort_dicts=False)
