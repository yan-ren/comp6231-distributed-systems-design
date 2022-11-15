import pandas as pd
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

dataset = '~/Combined_Flights_2021.csv'

if rank == 0:
    """
    Master worker (with rank 0) is responsible for distributes the workload evenly 
    between slave workers.
    """
    def load_data_in_chunks(data: str, chucks: int = 4) -> list:
        df = pd.read_csv(data)
        return np.array_split(df, chucks)


    def reduce_task(mapping_output: list):
        reduce_out = {}
        for out in mapping_output:
            for key, value in out.to_dict().items():
                if key in reduce_out:
                    reduce_out[key] = reduce_out.get(key) + value
                else:
                    reduce_out[key] = value
        print(reduce_out)
        print('Airline had the most canceled flights in September 2021', max(reduce_out, key=reduce_out.get))


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


elif rank > 0:
    df = comm.recv()
    print(f'Worker {rank} is assigned chunk {df.size} {dataset}')
    data = df[(df['Year'] == 2021) & (df['Month'] == 9) & (df['Cancelled'] == True)]
    result = data.iloc[:, 1:2].value_counts()
    print(f'Worker slave {rank} is done. Sending back to master')
    comm.send(result, dest=0)
