"""Define fixtures for the user reports endpoint."""
import pytest


@pytest.fixture()
def fixture_user_report_json():
    """Return a subset of a /map/markers response."""
    return [{
        "id": 1,
        "city": "Chester(72934)",
        "place_id": "49377",
        "zip": "72934",
        "contained_by": "610",
        "latitude": "35.687603",
        "longitude": "-94.253845",
        "none": 1,
        "symptoms": 0,
        "flu": 0,
        "lepto": 0,
        "dengue": 0,
        "chick": 0,
        "icon": "1"
    }, {
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
    }, {
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
    }]
