import asyncio
import time

from syncer import sync

@sync
async def test_timeouter(isolated_page):
    await isolated_page.goto('https://react.microfrontends.app/', waitUntil='networkidle0')
    await asyncio.gather(
        isolated_page.click('[href="/planets"]'),
        isolated_page.waitForSelector('.planetList a'),
    )
    print(await isolated_page.Jeval('.planetList a', 'e => e.textContent'))

