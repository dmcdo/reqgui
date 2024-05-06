import tkinter as tk
from tkinter import ttk

from endpoint_frame import EndpointFrame


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frames = {}
        self.session_index = 1
        self.geometry("800x600")
        self.setup_menubar()
        self.setup_gui()
        self.add_session()

    def setup_menubar(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add Session", command=self.add_session)
        file_menu.add_command(label="Save Sessions", command=lambda: None)
        file_menu.add_command(label="Load Sessions", command=lambda: None)
        action_menu = tk.Menu(menubar, tearoff=0)
        action_menu.add_command(label="Close Session", command=self.close_session)
        action_menu.add_command(label="Close All Sessions", command=self.close_all)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Action", menu=action_menu)
        self.config(menu=menubar)

    def setup_gui(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1)

    def add_session(self) -> None:
        name = f"Session {self.session_index}"
        frame = EndpointFrame(self.notebook)
        self.notebook.add(frame, text=name)
        self.frames[name] = frame
        self.session_index += 1

    def close_session(self) -> None:
        if tab := self.notebook.select():
            name = self.notebook.tab(tab, "text")
            self.notebook.forget(tab)
            del self.frames[name]

    def close_all(self) -> None:
        for tab in self.notebook.tabs():
            name = self.notebook.tab(tab, "text")
            self.notebook.forget(tab)
            del self.frames[name]


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
