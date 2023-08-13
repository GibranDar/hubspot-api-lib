import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.properties import read_all_properties, read_single_property_group


def test_read_all_properties():
    props = read_all_properties("deals")
    results = props.get("results")
    assert results
    assert len(results) > 0


def test_read_a_property_group():
    group = read_single_property_group("deals", "RE-DEFINED")
    assert group["label"] == "RE-DEFINED"
    assert group["name"] == "re-defined"
