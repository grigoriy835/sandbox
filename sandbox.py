
# import aiohttp
# import asyncio
# import time
# import threading
# import multiprocessing
# import concurrent.futures as fut
# import requests
# from multiprocessing import Queue
import os
# from dateutil.relativedelta import relativedelta
# import datetime

#
# url = 'http://localhost:9890'
# COUNT = 1000000000
#
# # async
# # 5k requests that await 5s, result 15s(mb server  is bottleneck)
# # 1k requests that await 5s, result 8s
#
# # count: 0
# # end, time: 152.57016849517822
# def main1():
#     async def run(k):
#         print(f'start {k}')
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, params={'response': k, 'sleep': 2}) as resp:
#                 text = await resp.text()
#                 print('pre ' + text)
#
#         # COUNT = 10000000
#         # for i in range(1000):
#         #     for j in range(1000):
#         #         for y in range(10):
#         #             COUNT -= 1
#
#
#     print('hi bitch 1')
#     start = time.time()
#
#     loop = asyncio.get_event_loop()
#
#     gather_task = asyncio.gather(*list(run(i) for i in range(1000)))
#     loop.run_until_complete(gather_task)
#
#     print(f'end, time: {time.time()-start}')
#
#
# def main2():
#     global COUNT
#     def http_req(k):
#         global COUNT
#         print(f'pre {k}')
#         # resp = requests.get(url, params={'response': k, 'sleep': 2})
#         # print(resp.text)
#
#         for i in range(1000):
#             for j in range(1000):
#                 for y in range(10):
#                     COUNT -= 1
#
#         print(f'{k}')
#         return
#
#     threads = []
#     for i in range(100):
#         t = threading.Thread(target=http_req, args=[i])
#         threads.append(t)
#         t.start()
#
#     for t in threads:
#         t.join()
#         print('w8')
#
#     print(f'count {COUNT}')
#
#
# # concurent treads
# # 1k requests that await 5s, result 15s(500 workers)
#
# # 50 workers
# # count: 951595897
# # end, time: 155.50403952598572
#
# # 100 workers
# # count: 973180905
# # end, time: 153.20835518836975
#
# cont = {'i': 1000000000}
# def main3():
#     def http_req(k):
#         # resp = requests.get(url, params={'response': k, 'sleep': 2})
#         # print('pre ' + resp.text)
#         for i in range(1000):
#             for j in range(1000):
#                 for y in range(10):
#                     cont['i'] -= 1
#
#         print(f'count {k}: {cont["i"]}')
#         return 1
#
#     print('hi bitch 3')
#     start = time.time()
#
#     with fut.ThreadPoolExecutor(max_workers=10) as pool:
#         futures = [pool.submit(http_req, i) for i in range(100)]
#         for future in fut.as_completed(futures):
#             future.result()
#
#
#     print(f'count final: {cont["i"]}')
#     print(f'end, time: {time.time()-start}')


if __name__ == '__main__':
    # pass
    # main2()


    # qu = Queue()
    #
    # qu.put({"fd": 12})
    # qu.put({"fd": 13})
    #
    # li = []
    # while not qu.empty():
    #     li.append(qu.get())
    #
    # print(li)

    # bb = [
    #     's3://bucket/path1/20210315124414/',
    #     's3://bucket/path1/20210215124414/',
    #     's3://bucket/path1/20210115124414/',
    #     's3://bucket/path1/20210114124414/',
    #     's3://bucket/path1/20210113124414/',
    #     's3://bucket/path1/20210112124414/',
    #     ]

    foo = 1
    tt = os.walk(os.path.join('maverik_game'))

    for t in tt:
        print(t)















