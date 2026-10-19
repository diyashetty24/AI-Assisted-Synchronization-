import os
import random
import sys
import threading
import time

from simlib import Recorder

# Optional command line arguments: readers writers delay
NUM_READERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
NUM_WRITERS = int(sys.argv[2]) if len(sys.argv) > 2 else 2
DELAY = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
ROUNDS = 3   # how many times each thread reads/writes

mutex = threading.Lock()
rw_lock = threading.Semaphore(1)
reader_count = 0
shared_value = 0

names = [f"R{i}" for i in range(1, NUM_READERS + 1)] + \
        [f"W{i}" for i in range(1, NUM_WRITERS + 1)]
recorder = Recorder("Readers-Writers - Semaphores (readers-preference)", names)


def wait_a_bit():
    time.sleep(random.uniform(0.5, 1.5) * DELAY)


def reader(number):
    global reader_count
    name = f"R{number}"
    for _ in range(ROUNDS):
        wait_a_bit()
        recorder.state(name, "waiting")

        # Entry section
        mutex.acquire()
        reader_count += 1
        if reader_count == 1:
            rw_lock.acquire()        # first reader blocks the writers
        recorder.state(name, "reading", f"{name} reads value {shared_value}")
        recorder.var("active readers", reader_count)
        mutex.release()

        wait_a_bit()                 # reading takes some time

        # Exit section
        mutex.acquire()
        reader_count -= 1
        recorder.state(name, "idle", f"{name} finished reading")
        recorder.var("active readers", reader_count)
        if reader_count == 0:
            rw_lock.release()        # last reader lets writers in
        mutex.release()


def writer(number):
    global shared_value
    name = f"W{number}"
    for _ in range(ROUNDS):
        wait_a_bit()
        recorder.state(name, "waiting")

        rw_lock.acquire()            # wait until nobody else is using the data
        recorder.state(name, "writing", f"{name} is writing")
        old = shared_value
        wait_a_bit()                 # if two writers got in, this would lose an update
        shared_value = old + 1
        recorder.var("value", shared_value)
        recorder.state(name, "idle", f"{name} finished writing")
        rw_lock.release()


if __name__ == "__main__":
    recorder.var("value", 0)
    recorder.var("active readers", 0)

    threads = []
    for i in range(1, NUM_READERS + 1):
        threads.append(threading.Thread(target=reader, args=(i,)))
    for i in range(1, NUM_WRITERS + 1):
        threads.append(threading.Thread(target=writer, args=(i,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = NUM_WRITERS * ROUNDS
    result = "OK" if shared_value == expected else "WRONG"
    print(f"Final value = {shared_value} (expected {expected}) -> {result}")
    recorder.write_html("rw_semaphore.html")
"""
Task 2, Question 2: Readers-Writers using semaphores and a mutex (readers-preference).

Rules:
  - Many readers may read at the same time.
  - A writer needs the data all to itself.

A mutex and a semaphore:
  mutex   - a Lock that protects the reader counter
  rw_lock - the "door" to the data; the first reader locks it for all
            readers, the last reader unlocks it, a writer locks it alone.
"""
import os
import random
import sys
import threading
import time

from simlib import Recorder

# Optional command line arguments: readers writers delay
NUM_READERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
NUM_WRITERS = int(sys.argv[2]) if len(sys.argv) > 2 else 2
DELAY = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
ROUNDS = 3   # how many times each thread reads/writes

mutex = threading.Lock()
rw_lock = threading.Semaphore(1)
reader_count = 0
shared_value = 0

names = [f"R{i}" for i in range(1, NUM_READERS + 1)] + \
        [f"W{i}" for i in range(1, NUM_WRITERS + 1)]
recorder = Recorder("Readers-Writers - Semaphores (readers-preference)", names)


def wait_a_bit():
    time.sleep(random.uniform(0.5, 1.5) * DELAY)


def reader(number):
    global reader_count
    name = f"R{number}"
    for _ in range(ROUNDS):
        wait_a_bit()
        recorder.state(name, "waiting")

        # Entry section
        mutex.acquire()
        reader_count += 1
        if reader_count == 1:
            rw_lock.acquire()        # first reader blocks the writers
        recorder.state(name, "reading", f"{name} reads value {shared_value}")
        recorder.var("active readers", reader_count)
        mutex.release()

        wait_a_bit()                 # reading takes some time

        # Exit section
        mutex.acquire()
        reader_count -= 1
        recorder.state(name, "idle", f"{name} finished reading")
        recorder.var("active readers", reader_count)
        if reader_count == 0:
            rw_lock.release()        # last reader lets writers in
        mutex.release()


def writer(number):
    global shared_value
    name = f"W{number}"
    for _ in range(ROUNDS):
        wait_a_bit()
        recorder.state(name, "waiting")

        rw_lock.acquire()            # wait until nobody else is using the data
        recorder.state(name, "writing", f"{name} is writing")
        old = shared_value
        wait_a_bit()                 # if two writers got in, this would lose an update
        shared_value = old + 1
        recorder.var("value", shared_value)
        recorder.state(name, "idle", f"{name} finished writing")
        rw_lock.release()


if __name__ == "__main__":
    recorder.var("value", 0)
    recorder.var("active readers", 0)

    threads = []
    for i in range(1, NUM_READERS + 1):
        threads.append(threading.Thread(target=reader, args=(i,)))
    for i in range(1, NUM_WRITERS + 1):
        threads.append(threading.Thread(target=writer, args=(i,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = NUM_WRITERS * ROUNDS
    result = "OK" if shared_value == expected else "WRONG"
    print(f"Final value = {shared_value} (expected {expected}) -> {result}")
    recorder.write_html("rw_semaphore.html")
