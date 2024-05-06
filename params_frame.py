import tkinter as tk
from functools import partial
from os.path import isfile
from tkinter import filedialog, messagebox, ttk

from requests import Session


class ParamsFrame(tk.Toplevel):
    def __init__(self, master: tk.Misc, session: Session):
        super().__init__(master)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.session = session
        self.setup_gui()
        self.fill_entries()
        self.bad_param = partial(messagebox.showerror, "Invalid Parameter", parent=self)

    def setup_gui(self) -> None:
        # Cert
        self.cert_label = tk.Label(self, text="Cert")
        self.cert_label.grid(row=0, column=0)
        self.cert_entry = tk.Entry(self)
        self.cert_entry.grid(row=0, column=1, sticky="ew")
        self.cert_button = tk.Button(self, text="Open Cert File", command=self.on_cert)
        self.cert_button.grid(row=0, column=2, sticky="ew")

        # Cert Key
        self.key_label = tk.Label(self, text="Cert (Key)")
        self.key_label.grid(row=1, column=0)
        self.key_entry = tk.Entry(self)
        self.key_entry.grid(row=1, column=1, sticky="ew")
        self.key_button = tk.Button(self, text="Open Cert Key File", command=self.on_key)
        self.key_button.grid(row=1, column=2, sticky="ew")

        # Verify
        self.verify_label = tk.Label(self, text="Verify")
        self.verify_label.grid(row=2, column=0)
        self.verify_entry = tk.Entry(self)
        self.verify_entry.grid(row=2, column=1, sticky="ew")
        self.verify_button = tk.Button(self, text="Open CA Bundle", command=self.on_verify)
        self.verify_button.grid(row=2, column=2, sticky="ew")

        # OK
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.grid(row=3, column=0, columnspan=3)

        # Weights
        self.columnconfigure(1, weight=1)

    def fill_entries(self) -> None:
        # Cert/Key
        if isinstance(self.session.cert, tuple):
            self.cert_entry.delete(0, tk.END)
            self.cert_entry.insert(0, self.session.cert[0])
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, self.session.cert[1])
        elif self.session.cert:
            self.cert_entry.delete(0, tk.END)
            self.cert_entry.insert(0, self.session.cert)
        else:
            self.cert_entry.delete(0, tk.END)

        # Verify
        self.verify_entry.delete(0, tk.END)
        self.verify_entry.insert(0, str(self.session.verify))

    def on_cert(self) -> None:
        if path := filedialog.askopenfilename(
            parent=self,
            title="Open Certificate File",
            filetypes=[("PEM Certificate File", "*.pem"), ("All Files", "*.*")],
        ):
            self.cert_entry.delete(0, tk.END)
            self.cert_entry.insert(0, path)

    def on_key(self):
        if path := filedialog.askopenfilename(
            parent=self,
            title="Open Certificate File",
            filetypes=[
                ("PEM Certificate Key File", ("*.pem", "*.key")),
                ("All Files", "*.*"),
            ],
        ):
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, path)

    def on_verify(self):
        if path := filedialog.askopenfilename(
            parent=self,
            title="Open Certificate File",
            filetypes=[("PEM Certificate File", "*.ca-bundle"), ("All Files", "*.*")],
        ):
            self.verify_entry.delete(0, tk.END)
            self.verify_entry.insert(0, path)

    def on_ok(self):
        # Fetch input
        cert = self.cert_entry.get().strip()
        key = self.key_entry.get().strip()
        verify = self.verify_entry.get().strip()
        # Validate input
        if cert and not isfile(cert):
            self.bad_param("Cert value must be a valid path to a file.")
            return
        if cert and key and not isfile(key):
            self.bad_param("Cert Key value must be a valid path to a file.")
            return
        if verify:
            if isfile(verify):
                pass
            elif verify.lower() == "true":
                verify = True
            elif verify.lower() == "false":
                verify = False
            else:
                self.bad_param("Verify value must be 'True', 'False', or a valid path to a file.")
                return

        # Update Session Cert
        if cert and key:
            self.session.cert = (cert, key)
        elif cert:
            self.session.cert = cert
        else:
            self.session.cert = None

        # Update Session CA
        self.session.verify = verify
        self.on_close()

    def on_close(self) -> None:
        self.destroy()
