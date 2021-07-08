import time


def sample(k):
    pass

# threading !!!!!!!!!!!!!!!!!!!!!!!!!!
import threading

threads = []
for i in range(100):
    t = threading.Thread(target=sample, args=[i])
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # w8 for thread is done
    print('w8')


# futures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import concurrent.futures as fut

start = time.time()

with fut.ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(sample, i) for i in range(100)]
    for future in fut.as_completed(futures):
        future.result()


print(f'end, time: {time.time()-start}')
