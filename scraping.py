import aiohttp
import asyncio
import bs4


async def get(*args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(*args, **kwargs) as resp:
            return await resp.text()


def first_magnet(page):
    soup = bs4.BeautifulSoup(page, "html.parser")
    a = soup.find('a', title='Download this torrent using magnet')
    return a['href']


async def print_magnet(query):
    url = 'http://thepiratebay.se/search/{}/0/7/0'.format(query)
    page = await get(url, compress=True)
    magnet = first_magnet(page)
    print('{}: {}'.format(query, magnet))

distros = ['archlinux', 'ubuntu', 'debian']
loop = asyncio.get_event_loop()
f = asyncio.wait([print_magnet(d) for d in distros])
loop.run_until_complete(f)
