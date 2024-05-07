import tkinter as tk
from tkinter import ttk

from session_frame import SessionFrame


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Requests GUI")
        self.frames = {}
        self.session_index = 1
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.setup_menubar()
        self.setup_gui()
        self.add_session()

    def setup_menubar(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Sessions", command=lambda: None)
        file_menu.add_command(label="Load Sessions", command=lambda: None)
        file_menu.add_command(label="Quit", command=self.exit)
        session_menu = tk.Menu(menubar, tearoff=0)
        session_menu.add_command(label="Add Session", command=self.add_session)
        session_menu.add_command(label="Configure Session", command=lambda: None)
        session_menu.add_command(label="Close Session", command=self.close_session)
        session_menu.add_command(label="Close All Sessions", command=self.close_all)
        endpoint_menu = tk.Menu(menubar, tearoff=0)
        endpoint_menu.add_command(label="Add Endpoint", command=self.add_endpoint)
        endpoint_menu.add_command(label="Close Endpoint", command=self.close_endpoint)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Session", menu=session_menu)
        menubar.add_cascade(label="Endpoint", menu=endpoint_menu)
        self.config(menu=menubar)

    def setup_gui(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1)

    def add_session(self) -> None:
        name = f"Session {self.session_index}"
        frame = SessionFrame(self.notebook)
        self.notebook.add(frame, text=name)
        self.notebook.select(frame)
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

    def add_endpoint(self) -> None:
        if tab := self.notebook.select():
            name = self.notebook.tab(tab, "text")
            frame = self.frames[name]
            frame.add_endpoint()

    def close_endpoint(self) -> None:
        if tab := self.notebook.select():
            name = self.notebook.tab(tab, "text")
            frame = self.frames[name]
            frame.close_endpoint()

    def exit(self) -> None:
        self.destroy()
        self.quit()


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
