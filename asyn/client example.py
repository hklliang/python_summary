import aiohttp
import asyncio
import async_timeout


conn = aiohttp.TCPConnector(limit=10)
async def fetch(session,url):
    with async_timeout.timeout(5):
        async with session.post(url, json={'test': 'object'}) as response:
            return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html=await fetch(session,'http://httpbin.org/post')



loop=asyncio.get_event_loop()
tasks=[main() for i in range(500)]
# print(tasks)
loop.run_until_complete(asyncio.wait(tasks))