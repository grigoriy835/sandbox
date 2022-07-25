import aiohttp
import time
import asyncio

url = 'testurl'


async def run(k):
    print(f'start {k}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={'response': k, 'sleep': 2}) as resp:
            text = await resp.text()
            print('pre ' + text)

    # COUNT = 10000000
    # for i in range(1000):
    #     for j in range(1000):
    #         for y in range(10):
    #             COUNT -= 1


print('hi bitch 1')
start = time.time()

loop = asyncio.get_event_loop()

gather_task = asyncio.gather(*list(run(i) for i in range(1000)))
loop.run_until_complete(gather_task)

print(f'end, time: {time.time() - start}')