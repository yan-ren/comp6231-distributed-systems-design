#### Run mpi
```
mpirun -np 4 python T3.py
```
```
mpiexec -host localhost -np 4 python T3.py
```

#### MPI misunderstanding
If plan to use MPI send to send truncate data, need to use MPI receive as well, e.g. https://mpitutorial.com/tutorials/mpi-send-and-receive/. In current implementation, each worker reads the file again and get its assigned chuck, even the result is still correct but it's not the good way to use MPI.