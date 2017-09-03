import tqdm
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
    with await sem:
        page = await get(url, compress=True)
    magnet = first_magnet(page)
    print('{}: {}'.format(query, magnet))


async def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        await f

distros = ['archlinux', 'ubuntu', 'debian', 'manjaro', 'suse', 'elementary',
           'fedora', 'gentoo']
sem = asyncio.Semaphore(5)
loop = asyncio.get_event_loop()
f = [print_magnet(d) for d in distros]
loop.run_until_complete(wait_with_progress(f))
