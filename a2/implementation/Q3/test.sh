#!/bin/zsh
echo "run with 3 workers"
mpirun -n 3 --oversubscribe python T3.py

echo "run with 4 workers"
mpirun -n 4 --oversubscribe python T3.py

echo "run with 5 workers"
mpirun -n 5 --oversubscribe python T3.py

echo "run with 6 workers"
mpirun -n 6 --oversubscribe python T3.py

echo "run with 7 workers"
mpirun -n 7 --oversubscribe python T3.py

echo "run with 8 workers"
mpirun -n 8 --oversubscribe python T3.py

echo "run with 9 workers"
mpirun -n 9 --oversubscribe python T3.py

echo "run with 10 workers"
mpirun -n 10 --oversubscribe python T3.py

echo "run with 11 workers"
mpirun -n 11 --oversubscribe python T3.py

echo "run with 12 workers"
mpirun -n 12 --oversubscribe python T3.py

echo "run with 13 workers"
mpirun -n 13 --oversubscribe python T3.py

echo "run with 14 workers"
mpirun -n 14 --oversubscribe python T3.py
