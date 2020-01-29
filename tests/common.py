"""Define common test utilities."""
import os

TEST_LATITUDE = 34.114731
TEST_LONGITUDE = -118.363724
TEST_ZIP = "90046"

TEST_LATITUDE_UNCONTAINED = 44.638504
TEST_LONGITUDE_UNCONTAINED = -123.292938


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
