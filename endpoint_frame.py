import json
import tkinter as tk
from tkinter import messagebox, ttk

from requests import Session

from display_exception import display_exception
from params_window import ParamsWindow


class EndpointFrame(tk.Frame):
    def __init__(self, master: tk.Misc, session: Session) -> None:
        super().__init__(master)
        self.session = session
        self.setup_gui()

    def setup_gui(self) -> None:
        self.params_button = ttk.Button(self, text="Session", command=self.params)
        self.params_button.grid(row=0, column=0)

        self.method_var = tk.StringVar(value="GET")
        self.method_combo = ttk.Combobox(master=self, values=["GET"], textvariable=self.method_var)
        self.method_combo.grid(row=0, column=1)

        self.url_entry = ttk.Entry(self)
        self.url_entry.grid(row=0, column=2, sticky="ew")

        self.go_button = ttk.Button(self, text="Go!", command=self.go)
        self.go_button.grid(row=0, column=3)

        self.feedback_label = tk.Label(self, text="✔️")
        self.feedback_label.grid(row=0, column=4)

        self.input_notebook = ttk.Notebook(self)
        self.input_notebook.grid(row=1, column=0, columnspan=5, sticky="nesw", padx=5, pady=5)
        self.setup_response_frame()

        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def setup_response_frame(self) -> None:
        self.response_frame = tk.Frame(self.input_notebook)

        self.status_label = tk.Label(self.response_frame, text="Status Code: N/A.   Content Type: N/A.")
        self.status_label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.response_text = tk.Text(self.response_frame, wrap=tk.NONE)
        self.response_text.config(state=tk.DISABLED)
        self.response_text.grid(row=1, column=0, sticky="nesw")

        yscroll = tk.Scrollbar(self.response_frame, command=self.response_text.yview)
        self.response_text["yscrollcommand"] = yscroll.set
        yscroll.grid(row=1, column=1, sticky="nesw")

        xscroll = tk.Scrollbar(self.response_frame, orient=tk.HORIZONTAL, command=self.response_text.xview)
        self.response_text["xscrollcommand"] = xscroll.set
        xscroll.grid(row=2, column=0, columnspan=2, sticky="nesw")

        self.response_frame.rowconfigure(1, weight=1)
        self.response_frame.columnconfigure(0, weight=1)
        self.input_notebook.add(self.response_frame, text="Response")

    @display_exception
    def go(self) -> None:
        method = self.method_var.get()
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showinfo("No URL", "You must enter a URL.", parent=self)
            return

        if not url.startswith(("https://", "http://")):
            url = f"https://{url}"

        # Update UI (TODO)
        self.feedback_label["text"] = "⏳"
        self.feedback_label.update()

        response = self.session.request(method, url)
        status_code = response.status_code
        content_type = response.headers.get("Content-Type")

        if content_type.startswith("application/json"):
            response_text = json.dumps(response.json(), indent=2)
        else:
            response_text = response.text

        # Update UI (TODO)
        self.feedback_label["text"] = "✔️"
        self.status_label["text"] = f"Status Code: {status_code}.   Content Type: {content_type}."
        self.response_text.config(state=tk.NORMAL)
        self.response_text.delete(1.0, tk.END)
        self.response_text.insert(1.0, response_text)
        self.response_text.config(state=tk.DISABLED)
        self.update()

    @display_exception
    def params(self) -> None:
        ParamsWindow(self, self.session)
