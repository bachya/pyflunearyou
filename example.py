"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from pyflunearyou import create_client
from pyflunearyou.errors import FluNearYouError

_LOGGER = logging.getLogger()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        try:
            # Create a client:
            client = await create_client(36.0861973, -86.8781167, websession)

            # Get user data for the client's latitude/longitude:
            user_coord_resp = await client.user_reports.status()
            _LOGGER.info(
                'User data by latitude/longitude: %s', user_coord_resp)

            # Get user data for the a specific ZIP code:
            user_zip_resp = await client.user_reports.status_by_zip("90046")
            _LOGGER.info('User data by ZIP code: %s', user_zip_resp)

            # Get CDC data for the client's latitude/longitude:
            cdc_coord_resp = await client.cdc_reports.status()
            _LOGGER.info('CDC data by latitude/longitude: %s', cdc_coord_resp)

            # Get CDC data for North Dakota
            cdc_state_resp = await client.cdc_reports.status_by_state(
                'North Dakota')
            _LOGGER.info('CDC data by state name: %s', cdc_state_resp)
        except FluNearYouError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
