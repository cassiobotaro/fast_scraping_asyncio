import aiohttp
import asyncio


async def print_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:
            print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(print_page('http://example.com'))
