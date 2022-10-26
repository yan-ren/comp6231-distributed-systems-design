import os
from mpi4py import MPI

comm = MPI.COMM_WORLD  # instantiate communication world

size = comm.Get_size()  # get size of communication world

rank = comm.Get_rank()  # get rank of particular process

PID = os.getpid()

print(f'Worker {rank}/{size} (PID: {PID}) says Hello World')
