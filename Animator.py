import time
from typing import TypedDict

class Animation_Future(TypedDict):
    func: callable
    init_time: float
    time_elapsed: float
    delay: float

class Animator:
    def __init__(self):
        self.list_funcs: list[Animation_Future] = []

    def add_animation(self, func, delay: float):
        self.list_funcs.append({"func": func, "init_time": time.time(), "time_elapsed": 0, "delay": delay})

    def update(self, dt: float):
        for func_dict in self.list_funcs:
            func_dict["time_elapsed"] += dt
            if func_dict["time_elapsed"] >= func_dict["delay"]:
                func_dict["func"]()
                self.list_funcs.remove(func_dict)
