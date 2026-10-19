import random
import sys
import threading
import time

from simlib import Recorder

NUM = 4
MEALS = 3
DELAY = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3

recorder = Recorder("Dining Philosophers (4) - Monitor (both chopsticks at once)",
                    [f"P{i}" for i in range(NUM)],
                    chopsticks=list(range(NUM)), circle=True)


class Table:
    """The monitor: shared data + one lock/condition that guards it."""

    def __init__(self):
        self.condition = threading.Condition()
        self.chopstick_free = [True] * NUM
        self.meals_eaten = [0] * NUM

    def pick_up(self, i):
        name = f"P{i}"
        left = i
        right = (i + 1) % NUM
        with self.condition:
            recorder.state(name, "hungry")
            while not (self.chopstick_free[left] and self.chopstick_free[right]):
                self.condition.wait()            # sleep until a neighbour puts down
            self.chopstick_free[left] = False
            self.chopstick_free[right] = False
            recorder.chopstick(left, name, f"{name} picks up chopstick {left}")
            recorder.chopstick(right, name, f"{name} picks up chopstick {right}")
            recorder.state(name, "eating")

    def put_down(self, i):
        name = f"P{i}"
        left = i
        right = (i + 1) % NUM
        with self.condition:
            self.chopstick_free[left] = True
            self.chopstick_free[right] = True
            self.meals_eaten[i] += 1
            recorder.chopstick(left, None, f"{name} puts down chopstick {left}")
            recorder.chopstick(right, None, f"{name} puts down chopstick {right}")
            recorder.state(name, "thinking")
            self.condition.notify_all()          # neighbours may be waiting


table = Table()


def wait_a_bit():
    time.sleep(random.uniform(0.5, 1.5) * DELAY)


def philosopher(i):
    name = f"P{i}"
    for _ in range(MEALS):
        recorder.state(name, "thinking")
        wait_a_bit()
        table.pick_up(i)
        wait_a_bit()                             # eating
        table.put_down(i)
    recorder.state(name, "done", f"{name} finished all meals")


if __name__ == "__main__":
    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("Meals eaten:", table.meals_eaten)
    print("All philosophers finished - no deadlock.")
    recorder.write_html("dp_monitor.html")
