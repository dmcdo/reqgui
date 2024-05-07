import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from requests import Session

from endpoint_frame import EndpointFrame


class SessionFrame(tk.Frame):
    def __init__(self, master: tk.Misc, session: Optional[Session] = None):
        super().__init__(master)
        self.session = session or Session()
        self.endpoint_index = 1
        self.setup_gui()

    def setup_gui(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
        self.add_endpoint()

    def add_endpoint(self) -> None:
        name = f"Endpoint {self.endpoint_index}"
        frame = EndpointFrame(self.notebook, self.session)
        self.notebook.add(frame, text=name)
        self.notebook.select(frame)
        self.endpoint_index += 1

    def close_endpoint(self) -> None:
        if tab := self.notebook.select():
            self.notebook.forget(tab)
