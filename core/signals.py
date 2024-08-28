import signal
import sys
from typing import Callable, List
from functools import wraps


shutdown_funcs: List[Callable] = []


def on_shutdown(func: Callable) -> Callable:
    shutdown_funcs.append(func)
    return func


def actual_shutdown():
    for func in shutdown_funcs:
        func()
    sys.exit(0)
