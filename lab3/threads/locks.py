# example of a race condition with a shared variable
from threading import Thread
from threading import Lock


# make additions into the global variable


def adder_WithLock(amount, repeats, lock):
    global value
    lock.acquire()
    for _ in range(repeats):
        value += amount
    lock.release()


# make subtractions from the global variable
def subtractor_WithLock(amount, repeats, lock):
    global value
    lock.acquire()
    for _ in range(repeats):
        value -= amount
    lock.release()


# make additions into the global variable
def adder(amount, repeats):
    global value
    for _ in range(repeats):
        value += amount


# make subtractions from the global variable
def subtractor(amount, repeats):
    global value
    for _ in range(repeats):
        value -= amount


def add_subtract_withLock():
    # define a lock to protect the shared variable
    lock = Lock()
    # start a thread making additions
    adder_thread = Thread(target=adder_WithLock, args=(10, 1000000, lock))
    adder_thread.start()
    # start a thread making subtractions
    subtractor_thread = Thread(target=subtractor_WithLock, args=(10, 1000000, lock))
    subtractor_thread.start()
    # wait for both threads to finish
    print('Waiting for threads to finish...')
    adder_thread.join()
    subtractor_thread.join()
    # report the value
    print(f'Value: {value}')


def add_subtract():
    # start a thread making additions
    adder_thread = Thread(target=adder, args=(10, 1000000))
    adder_thread.start()
    # start a thread making subtractions
    subtractor_thread = Thread(target=subtractor, args=(10, 1000000))
    subtractor_thread.start()
    # wait for both threads to finish
    print('Waiting for threads to finish...')
    adder_thread.join()
    subtractor_thread.join()
    # report the value
    print(f'Value: {value}')


value = 0
add_subtract()
# add_subtract_withLock()
