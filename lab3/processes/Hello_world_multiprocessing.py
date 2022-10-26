import os
import multiprocessing
from time import time, sleep


def compute():
    print('computing...')
    sleep(1)


def compute_serially():
    print('using serial execution')
    start = time()
    compute()
    compute()
    finished = time()
    print(f'time taken (serial execution): {round(finished - start, 2)} second(s)\n')


def compute_multi_processing():
    print('using multi-processing\nCPU-core(s) available: ', os.cpu_count())
    start = time()
    p1 = multiprocessing.Process(target=compute)
    p2 = multiprocessing.Process(target=compute)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    finished = time()
    print(f'time taken (multi-processing): {round(finished - start, 2)} second(s)')


if __name__ == '__main__':
    compute_serially()
    compute_multi_processing()


