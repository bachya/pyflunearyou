"""Define tests for the CDC endpoints."""
import json

import aiohttp
import pytest

from pyflunearyou import create_client

from .const import TEST_LATITUDE, TEST_LONGITUDE, TEST_ZIP
from .fixtures.cdc import fixture_cdc_report_json
from .fixtures.user import fixture_user_report_json


@pytest.mark.asyncio
async def test_status(
        aresponses, event_loop, fixture_cdc_report_json,
        fixture_user_report_json):
    """Test getting CDC reports by latitude/longitude."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))
    aresponses.add(
        'api.v2.flunearyou.org', '/map/cdc', 'get',
        aresponses.Response(
            text=json.dumps(fixture_cdc_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await create_client(TEST_LATITUDE, TEST_LONGITUDE, websession)
        info = await client.cdc_reports.status()

        assert info == {
            "level": "3",
            "level2": None,
            "week_date": "2018-10-13",
            "name": "California",
            "fill": {
                "color": "#00B7B6",
                "opacity": 0.7
            }
        }


async def test_status_by_state(
        aresponses, event_loop, fixture_cdc_report_json,
        fixture_user_report_json):
    """Test getting CDC reports by state."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))
    aresponses.add(
        'api.v2.flunearyou.org', '/map/cdc', 'get',
        aresponses.Response(
            text=json.dumps(fixture_cdc_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await create_client(TEST_LATITUDE, TEST_LONGITUDE, websession)
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
