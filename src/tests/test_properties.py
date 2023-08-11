import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.properties import real_all_properties


def test_read_all():
    props = real_all_properties("deals")
    results = props.get("results")
    assert results
    assert len(results) > 0
