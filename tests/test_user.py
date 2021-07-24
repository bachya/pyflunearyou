"""Define tests for the user report endpoints."""
from aiocache import SimpleMemoryCache
import aiohttp
import pytest

from pyflunearyou import Client
from pyflunearyou.helpers.report import CACHE_KEY_LOCAL_DATA, CACHE_KEY_STATE_DATA

from .common import (
    TEST_LATITUDE,
    TEST_LATITUDE_UNCONTAINED,
    TEST_LONGITUDE,
    TEST_LONGITUDE_UNCONTAINED,
    TEST_ZIP,
    load_fixture,
)


@pytest.mark.asyncio
async def test_no_explicit_client_session(aresponses):
    """Test not providing an explicit aiohttp ClientSession."""
    cache = SimpleMemoryCache()
    await cache.delete(CACHE_KEY_LOCAL_DATA)
    await cache.delete(CACHE_KEY_STATE_DATA)

    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(
            text=load_fixture("user_report_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(
            text=load_fixture("states_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    client = Client()
    info = await client.user_reports.status_by_coordinates(
        TEST_LATITUDE, TEST_LONGITUDE
    )
    assert info == {
        "local": {
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
            "icon": "1",
        },
        "state": {
            "name": "California",
            "place_id": "204",
            "lat": "37.250198",
            "lon": "-119.750298",
            "data": {
                "symptoms_percentage": 12.32,
                "none_percentage": 87.68,
                "ili_percentage": 2.69,
                "lepto_percentage": 0,
                "dengue_percentage": 2.17,
                "chick_percentage": 0,
                "level": 3,
                "overlay_color": "#00B7B6",
                "total_surveys": 2119,
                "symptoms": 261,
                "no_symptoms": 1858,
                "ili": 57,
                "lepto": 0,
                "dengue": 46,
                "chick": 0,
            },
            "last_week_data": {
                "symptoms_percentage": 14.29,
                "none_percentage": 85.71,
                "ili_percentage": 2.91,
                "lepto_percentage": 0.05,
                "dengue_percentage": 2.21,
                "chick_percentage": 0,
                "level": 3,
                "overlay_color": "#00B7B6",
                "total_surveys": 2128,
                "symptoms": 304,
                "no_symptoms": 1824,
                "ili": 62,
                "lepto": 1,
                "dengue": 47,
                "chick": 0,
            },
        },
    }


@pytest.mark.asyncio
async def test_status_by_coordinates_success_id(aresponses):
    """Test getting user reports by latitude/longitude (contained ID)."""
    cache = SimpleMemoryCache()
    await cache.delete(CACHE_KEY_LOCAL_DATA)
    await cache.delete(CACHE_KEY_STATE_DATA)

    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(
            text=load_fixture("user_report_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(
            text=load_fixture("states_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        info = await client.user_reports.status_by_coordinates(
            TEST_LATITUDE, TEST_LONGITUDE
        )
        assert info == {
            "local": {
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
                "icon": "1",
            },
            "state": {
                "name": "California",
                "place_id": "204",
                "lat": "37.250198",
                "lon": "-119.750298",
                "data": {
                    "symptoms_percentage": 12.32,
                    "none_percentage": 87.68,
                    "ili_percentage": 2.69,
                    "lepto_percentage": 0,
                    "dengue_percentage": 2.17,
                    "chick_percentage": 0,
                    "level": 3,
                    "overlay_color": "#00B7B6",
                    "total_surveys": 2119,
                    "symptoms": 261,
                    "no_symptoms": 1858,
                    "ili": 57,
                    "lepto": 0,
                    "dengue": 46,
                    "chick": 0,
                },
                "last_week_data": {
                    "symptoms_percentage": 14.29,
                    "none_percentage": 85.71,
                    "ili_percentage": 2.91,
                    "lepto_percentage": 0.05,
                    "dengue_percentage": 2.21,
                    "chick_percentage": 0,
                    "level": 3,
                    "overlay_color": "#00B7B6",
                    "total_surveys": 2128,
                    "symptoms": 304,
                    "no_symptoms": 1824,
                    "ili": 62,
                    "lepto": 1,
                    "dengue": 47,
                    "chick": 0,
                },
            },
        }


@pytest.mark.asyncio
async def test_status_by_coordinates_success_measure(aresponses):
    """Test getting user reports by latitude/longitude (measurement)."""
    cache = SimpleMemoryCache()
    await cache.delete(CACHE_KEY_LOCAL_DATA)
    await cache.delete(CACHE_KEY_STATE_DATA)

    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(
            text=load_fixture("user_report_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(
            text=load_fixture("states_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        info = await client.user_reports.status_by_coordinates(
            TEST_LATITUDE_UNCONTAINED, TEST_LONGITUDE_UNCONTAINED
        )
        assert info == {
            "local": {
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
                "icon": "1",
            },
            "state": {
                "name": "California",
                "place_id": "204",
                "lat": "37.250198",
                "lon": "-119.750298",
                "data": {
                    "symptoms_percentage": 12.32,
                    "none_percentage": 87.68,
                    "ili_percentage": 2.69,
                    "lepto_percentage": 0,
                    "dengue_percentage": 2.17,
                    "chick_percentage": 0,
                    "level": 3,
                    "overlay_color": "#00B7B6",
                    "total_surveys": 2119,
                    "symptoms": 261,
                    "no_symptoms": 1858,
                    "ili": 57,
                    "lepto": 0,
                    "dengue": 46,
                    "chick": 0,
                },
                "last_week_data": {
                    "symptoms_percentage": 14.29,
                    "none_percentage": 85.71,
                    "ili_percentage": 2.91,
                    "lepto_percentage": 0.05,
                    "dengue_percentage": 2.21,
                    "chick_percentage": 0,
                    "level": 3,
                    "overlay_color": "#00B7B6",
                    "total_surveys": 2128,
                    "symptoms": 304,
                    "no_symptoms": 1824,
                    "ili": 62,
                    "lepto": 1,
                    "dengue": 47,
                    "chick": 0,
                },
            },
        }


@pytest.mark.asyncio
async def test_status_by_zip_success(aresponses):
    """Test getting user reports by ZIP code."""
    cache = SimpleMemoryCache()
    await cache.delete(CACHE_KEY_LOCAL_DATA)
    await cache.delete(CACHE_KEY_STATE_DATA)

    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(
            text=load_fixture("user_report_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(
            text=load_fixture("states_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        info = await client.user_reports.status_by_zip(TEST_ZIP)
        assert info == {
            "local": {
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
                "icon": "1",
            },
            "state": {
                "name": "California",
                "place_id": "204",
                "lat": "37.250198",
                "lon": "-119.750298",
                "data": {
                    "symptoms_percentage": 12.32,
                    "none_percentage": 87.68,
                    "ili_percentage": 2.69,
                    "lepto_percentage": 0,
                    "dengue_percentage": 2.17,
                    "chick_percentage": 0,
                    "level": 3,
                    "overlay_color": "#00B7B6",
                    "total_surveys": 2119,
                    "symptoms": 261,
                    "no_symptoms": 1858,
                    "ili": 57,
                    "lepto": 0,
                    "dengue": 46,
                    "chick": 0,
                },
                "last_week_data": {
                    "symptoms_percentage": 14.29,
                    "none_percentage": 85.71,
                    "ili_percentage": 2.91,
                    "lepto_percentage": 0.05,
                    "dengue_percentage": 2.21,
                    "chick_percentage": 0,
                    "level": 3,
                    "overlay_color": "#00B7B6",
                    "total_surveys": 2128,
                    "symptoms": 304,
                    "no_symptoms": 1824,
                    "ili": 62,
                    "lepto": 1,
                    "dengue": 47,
                    "chick": 0,
                },
            },
        }


@pytest.mark.asyncio
async def test_status_by_zip_failure(aresponses):
    """Test getting user reports by ZIP code."""
    cache = SimpleMemoryCache()
    await cache.delete(CACHE_KEY_LOCAL_DATA)
    await cache.delete(CACHE_KEY_STATE_DATA)

    aresponses.add(
        "api.v2.flunearyou.org",
        "/map/markers",
        "get",
        aresponses.Response(
            text=load_fixture("user_report_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.v2.flunearyou.org",
        "/states",
        "get",
        aresponses.Response(
            text=load_fixture("states_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        info = await client.user_reports.status_by_zip("00000")
        assert info == {}
