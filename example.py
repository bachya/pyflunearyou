"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from pyflunearyou import Client
from pyflunearyou.errors import FluNearYouError

_LOGGER = logging.getLogger()

LATITUDE = 47.6129432
LONGITUDE = -122.4821475
STATE = 'North Dakota'
ZIP_CODE = '98110'


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        try:
            # Create a client:
            client = Client(websession)

            # Get user data for the client's latitude/longitude:
            user_coord_resp = await client.user_reports.status_by_coordinates(
                LATITUDE, LONGITUDE)
            _LOGGER.info(
                'User data by latitude/longitude (%s, %s): %s', LATITUDE,
                LONGITUDE, user_coord_resp)

            # Get user data for the a specific ZIP code:
            user_zip_resp = await client.user_reports.status_by_zip(ZIP_CODE)
            _LOGGER.info(
                'User data by ZIP code (%s): %s', ZIP_CODE, user_zip_resp)

            # Get CDC data for the client's latitude/longitude:
            cdc_coord_resp = await client.cdc_reports.status_by_coordinates(
                LATITUDE, LONGITUDE)
            _LOGGER.info(
                'CDC data by latitude/longitude (%s, %s): %s', LATITUDE,
                LONGITUDE, cdc_coord_resp)

            # Get CDC data for North Dakota
            cdc_state_resp = await client.cdc_reports.status_by_state(STATE)
            _LOGGER.info(
                'CDC data by state name (%s): %s', STATE, cdc_state_resp)
        except FluNearYouError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
