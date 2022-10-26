from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    message = '"I am in a COMP 6231 lab tutorial ' + f'-Worker {rank}"'
    for i in range(1, size):
      comm.send(message, dest=i)
else:
    message_received = comm.recv()
    print(f'Worker {rank}, I received {message_received}')
