#!/bin/zsh
# echo "Q1 run with 1 workers"
# mpiexec -host localhost -np 2 python Q1_T3.py

echo "Q1 run with 2 workers"
mpiexec -host localhost -np 3 python Q1_T3.py

echo "Q1 run with 3 workers"
mpiexec -host localhost -np 4 python Q1_T3.py

# echo "Q2 run with 1 workers"
# mpiexec -host localhost -np 2 python Q2_T3.py

echo "Q2 run with 2 workers"
mpiexec -host localhost -np 3 python Q2_T3.py

echo "Q2 run with 3 workers"
mpiexec -host localhost -np 4 python Q2_T3.py

# echo "Q3 run with 1 workers"
# mpiexec -host localhost -np 2 python Q3_T3.py

echo "Q3 run with 2 workers"
mpiexec -host localhost -np 3 python Q3_T3.py

echo "Q3 run with 3 workers"
mpiexec -host localhost -np 4 python Q3_T3.py

# echo "Q4 run with 1 workers"
# mpiexec -host localhost -np 2 python Q4_T3.py

echo "Q4 run with 2 workers"
mpiexec -host localhost -np 3 python Q4_T3.py

echo "Q4 run with 3 workers"
mpiexec -host localhost -np 4 python Q4_T3.py
