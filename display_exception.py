from tkinter import messagebox
from typing import Callable


def display_exception(func: Callable):
    def internal(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            messagebox.showerror(f"Uncaught {type(e).__name__}", str(e))

    return internal
