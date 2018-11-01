"""Run an example script to quickly test."""
import asyncio

from aiohttp import ClientSession

from pyflunearyou import create_client
from pyflunearyou.errors import FluNearYouError


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        await run(websession)


async def run(websession: ClientSession):
    """Run."""
    try:
        # Create a client:
        client = await create_client(36.0861973, -86.8781167, websession)

        # Get user data for the client's latitude/longitude:
        print('Getting user data by latitude/longitude:')
        print(await client.user_reports.status())

        # Get user data for the a specific ZIP code:
        print()
        print('Getting user data by ZIP code:')
        print(await client.user_reports.status_by_zip("90046"))

        # Get CDC data for the client's latitude/longitude:
        print()
        print('Getting CDC data by latitude/longitude:')
        print(await client.cdc_reports.status())

        # Get CDC data for North Dakota
        print()
        print('Getting CDC data by state name:')
        print(await client.cdc_reports.status_by_state('North Dakota'))
    except FluNearYouError as err:
        print(err)


asyncio.get_event_loop().run_until_complete(main())
