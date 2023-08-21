import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.properties import (
    read_all_properties,
    read_single_property_group,
    read_all_properties_in_group,
)


def test_read_all_properties():
    props = read_all_properties("deals")
    results = props.get("results")
    assert results
    assert len(results) > 0


def test_read_a_property_group():
    group = read_single_property_group("deals", "RE-DEFINED")
    assert group["label"] == "RE-DEFINED"
    assert group["name"] == "re-defined"


def test_get_all_group_properties():
    group_props = read_all_properties_in_group("deals", "re-defined")
    pprint(group_props, indent=2, sort_dicts=False)
