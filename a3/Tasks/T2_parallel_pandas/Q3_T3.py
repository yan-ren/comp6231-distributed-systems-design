import time

import pandas as pd
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

dataset = './Combined_Flights_2021.csv'

if rank == 0:
    """
    Master worker (with rank 0) is responsible for distributes the workload evenly 
    between slave workers.
    """
    def load_data_in_chunks(data: str, chucks: int = 4) -> list:
        df = pd.read_csv(data)
        return np.array_split(df, chucks)

    def reduce_task(mapping_output: list):
        total_count = 0
        total_time = 0
        for out in mapping_output:
            for key, value in out.items():
                total_count += key
                total_time += value
        print('Average airtime for flights that were flying from Nashville to Chicago:',
              total_time / total_count)

    start_time = time.time()

    slave_workers = size - 1
    chunk_distribution = load_data_in_chunks(dataset, slave_workers)

    # distribute tasks to slaves
    for worker in range(1, size):
        chunk_to_process = worker-1
        comm.send(chunk_distribution[chunk_to_process], dest=worker)

    # receive and aggregate results from slave
    results = []
    for worker in (range(1, size)):  # receive
        result = comm.recv(source=worker)
        results.append(result)
        print(f'received from Worker slave {worker}')

    reduce_task(results)
    print("--- %s seconds ---" % (time.time() - start_time))


elif rank > 0:
    data = comm.recv()
    # print(f'Worker {rank} is assigned chunk {data.size} {dataset}')
    data = data[(data['OriginCityName'] == 'Nashville, TN')
                & (data['DestCityName'] == 'Chicago, IL')]
    result = {len(data.index): data['AirTime'].sum()}
    print(f'Worker slave {rank} is done. Sending back to master')
    comm.send(result, dest=0)
