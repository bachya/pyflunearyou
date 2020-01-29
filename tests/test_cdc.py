"""Define tests for the CDC endpoints."""
import aiohttp
import pytest

from pyflunearyou import Client

from .common import TEST_LATITUDE, TEST_LONGITUDE, load_fixture


@pytest.mark.asyncio
async def test_status_by_coordinates_success(aresponses):
    """Test getting CDC reports by latitude/longitude."""
    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(text=load_fixture("user_report_response.json"), status=200),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(text=load_fixture("states_response.json"), status=200),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/cdc",
        "get",
        aresponses.Response(text=load_fixture("cdc_report_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession)
        info = await client.cdc_reports.status_by_coordinates(
            TEST_LATITUDE, TEST_LONGITUDE
        )
        assert info == {
            "level": "High",
            "level2": "None",
            "week_date": "2018-10-13",
            "name": "California",
            "fill": {"color": "#00B7B6", "opacity": 0.7},
        }


async def test_status_by_state_success(aresponses):
    """Test getting CDC reports by state."""
    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(text=load_fixture("user_report_response.json"), status=200),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(text=load_fixture("states_response.json"), status=200),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/cdc",
        "get",
        aresponses.Response(text=load_fixture("cdc_report_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession)
        info = await client.cdc_reports.status_by_state("Colorado")
        assert info == {
            "level": "Minimal",
            "level2": "None",
            "week_date": "2018-10-13",
            "name": "Colorado",
            "fill": {"color": "#00B7B6", "opacity": 0.7},
        }


async def test_status_by_state_failure(aresponses):
    """Test getting CDC reports by state."""
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(text=load_fixture("states_response.json"), status=200),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/cdc",
        "get",
        aresponses.Response(text=load_fixture("cdc_report_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(websession)
        info = await client.cdc_reports.status_by_state("Jupiter")
        assert info == {}
