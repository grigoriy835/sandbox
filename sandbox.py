import asyncio


URL_LIST = ['<url1>',
            '<url2>',
            '<url2>',
            ]

def demo_async(urls):
    """Fetch list of web pages asynchronously."""
    loop = asyncio.get_event_loop() # event loop
    future = asyncio.ensure_future(fetch_all(urls)) # tasks to do
    loop.run_until_complete(future) # loop until done

async def fetch_all(urls):
    tasks = [] # dictionary of start times for each url
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task) # create list of tasks
        _ = await asyncio.gather(*tasks) # gather task responses

async def fetch(url, session):
    """Fetch a url, using specified ClientSession."""
    async with session.get(url) as response:
        resp = await response.read()
        print(resp)

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(demo_async, args=[URL_LIST], trigger='interval', seconds=15)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass