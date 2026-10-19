"""
simlib.py - helper used by all four programs.

The Recorder remembers every event (a state change, a chopstick pickup, a
variable change) in the order it happened. At the end, write_html()
puts that list into template.html, which replays it in the browser.
"""
import json
import os
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))


class Recorder:
    def __init__(self, title, actors, chopsticks=None, circle=False):
        self.title = title
        self.actors = list(actors)        # names of threads, e.g. ["R1", "W1"]
        self.chopsticks = list(chopsticks or [])    # chopstick numbers (philosophers only)
        self.circle = circle              # True = draw actors around a table
        self.events = []
        self.start_time = time.time()
        self.lock = threading.Lock()      # many threads write to self.events

    def add_event(self, kind, message, **extra):
        # The lock makes sure events are stored in the same order they are printed.
        with self.lock:
            event = {"time": round(time.time() - self.start_time, 3),
                     "kind": kind, "message": message}
            event.update(extra)
            self.events.append(event)
            print(f"[{event['time']:7.3f}s] {message}")

    def state(self, actor, state, message=None):
        """An actor changed state (waiting, reading, eating, ...)."""
        if message is None:
            message = f"{actor} is now {state}"
        self.add_event("state", message, actor=actor, state=state)

    def chopstick(self, chopstick_id, owner, message=None):
        """A chopstick was picked up (owner = name) or put down (owner = None)."""
        if message is None:
            message = f"chopstick {chopstick_id} is now held by {owner}"
        self.add_event("chopstick", message, chopstick=chopstick_id, owner=owner)

    def var(self, name, value):
        """A shared variable changed (for the display only)."""
        self.add_event("var", f"{name} = {value}", name=name, value=value)

    def write_html(self, filename):
        data = {"title": self.title, "actors": self.actors, "chopsticks": self.chopsticks,
                "circle": self.circle, "events": self.events}
        with open(os.path.join(HERE, "template.html"), encoding="utf-8") as f:
            page = f.read()
        data_text = json.dumps(data).replace("</", "<\\/")   # keep </script> safe
        page = page.replace("__TITLE__", self.title).replace("__DATA__", data_text)

        path = os.path.join(HERE, filename)     # saved next to the program
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print("HTML written ->", path)
