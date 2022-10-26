from threading import Thread
import math
import numpy as np
import time

Matrix_A = []
Matrix_B = []
Matrix_C = []

size_of_vectors_n = [int(math.pow(10, 2)), int(math.pow(10, 3)), int(math.pow(10, 4))]

dimension_N = 2  # Default to a 2x2 matrix

num_of_threads = 1


def Input_for_matrix_dimensions():
    global dimension_N
    global num_of_threads

    dimension_N = int(input("Enter the number N to generate NxN matrix : "))
    num_of_threads = int(input("Enter the number of threads : "))


def Initialize_Matrix(A_value=None, B_value=None):
    global Matrix_A
    global Matrix_B
    global Matrix_C
    if A_value:
        Matrix_A = np.empty(shape=(dimension_N, dimension_N))
        Matrix_A.fill(A_value)
    else:
        Matrix_A = np.random.random((dimension_N, dimension_N))
        Matrix_A = Matrix_A * 10
        Matrix_A = Matrix_A.astype(int)
    if B_value:
        Matrix_B = np.empty(shape=(dimension_N, dimension_N))
        Matrix_B.fill(B_value)
    else:
        Matrix_B = np.random.random((dimension_N, dimension_N))
        Matrix_B = Matrix_B * 10
        Matrix_B = Matrix_B.astype(int)

    Matrix_C = np.zeros((dimension_N, dimension_N))
    Matrix_C = Matrix_C.astype(int)


def Matrix_multiply_parallel(start, end):
    for i in range(start, end):
        for j in range(dimension_N):
            for k in range(dimension_N):
                Matrix_C[i][j] += int(Matrix_A[i][k] * Matrix_B[k][j])


def Thread_function():
    global num_of_threads
    thread_handle = []
    for j in range(0, num_of_threads):
        t = Thread(target=Matrix_multiply_parallel,
                   args=(int((dimension_N / num_of_threads) * j), int((dimension_N / num_of_threads) * (j + 1))))
        thread_handle.append(t)
        t.start()

    for j in range(0, num_of_threads):
        thread_handle[j].join()


if __name__ == "__main__":
    Input_for_matrix_dimensions()

    # serial execution
    start_time = time.time()
    Initialize_Matrix(1, 1)
    Matrix_multiply_parallel(0, len(Matrix_A))
    end_time = time.time()
    print("Time taken to multiply two matrices in serial comes out to be : " + str(end_time - start_time))
    print("Matrix C=", Matrix_A)
    print("Matrix C=", Matrix_B)
    print("Matrix C=", Matrix_C)

    # multithread execution
    start_time = time.time()
    Initialize_Matrix(1, 1)
    Thread_function()
    end_time = time.time()
    print("Time taken to multiply two matrices in parallel comes out to be : " + str(end_time - start_time))
    print("Matrix C=", Matrix_A)
    print("Matrix C=", Matrix_B)
    print("Matrix C=", Matrix_C)
