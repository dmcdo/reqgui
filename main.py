import tkinter as tk
from tkinter import ttk, messagebox
import requests


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.geometry("500x500")
        self.setup_gui()

    def setup_gui(self) -> None:
        self.method_var = tk.StringVar(value="GET")
        self.method_combo = ttk.Combobox(
            master=self,
            values=["GET"],
            textvariable=self.method_var
        )
        self.method_combo.grid(row=0, column=0)

        self.url_entry = ttk.Entry(self)
        self.url_entry.grid(row=0, column=1, sticky="ew")

        self.go_button = ttk.Button(self, text="Go!", command=self.go)
        self.go_button.grid(row=0, column=2)

        self.response_text = tk.Text(self)
        self.response_text.grid(row=1, column=0, columnspan=3, sticky="nesw")
        self.response_text.config(state=tk.DISABLED)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

    def go(self) -> None:
        method = self.method_var.get()
        url = self.url_entry.get().strip()

        if not url.startswith(("https://", "http://")):
            url = f"https://{url}"

        response = requests.request(method, url)
        self.title(response.status_code)
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, response.text)
        self.response_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()