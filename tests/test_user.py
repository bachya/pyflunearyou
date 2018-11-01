"""Define tests for the user report endpoints."""
import json

import aiohttp
import pytest

from pyflunearyou import create_client

from .const import TEST_LATITUDE, TEST_LONGITUDE, TEST_ZIP
from .fixtures.user import fixture_user_report_json


@pytest.mark.asyncio
async def test_status(aresponses, event_loop, fixture_user_report_json):
    """Test getting user reports by latitude/longitude."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await create_client(TEST_LATITUDE, TEST_LONGITUDE, websession)
        info = await client.user_reports.status()

        assert info == {
            "id": 2,
            "city": "Los Angeles(90046)",
            "place_id": "23818",
            "zip": "90046",
            "contained_by": "204",
            "latitude": "34.114731",
            "longitude": "-118.363724",
            "none": 2,
            "symptoms": 0,
            "flu": 0,
            "lepto": 0,
            "dengue": 0,
            "chick": 0,
            "icon": "1"
        }


@pytest.mark.asyncio
async def test_status_by_zip_success(
        aresponses, event_loop, fixture_user_report_json):
    """Test getting user reports by ZIP code."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await create_client(TEST_LATITUDE, TEST_LONGITUDE, websession)
        info = await client.user_reports.status_by_zip(TEST_ZIP)

        assert info == {
            "id": 3,
            "city": "Corvallis(97330)",
            "place_id": "21462",
            "zip": "97330",
            "contained_by": "239",
            "latitude": "44.638504",
            "longitude": "-123.292938",
            "none": 3,
            "symptoms": 0,
            "flu": 0,
            "lepto": 0,
            "dengue": 0,
            "chick": 0,
            "icon": "1"
        }


@pytest.mark.asyncio
async def test_status_by_zip_failure(
        aresponses, event_loop, fixture_user_report_json):
    """Test getting user reports by ZIP code."""
    aresponses.add(
        'api.v2.flunearyou.org', '/map/markers', 'get',
        aresponses.Response(
            text=json.dumps(fixture_user_report_json), status=200))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await create_client(TEST_LATITUDE, TEST_LONGITUDE, websession)
        info = await client.user_reports.status_by_zip('00000')

        assert info == {}
