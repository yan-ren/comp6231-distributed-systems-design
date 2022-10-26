"""
dataset borrowed from: https://www.kaggle.com/datasets/ekibee/car-sales-information?select=region25.csv
"""


import time
import multiprocessing
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool


def compute_serially(data: str = '../datasets/region25.csv'):
    print('using serial execution')
    start = time.time()
    df = pd.read_csv(data)
    print(df['brand'].value_counts())
    print(f'time taken (serial execution): {round(time.time()-start, 2)} second(s)\n')


def map_tasks(reading_info: list, data: str = '../datasets/region25.csv'):
    df = pd.read_csv(data, nrows=reading_info[0], skiprows=reading_info[1], header=None)
    return df.iloc[:, :1].value_counts()


def reduce_task(mapping_output: list):
    reduce_out = {}
    for out in tqdm(mapping_output):
        for key, value in out.to_dict().items():
            if key in reduce_out:
                reduce_out[key] = reduce_out.get(key) + value
            else:
                reduce_out[key] = value
    print(reduce_out)


def compute_multiprocessing():
    def distribute_rows(n_rows: int, n_processes):
        reading_info = []
        skip_rows = 1
        reading_info.append([n_rows - skip_rows, skip_rows])
        skip_rows = n_rows

        for _ in range(1, n_processes - 1):
            reading_info.append([n_rows, skip_rows])
            skip_rows = skip_rows + n_rows

        reading_info.append([None, skip_rows])
        return reading_info

    print('using multiprocessing')
    processes = multiprocessing.cpu_count()
    p = Pool(processes=processes)
    start = time.time()
    result = p.map(map_tasks, distribute_rows(n_rows=200000, n_processes=processes))
    reduce_task(result)
    p.close()
    p.join()
    print(f'time taken with {processes} processes (multiprocessing execution): {round(time.time() - start, 2)} second(s)')


if __name__ == '__main__':
    compute_serially()
    compute_multiprocessing()
