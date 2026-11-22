#!python
"""
AxiosGetCompiti Configuratore.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import os

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
import yaml
import re
from pydantic import ValidationError

from AxiosGetCompiti import file_config_default, format_yaml_with_comments
from moduli.model_config import ConfigCredenzialiYaml


class ApplicationGUIConfigurator():
    """
    Interfaccia grafica del configuratore.

    :param DIR: Percorso di salvataggio log e errori
    :type DIR: str

    :param root: Radice principale della finestra Tkinter
    :type root: tk.Tk
    """
    def __init__(self, DIR: str, root: tk.Tk):
        self.percorso_configurazione = None
        self.DIR = DIR
        self.root = root

        # Finestra 5x2
        self.window = tk.Toplevel()

        self.window.title("Axios-get Configuratore")
        self.window.geometry("800x400")

        self.window.grab_set()
        self.window.transient(root)

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
        self.text_area.tag_configure("chiave", foreground="#46acff", font=("Consolas", 9, "bold"))  # Blu
        self.text_area.tag_configure("stringa", foreground="#fda33d")                               # Arancione
        self.text_area.tag_configure("numero_bool", foreground="#ffdc43")                           # Giallo
        self.text_area.tag_configure("commento", foreground="#6a9955", font=("Consolas", 9, "italic"))  # Verde scuro

        # Collega la colorazione a ogni tasto rilasciato
        self.text_area.bind("<KeyRelease>", self.evidenzia_sintassi)

        # Testo iniziale
        esempio = file_config_default()
        self.text_area.insert("1.0", esempio)
        self.evidenzia_sintassi()  # Colora subito all'avvio

        self.label_credit = tk.Text(self.window, font=("Consolas", 8), wrap=tk.WORD, relief="flat", bd=0, height=4, bg=self.window.cget("bg"))
        self.label_credit.tag_config("Bold", foreground="#569cd6", font=("Consolas", 8, "bold"))
        self.label_credit.insert("end", "Axios-get\n", "Bold")
        self.label_credit.insert("end", "Autore: Roberto Quintiliani\n")
        self.label_credit.insert("end", "Licenza: Open Source (MIT)\n")
        self.label_credit.insert("end", "Progetto: https://github.com/robyquin/axios-get")
        self.label_credit.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        self.label_credit.config(state="disabled")

        self.lbl_stato = tk.Label(self.window, text="Stato: Pronto", anchor="w", relief="sunken", padx=5)
        self.lbl_stato.grid(row=5, column=0, columnspan=2, sticky="ew")

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
            # Ipotizzo che ci sia di default una stringa
            (r":(.*)$", "stringa", 1),
            # Elementi di una lista (elementi non chiavi)
            (r"(?m)^[ \t\-]*([a-zA-Z0-9_\-\.]+)[^:]+$", "stringa", 1),
            # Numeri interi o decimali dopo i due punti
            (r":\s*(\-{0,1}\d+(\.\d+){0,1})[^\.]", "numero_bool", 0),
            # Chiavi (es. "nome:" o "- nome:")
            (r"(?m)^[ \t\-]*([a-zA-Z0-9_\-\.]+)\s*:", "chiave", 1),
            # Valori booleani o nulli
            (r":\s*\b(true|false|yes|no|null|~)\b", "numero_bool", 1),
            # Commenti che iniziano con #
            (r"(?m)#.*$", "commento", 0),
        ]

        # 3. Applica i tag alle corrispondenze trovate
        for pattern, tag, gruppo in regole:
            for match in re.finditer(pattern, contenuto, re.MULTILINE):
                start = f"1.0 + {match.start(gruppo)} chars"
                end = f"1.0 + {match.end(gruppo)} chars"
                self.text_area.tag_add(tag, start, end)

    def verifica_yaml(self) -> bool:
        """
        Verifica la correttezza della sintassi YAML e della validità del modello.

        :return: True se valido, False in caso di errore
        :rtype: bool
        """
        contenuto = self.text_area.get("1.0", "end-1c")
        if not contenuto.strip():
            self.lbl_stato.config(text="Stato: Il file è vuoto", fg="orange")
            return False
        try:
            config_default = yaml.safe_load(contenuto)
            self.lbl_stato.config(text="Stato: YAML valido ✔", fg="green")
            ConfigCredenzialiYaml.model_validate(config_default)
            return True
        except yaml.YAMLError as e:
            self.lbl_stato.config(text=f"Stato: Errore di sintassi {e} ✖", fg="red")
            # messagebox.showerror("Errore di sintassi YAML", f"Dettagli:\n\n{e}")
            return False
        except ValidationError as e:
            for dettagli_e in e.errors():
                loc = ".".join(str(x) for x in dettagli_e.get('loc', ['unknown']))
                msg = dettagli_e.get('msg', 'Unknown error')
                if dettagli_e.get('type') == 'missing_field':
                    self.lbl_stato.config(text=f"Manca il campo: {loc} ✖", fg="red")
                elif dettagli_e.get('type') == 'extra_forbidden':
                    self.lbl_stato.config(text=f"Campo non permesso: {loc} ✖", fg="red")
                else:
                    self.lbl_stato.config(text=f"{dettagli_e.get('type')} {loc}: {msg} ✖", fg="red")
            return False
        except ValueError as e:
            # Eccezione custom (coerenza notifiche non configurata)
            self.lbl_stato.config(text=f"Errore di coerenza: {e} ✖", fg="red")
            return False
        except Exception as e:
            # Altri errori (file non trovato, permessi, ecc.)
            print(f"Errore imprevisto: {type(e).__name__}: {e}")
            return False

    def salva_file(self) -> bool:
        """
        Salva il contenuto dell'area di testo in un file YAML valido con commenti.

        :return: True se salvato con successo, False in caso di errore
        :rtype: bool
        """
        if not self.verifica_yaml():
            if not messagebox.askyesno("Attenzione", "YAML non valido. Salvare comunque?"):
                return

        percorso = os.path.join(self.DIR, "credenziali.yml")
        if percorso:
            try:
                config_default = yaml.safe_load(self.text_area.get("1.0", "end-1c"))
                config_validato = ConfigCredenzialiYaml.model_validate(config_default)

                # Genera YAML con commenti
                content_con_commenti = format_yaml_with_comments(config_validato.model_dump())

                with open(percorso, "w", encoding="utf-8") as f:
                    f.write(content_con_commenti)
                self.lbl_stato.config(text=f"Salvato in: {percorso}", fg="blue")
            except Exception as e:
                messagebox.showerror("Errore salvataggio", f"Impossibile formattare il file:\n{e}")
                return

    def carica_file(self, percorso: str = None):
        """
        Carica un file YAML dal percorso specificato o dalla dialog di selezione.

        :param percorso: Percorso del file da caricare (opzionale)
        :type percorso: str
        """
        if (percorso is None):
            percorso = filedialog.askopenfilename(filetypes=[("YAML", "*.yml *.yaml")])
        self.percorso_configurazione = percorso
        if self.percorso_configurazione:
            with open(self.percorso_configurazione, "r", encoding="utf-8") as f:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", f.read())
            self.evidenzia_sintassi()
            self.verifica_yaml()
            self.root.wait_window(self.window)

    def run(self, path_config_file: str = None):
        """
        Avvia l'interfaccia grafica e gestisce il ciclo principale.

        :param path_config_file: Percorso del file di configurazione da caricare all'avvio (opzionale)
        :type path_config_file: str
        """
        if (path_config_file is not None):
            self.carica_file(percorso=path_config_file)
        self.window.mainloop()
