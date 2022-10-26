import multiprocessing
import time
from multiprocessing import Pool


def sum_square(number):
    s = 0
    for i in range(number):
        s += i * i
    return s


def compute_serially(numbers):
    print('using serial execution')
    start = time.time()
    result = []
    for number in numbers:
        result.append(sum_square(number))
    finish = time.time()
    print(f'time taken (serial execution): {round(finish - start, 2)} second(s)\n')


def compute_multiprocessing(numbers, n_processes: int = multiprocessing.cpu_count()):
    print('using multiprocessing')
    start = time.time()
    p = Pool(processes=n_processes)
    result = p.map(sum_square, numbers)
    p.close()
    p.join()
    finish = time.time()
    print(f'time taken with {n_processes} processes (multiprocessing execution): {round(finish - start, 2)} second(s)')


if __name__ == '__main__':
    n = range(30000)
    compute_serially(numbers=n)
    compute_multiprocessing(numbers=n)
