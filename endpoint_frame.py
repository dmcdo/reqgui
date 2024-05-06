import tkinter as tk
from tkinter import messagebox, ttk

import requests

from display_exception import display_exception
from params_frame import ParamsFrame


class EndpointFrame(tk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.session = requests.Session()
        self.setup_gui()

    def setup_gui(self) -> None:
        self.params_button = ttk.Button(self, text="Params", command=self.params)
        self.params_button.grid(row=0, column=0)

        self.method_var = tk.StringVar(value="GET")
        self.method_combo = ttk.Combobox(master=self, values=["GET"], textvariable=self.method_var)
        self.method_combo.grid(row=0, column=1)

        self.url_entry = ttk.Entry(self)
        self.url_entry.grid(row=0, column=2, sticky="ew")

        self.go_button = ttk.Button(self, text="Go!", command=self.go)
        self.go_button.grid(row=0, column=3)

        self.response_text = tk.Text(self)
        self.response_text.grid(row=1, column=0, columnspan=4, sticky="nesw")
        self.response_text.config(state=tk.DISABLED)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    @display_exception
    def go(self) -> None:
        method = self.method_var.get()
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showinfo("No URL", "You must enter a URL.", parent=self)
            return

        if not url.startswith(("https://", "http://")):
            url = f"https://{url}"

        response = self.session.request(method, url)
        self.winfo_toplevel().title(response.status_code)
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, response.text)
        self.response_text.config(state=tk.DISABLED)

    @display_exception
    def params(self) -> None:
        ParamsFrame(self, self.session)
