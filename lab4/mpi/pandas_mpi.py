import pandas as pd
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

dataset = '../datasets/region25.csv'

if rank == 0:
    """
    Master worker (with rank 0) is responsible for distributes the workload evenly 
    between slave workers.
    """
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

    slave_workers = size - 1
    chunk_distribution = distribute_rows(n_rows=200000, n_processes=slave_workers)

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

    out = {}
    for r in results:
        for key, value in r.to_dict().items():
            if key in out:
                out[key] = out[key] + value
            else:
                out[key] = value

    print(out, '\ndone.')


elif rank > 0:
    chunk_to_process = comm.recv()
    print(f'Worker {rank} is assigned chunk info {chunk_to_process} {dataset}')
    df = pd.read_csv(dataset, nrows=chunk_to_process[0], skiprows=chunk_to_process[1], header=None)
    result = df.iloc[:, :1].value_counts()
    print(f'Worker slave {rank} is done. Sending back to master')
    comm.send(result, dest=0)
