"""Define tests for the CDC endpoints."""
import json

import aiohttp
import pytest

from pyflunearyou import Client

from .const import TEST_LATITUDE, TEST_LONGITUDE, TEST_ZIP
from .fixtures import fixture_states_json
from .fixtures.cdc import fixture_cdc_report_json


@pytest.mark.asyncio
async def test_status_by_coordinates_success(
        aresponses, event_loop, fixture_cdc_report_json, fixture_states_json):
    """Test getting CDC reports by latitude/longitude."""
    aresponses.add(
        'api.v2.flunearyou.org', '/states', 'get',
        aresponses.Response(text=json.dumps(fixture_states_json), status=200))
    aresponses.add(
        'api.v2.flunearyou.org', '/map/cdc', 'get',
        aresponses.Response(
            text=json.dumps(fixture_cdc_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        info = await client.cdc_reports.status_by_coordinates(
            TEST_LATITUDE, TEST_LONGITUDE)

        assert info == {
            "level": "Low",
            "level2": "None",
            "week_date": "2018-10-13",
            "name": "California",
            "fill": {
                "color": "#00B7B6",
                "opacity": 0.7
            }
        }


async def test_status_by_state_success(
        aresponses, event_loop, fixture_cdc_report_json, fixture_states_json):
    """Test getting CDC reports by state."""
    aresponses.add(
        'api.v2.flunearyou.org', '/states', 'get',
        aresponses.Response(text=json.dumps(fixture_states_json), status=200))
    aresponses.add(
        'api.v2.flunearyou.org', '/map/cdc', 'get',
        aresponses.Response(
            text=json.dumps(fixture_cdc_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        info = await client.cdc_reports.status_by_state('Colorado')

        assert info == {
            "level": "Minimal",
            "level2": "None",
            "week_date": "2018-10-13",
            "name": "Colorado",
            "fill": {
                "color": "#00B7B6",
                "opacity": 0.7
            }
        }


async def test_status_by_state_failure(
        aresponses, event_loop, fixture_cdc_report_json, fixture_states_json):
    """Test getting CDC reports by state."""
    aresponses.add(
        'api.v2.flunearyou.org', '/states', 'get',
        aresponses.Response(text=json.dumps(fixture_states_json), status=200))
    aresponses.add(
        'api.v2.flunearyou.org', '/map/cdc', 'get',
        aresponses.Response(
            text=json.dumps(fixture_cdc_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        info = await client.cdc_reports.status_by_state('Jupiter')

        assert info == {}
