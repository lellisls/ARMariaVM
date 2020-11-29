import threading
import time


class KeyTracker:
    keys = []
    last_press_time = dict()
    last_release_time = dict()

    def track(self, key):
        self.keys.append(key)
        self.last_press_time[key] = time.time()

    def is_pressed(self, key: str):
        return (time.time() - self.last_press_time[key]) < .1

    def report_key_press(self, event):
        if event.keysym in self.keys:
            if not self.is_pressed(event.keysym):
                print(f"KEY PRESS: {event}")
                self.on_key_press(event)
            self.last_press_time[event.keysym] = time.time()
        return "break"

    def report_key_release(self, event):
        if event.keysym in self.keys:
            timer = threading.Timer(.1, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed(event.keysym):
            print(f"KEY RELEASE: {event}")
            self.on_key_release(event)

    @classmethod
    def on_key_press(cls, event):
        pass

    @classmethod
    def on_key_release(cls, event):
        pass
