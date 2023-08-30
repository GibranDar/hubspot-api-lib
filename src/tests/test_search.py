import pytest
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from hubspotapilib.deals import search_deals
from hubspotapilib.schemas import HsSearchRequest, HsSearchFilters, HsSearchFilterQuery


def test_search_deals_request():
    filter_queries = [
        HsSearchFilterQuery(propertyName="dealstage", operator="NEQ", value="closedlost"),
    ]
    filter_groups = [HsSearchFilters(filters=filter_queries)]
    request = HsSearchRequest(
        filter_groups=filter_groups,
        sorts=["hs_deal_stage_probability"],
        properties=["dealname", "dealstage"],
        limit=10,
    )
    response = search_deals(request)
    print(response["total"])
    for deal in response["results"]:
        assert deal["properties"]["dealstage"] != "closedlost"


def test_search_deals_in_and_notin():
    filter_queries = [
        HsSearchFilterQuery(propertyName="dealstage", operator="NOT_IN", values=["closedlost", "closedwon"]),
    ]
    filter_groups = [HsSearchFilters(filters=filter_queries)]
    request = HsSearchRequest(
        filter_groups=filter_groups,
        sorts=["hs_deal_stage_probability"],
        properties=["dealname", "dealstage", "hs_deal_stage_probability"],
        limit=10,
    )
    response = search_deals(request)
    print(response["total"])
    for deal in response["results"]:
        assert deal["properties"]["dealstage"] not in ["closedlost", "closedwon"]

    filter_queries = [
        HsSearchFilterQuery(propertyName="dealstage", operator="IN", values=["closedlost", "closedwon"]),
    ]
    filter_groups = [HsSearchFilters(filters=filter_queries)]
    request = HsSearchRequest(
        filter_groups=filter_groups,
        sorts=["hs_deal_stage_probability"],
        properties=["dealname", "dealstage", "hs_deal_stage_probability"],
        limit=10,
    )
    response = search_deals(request)
    print(response["total"])
    for deal in response["results"]:
        assert deal["properties"]["dealstage"] in ["closedlost", "closedwon"]


def test_search_deals_in_notin_fails():
    with pytest.raises(ValueError):
        filter_queries = [
            HsSearchFilterQuery(propertyName="dealstage", operator="NOT_IN", value="closedwon"),
        ]
        filter_groups = [HsSearchFilters(filters=filter_queries)]
        request = HsSearchRequest(
            filter_groups=filter_groups,
            sorts=["hs_deal_stage_probability"],
            properties=["dealname", "dealstage", "hs_deal_stage_probability"],
            limit=10,
        )
        response = search_deals(request)
        pprint(response, indent=2, sort_dicts=False)


def test_search_deals_has_property():
    filter_queries = [
        HsSearchFilterQuery(propertyName="ornd_unit", operator="HAS_PROPERTY"),
    ]
    filter_groups = [HsSearchFilters(filters=filter_queries)]
    request = HsSearchRequest(
        filter_groups=filter_groups,
        sorts=["hs_deal_stage_probability"],
        properties=["dealname", "ornd_unit", "hs_deal_stage_probability"],
        limit=10,
    )
    response = search_deals(request)
    print(response["total"])
    for deal in response["results"]:
        assert deal["properties"]["ornd_unit"] is not None


def test_search_deals_has_property_fails():
    with pytest.raises(ValueError):
        filter_queries = [
            HsSearchFilterQuery(propertyName="dealstage", operator="HAS_PROPERTY", value="closedlost"),
        ]
        filter_groups = [HsSearchFilters(filters=filter_queries)]
        request = HsSearchRequest(
            filter_groups=filter_groups,
            sorts=["hs_deal_stage_probability"],
            properties=["dealname", "dealstage", "hs_deal_stage_probability"],
            limit=10,
        )
        response = search_deals(request)
        pprint(response, indent=2, sort_dicts=False)


def test_search_deals_between():
    filter_queries = [
        HsSearchFilterQuery(
            propertyName="hs_deal_stage_probability", operator="BETWEEN", value="0.0", highValue="0.5"
        )
    ]
    filter_groups = [HsSearchFilters(filters=filter_queries)]
    request = HsSearchRequest(
        filter_groups=filter_groups,
        sorts=["hs_deal_stage_probability"],
        properties=["dealname", "dealstage", "hs_deal_stage_probability"],
        limit=10,
    )
    response = search_deals(request)
    print(response["total"])
    for deal in response["results"]:
        assert 0.0 <= float(deal["properties"]["hs_deal_stage_probability"]) <= 0.5


def test_search_deals_between_fails():
    with pytest.raises(ValueError):
        filter_queries = [
            HsSearchFilterQuery(propertyName="dealstage", operator="BETWEEN", values=["0.0", "0.5"])
        ]
        filter_groups = [HsSearchFilters(filters=filter_queries)]
        request = HsSearchRequest(
            filter_groups=filter_groups,
            sorts=["hs_deal_stage_probability"],
            properties=["dealname", "dealstage", "hs_deal_stage_probability"],
            limit=10,
        )
        response = search_deals(request)
        pprint(response, indent=2, sort_dicts=False)


# TODO test AND and OR logic
