import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.deals import search_deals
from hubspotapilib.schemas import HsSearchRequest, HsSearchFilters, SearchOperators


def test_search_deals_request():
    filters = [
        HsSearchFilters(propertyName="dealstage", operator="NEQ", value="closedlost"),
    ]
    request = HsSearchRequest(
        filters=filters,
        sorts="hs_deal_stage_probability",
        properties=["dealname", "dealstage"],
    )
    response = search_deals([request])
    pprint(response, indent=2, sort_dicts=False)


def test_search_deals_in_and_notin():
    filters = [
        HsSearchFilters(propertyName="dealstage", operator="NOT_IN", values=["closedlost", "closedwon"]),
    ]
    request = HsSearchRequest(
        filters=filters,
        sorts="hs_deal_stage_probability",
        properties=["dealname", "dealstage", "hs_deal_stage_probability"],
    )
    response = search_deals([request])
    pprint(response, indent=2, sort_dicts=False)


def test_search_deals_in_notin_fails():
    with pytest.raises(ValueError):
        filters = [HsSearchFilters(propertyName="dealstage", operator="IN", value="closedlost")]
        request = HsSearchRequest(
            filters=filters,
            sorts="hs_deal_stage_probability",
            properties=["dealname", "dealstage", "hs_deal_stage_probability"],
        )
        search_deals([request])


def test_search_deals_has_property():
    filters = [
        HsSearchFilters(propertyName="ornd_unit", operator="HAS_PROPERTY"),
    ]
    request = HsSearchRequest(
        filters=filters,
        sorts="hs_deal_stage_probability",
        properties=["dealname", "dealstage", "hs_deal_stage_probability"],
    )
    response = search_deals([request])
    pprint(response, indent=2, sort_dicts=False)


def test_search_deals_has_property_fails():
    with pytest.raises(ValueError):
        filters = [
            HsSearchFilters(propertyName="ornd_unit", operator="HAS_PROPERTY", value="closedlost"),
        ]
        request = HsSearchRequest(
            filters=filters,
            sorts="hs_deal_stage_probability",
            properties=["dealname", "dealstage", "hs_deal_stage_probability"],
        )
        search_deals([request])


def test_search_deals_between():
    filters = [
        HsSearchFilters(
            propertyName="hs_deal_stage_probability", operator="BETWEEN", value="0.0", highValue="0.5"
        ),
    ]
    request = HsSearchRequest(
        filters=filters,
        sorts="hs_deal_stage_probability",
        properties=["dealname", "dealstage", "hs_deal_stage_probability"],
    )
    response = search_deals([request])
    pprint(response, indent=2, sort_dicts=False)


def test_search_deals_between_fails():
    with pytest.raises(ValueError):
        filters = [
            HsSearchFilters(
                propertyName="hs_deal_stage_probability", operator="BETWEEN", values=["0.0", "0.5"]
            ),
        ]
        request = HsSearchRequest(
            filters=filters,
            sorts="hs_deal_stage_probability",
            properties=["dealname", "dealstage", "hs_deal_stage_probability"],
        )
        search_deals([request])
