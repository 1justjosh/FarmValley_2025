from src.engine.settings import *

class Timer:
    def __init__(self, duration: int, func=None,end_func=None):
        """
        A timer that runs a function immediately and then prevents reactivation
        until the duration has passed.

        :param duration: Duration in milliseconds.
        :param func: The function to call when the timer is activated.
        """
        self.duration = duration
        self.func = func
        self.end_func = end_func
        self.start_time = None  # Track activation time

    @property
    def active(self):
        return self.start_time is not None

    def activate(self):
        if self.start_time is None:  # Only activate if not already running
            if self.func:
                self.func()  # Run the function immediately
            self.start_time = pg.time.get_ticks()  # Start the timer

    def update(self):
        if self.start_time is not None:  # If timer is running
            current_time = pg.time.get_ticks()
            if current_time - self.start_time >= self.duration:
                self.start_time = None  # Reset timer, allowing reactivation
                if self.end_func:
                    self.end_func()
