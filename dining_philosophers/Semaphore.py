import os
import random
import sys
import threading
import time

from simlib import Recorder

NUM = 4
MEALS = 3
DELAY = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3

chopstick_locks = [threading.Semaphore(1) for _ in range(NUM)]
room = threading.Semaphore(NUM - 1)
meals_eaten = [0] * NUM

recorder = Recorder("Dining Philosophers (4) - Semaphores (room = 3)",
                    [f"P{i}" for i in range(NUM)],
                    chopsticks=list(range(NUM)), circle=True)


def wait_a_bit():
    time.sleep(random.uniform(0.5, 1.5) * DELAY)


def philosopher(i):
    name = f"P{i}"
    left = i
    right = (i + 1) % NUM

    for _ in range(MEALS):
        recorder.state(name, "thinking")
        wait_a_bit()

        recorder.state(name, "hungry")
        room.acquire()                     # take a seat at the table
        chopstick_locks[left].acquire()
        recorder.chopstick(left, name, f"{name} picks up chopstick {left}")
        chopstick_locks[right].acquire()
        recorder.chopstick(right, name, f"{name} picks up chopstick {right}")

        recorder.state(name, "eating")
        wait_a_bit()
        meals_eaten[i] += 1

        # Record first, then release, so the log order stays correct.
        recorder.chopstick(left, None, f"{name} puts down chopstick {left}")
        chopstick_locks[left].release()
        recorder.chopstick(right, None, f"{name} puts down chopstick {right}")
        chopstick_locks[right].release()
        room.release()                     # leave the table

    recorder.state(name, "done", f"{name} finished all meals")


if __name__ == "__main__":
    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Meals eaten:", meals_eaten)
    print("All philosophers finished - no deadlock.")
    recorder.write_html("dp_semaphore.html")
