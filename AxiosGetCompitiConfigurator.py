#!python
"""
AxiosGetCompiti Configuratore.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import sys
import os
from pathlib import Path

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
import yaml
import re

from AxiosGetCompiti import file_config_default

class ApplicationGUIConfigurator():

    def __init__(self):
        self.percorso_configurazione = None

        # Finestra 5x2
        self.window = tk.Toplevel()

        self.window.title("Axios-get Configuratore")
        self.window.geometry("800x400") 

        # Pulsanti
        button_open = ttk.Button(self.window, text="Apri .yml", command=self.carica_file)
        button_open.grid(row=0, column=0, padx=10, pady=10)

        button_verifica = ttk.Button(self.window, text="Verifica Sintassi", command=self.verifica_yaml)
        button_verifica.grid(row=1, column=0, padx=10, pady=10)

        button_save = ttk.Button(self.window, text="Salva credenziali.yml", command=self.salva_file)
        button_save.grid(row=2, column=0, padx=10, pady=10)

        # Area di testo con tema scuro
        self.text_area = scrolledtext.ScrolledText(self.window, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", undo=True)
        self.text_area.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=5, pady=5)

        # Configurazione colori dei Tag
        self.text_area.tag_configure("chiave", foreground="#569cd6", font=("Consolas", 9, "bold")) # Blu
        self.text_area.tag_configure("stringa", foreground="#ce9178")                               # Arancione
        self.text_area.tag_configure("numero_bool", foreground="#b5cea8")                           # Verde chiaro
        self.text_area.tag_configure("commento", foreground="#6a9955", font=("Consolas", 9, "italic")) # Verde scuro

        # Collega la colorazione a ogni tasto rilasciato
        self.text_area.bind("<KeyRelease>", self.evidenzia_sintassi)

        # Testo iniziale
        esempio = file_config_default()
        self.text_area.insert("1.0", esempio)
        self.evidenzia_sintassi() # Colora subito all'avvio

        self.lbl_stato = tk.Label(self.window, text="Stato: Pronto", anchor="w", relief="sunken", padx=5)
        self.lbl_stato.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(3, weight=1)

    def evidenzia_sintassi(self, event=None):
        """Scansiona il testo e applica i colori YAML tramite i Tag."""
        # 1. Rimuove tutti i tag esistenti prima di ricalcolarli
        for tag in ["chiave", "stringa", "numero_bool", "commento"]:
            self.text_area.tag_remove(tag, "1.0", tk.END)

        contenuto = self.text_area.get("1.0", "end-1c")

        # 2. Regole Regex per gli elementi YAML
        regole = [
            # Chiavi (es. "nome:" o "- nome:")
            (r"(?m)^[\s\-]*([a-zA-Z0-9_\-\.\s]+)\s*:", "chiave", 1),
            # Valori booleani o nulli
            (r":\s*\b(true|false|yes|no|null|~)\b", "numero_bool", 1),
            # Numeri interi o decimali dopo i due punti
            (r":\s*(-?\d+(?:\.\d+)?)\b", "numero_bool", 1),
            # Stringhe tra virgolette singole o doppie
            (r"([\"'])(?:(?=(\\?))\2.)*?\1", "stringa", 0),
            # Commenti che iniziano con #
            (r"#.*$", "commento", 0),
        ]

        # 3. Applica i tag alle corrispondenze trovate
        for pattern, tag, gruppo in regole:
            for match in re.finditer(pattern, contenuto, re.MULTILINE):
                start = f"1.0 + {match.start(gruppo)} chars"
                end = f"1.0 + {match.end(gruppo)} chars"
                self.text_area.tag_add(tag, start, end)

    def verifica_yaml(self):
        contenuto = self.text_area.get("1.0", "end-1c")
        if not contenuto.strip():
            self.lbl_stato.config(text="Stato: Il file è vuoto", fg="orange")
            return False
        try:
            yaml.safe_load(contenuto)
            self.lbl_stato.config(text="Stato: YAML valido ✔", fg="green")
            return True
        except yaml.YAMLError as e:
            self.lbl_stato.config(text="Stato: Errore di sintassi ✖", fg="red")
            messagebox.showerror("Errore di sintassi YAML", f"Dettagli:\n\n{e}")
            return False

    def salva_file(self):
        if not self.verifica_yaml():
            if not messagebox.askyesno("Attenzione", "YAML non valido. Salvare comunque?"):
                return
        if (getattr(sys, 'frozen', False)):
            # Se l'applicazione è compilata con PyInstaller
            DIR=str(os.path.dirname(sys.executable))
        else:
            DIR=str(Path(os.path.dirname(__file__)).absolute())
        # percorso = filedialog.asksaveasfilename(defaultextension=".yml", filetypes=[("YAML", "*.yml *.yaml")])
        percorso = os.path.join(DIR, "credenziali.yml")
        if percorso:
            with open(percorso, "w", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", "end-1c"))
            self.lbl_stato.config(text=f"Salvato in: {percorso}", fg="blue")

    def carica_file(self, percorso=None):
        if (percorso is None):
            percorso = filedialog.askopenfilename(filetypes=[("YAML", "*.yml *.yaml")])
        self.percorso_configurazione = percorso
        if self.percorso_configurazione:
            with open(self.percorso_configurazione, "r", encoding="utf-8") as f:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", f.read())
            self.evidenzia_sintassi()
            self.verifica_yaml()

    def run(self, path_config_file=None):
        if (path_config_file is not None):
            self.carica_file(percorso=path_config_file)
        self.window.mainloop()

if __name__ == "__main__":

    if (getattr(sys, 'frozen', False)):
        # Se l'applicazione è compilata con PyInstaller
        DIR=str(os.path.dirname(sys.executable))
    else:
        DIR=str(Path(os.path.dirname(__file__)).absolute())

    gui = ApplicationGUIConfigurator()

    if (os.path.exists(os.path.join(DIR, "credenziali.yml"))):
        gui.run(os.path.join(DIR, "credenziali.yml"))
    else:
        gui.run()
