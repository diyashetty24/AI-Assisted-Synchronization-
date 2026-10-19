import random
import sys
import threading
import time

from simlib import Recorder

NUM_READERS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
NUM_WRITERS = int(sys.argv[2]) if len(sys.argv) > 2 else 2
DELAY = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
ROUNDS = 3

names = [f"R{i}" for i in range(1, NUM_READERS + 1)] + \
        [f"W{i}" for i in range(1, NUM_WRITERS + 1)]
recorder = Recorder("Readers-Writers - Monitor (writer-preference)", names)


class ReadWriteMonitor:
    def __init__(self):
        self.condition = threading.Condition()   # has its own lock inside
        self.active_readers = 0
        self.writer_active = False
        self.waiting_writers = 0
        self.value = 0                            # the shared data

    def start_read(self, name):
        with self.condition:
            while self.writer_active or self.waiting_writers > 0:
                self.condition.wait()
            self.active_readers += 1
            recorder.state(name, "reading", f"{name} reads value {self.value}")
            recorder.var("active readers", self.active_readers)

    def end_read(self, name):
        with self.condition:
            self.active_readers -= 1
            recorder.state(name, "idle", f"{name} finished reading")
            recorder.var("active readers", self.active_readers)
            if self.active_readers == 0:
                self.condition.notify_all()      # a writer may be waiting

    def start_write(self, name):
        with self.condition:
            self.waiting_writers += 1
            while self.writer_active or self.active_readers > 0:
                self.condition.wait()
            self.waiting_writers -= 1
            self.writer_active = True
            recorder.state(name, "writing", f"{name} is writing")

    def end_write(self, name):
        with self.condition:
            self.value += 1
            recorder.var("value", self.value)
            self.writer_active = False
            recorder.state(name, "idle", f"{name} finished writing")
            self.condition.notify_all()          # wake readers and writers


monitor = ReadWriteMonitor()


def wait_a_bit():
    time.sleep(random.uniform(0.5, 1.5) * DELAY)


def reader(number):
    name = f"R{number}"
    for _ in range(ROUNDS):
        wait_a_bit()
        recorder.state(name, "waiting")
        monitor.start_read(name)
        wait_a_bit()
        monitor.end_read(name)


def writer(number):
    name = f"W{number}"
    for _ in range(ROUNDS):
        wait_a_bit()
        recorder.state(name, "waiting")
        monitor.start_write(name)
        wait_a_bit()
        monitor.end_write(name)


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
    result = "OK" if monitor.value == expected else "WRONG"
    print(f"Final value = {monitor.value} (expected {expected}) -> {result}")
    recorder.write_html("rw_monitor.html")
