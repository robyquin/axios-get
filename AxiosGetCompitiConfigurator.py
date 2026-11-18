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

class ApplicationGUIConfigurator():

    def __init__(self):
        self.percorso_configurazione = None
        # --- Finestra ---
        self.window = tk.Tk()
        ttk.Style().theme_use("clam")
        self.window.title("Axios-get Configuratore")
        self.window.geometry("650x500")

        self.window.columnconfigure((0, 1, 2), weight=1)
        self.window.rowconfigure(1, weight=1)

        # Pulsanti
        ttk.Button(self.window, text="Apri .yml", command=self.carica_file).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(self.window, text="Verifica Sintassi", command=self.verifica_yaml).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(self.window, text="Salva credenziali.yml", command=self.salva_file).grid(row=0, column=2, sticky="ew", padx=5, pady=5)

        # Area di testo con tema scuro
        self.text_area = scrolledtext.ScrolledText(self.window, font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", undo=True)
        self.text_area.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Configurazione colori dei Tag
        self.text_area.tag_configure("chiave", foreground="#569cd6", font=("Consolas", 12, "bold")) # Blu
        self.text_area.tag_configure("stringa", foreground="#ce9178")                               # Arancione
        self.text_area.tag_configure("numero_bool", foreground="#b5cea8")                           # Verde chiaro
        self.text_area.tag_configure("commento", foreground="#6a9955", font=("Consolas", 9, "italic")) # Verde scuro

        # Collega la colorazione a ogni tasto rilasciato
        self.text_area.bind("<KeyRelease>", self.evidenzia_sintassi)

        # Testo iniziale
        esempio = self.file_config_default("1.1.1")
        self.text_area.insert("1.0", esempio)
        self.evidenzia_sintassi() # Colora subito all'avvio

        self.lbl_stato = tk.Label(self.window, text="Stato: Pronto", anchor="w", relief="sunken", padx=5)
        self.lbl_stato.grid(row=2, column=0, columnspan=3, sticky="ew")

    def evidenzia_sintassi(self, event=None):
        """Scansiona il testo e applica i colori YAML tramite i Tag."""
        # 1. Rimuove tutti i tag esistenti prima di ricalcolarli
        for tag in ["chiave", "stringa", "numero_bool", "commento"]:
            self.text_area.tag_remove(tag, "1.0", tk.END)

        contenuto = self.text_area.get("1.0", "end-1c")

        # 2. Regole Regex per gli elementi YAML
        regole = [
            # Chiavi (es. "nome:" o "- nome:")
            (r"(?m)^[\s\-]*([a-zA-Z0-9_\-\.]+)\s*:", "chiave", 1),
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
        print(path_config_file)
        if (path_config_file is not None):
            self.carica_file(percorso=path_config_file)
        self.window.mainloop()

    def file_config_default(self, version):
        config_default = {
            'version': version,
            'credenziali': [
                    {
                    'customerid': 'customerid',
                    'username': 'username',
                    'password': 'password',
                    'alunni': {
                        'NOME_ALUNNO_A' : {
                            'tipo': 'smtp',
                            'param': 'EMAIL_STUDENTE'
                        },
                        'NOME_ALUNNO_B' : {
                            'tipo': 'html',
                            'param': '.'
                        },
                        'NOME_ALUNNO_C' : {
                            'tipo': 'screenshot',
                            'param': '.'
                        },
                        'NOME_ALUNNO_D' : {
                            'tipo': 'telegram',
                            'param': 'CHAT_ID'
                        }
                    }
                }
            ],
            'params_notifiche':{
                'html': {
                    'path': '.'
                },
                'smtp': {
                    'smtp_server': 'smtp.example.it',
                    'smtp_port': 465,
                    'smtp_username': 'Username',
                    'smtp_password': 'PaSsWoRd',
                    'destinatari': [
                        'EMAIL_GENITORE-TUTORE',
                        'EMAIL_ALTRI'
                        ],
                    'n_allegati': 0
                },
                'telegram': {
                    'BOT_TOKEN': 'TOKEN',
                    'CHAT_ID': 'ID',
                    'n_allegati': 0
                },
                'screenshot': {
                    'path': '.'
                }
            }
        }
        content_yaml = yaml.dump(config_default, sort_keys=False)
        content_yaml = """# GUIDA ALLA CONFIGURAZIONE
        # https://github.com/robyquin/axios-get/blob/master/docs/Configurazione.md
        # Questo file è scritto in YAML, se lo modifichi manualmente presta attenzione all'indentazione e alla sintassi specifica.
        # Il testo che segue il carattere # è un commento e quindi nell'esecuzione verrà ignorato\n\n""" + content_yaml

        content_yaml = re.sub(r'(version:.*)', '\\1 # Versione della release', content_yaml)
        content_yaml = re.sub(r'(credenziali:.*)', '\\1 # Gruppo credenziali: raccoglie informazioni per l\'accesso al portale, la definizione degli studenti e per ciascuno la propria configurazione di notifica', content_yaml)
        content_yaml = re.sub(r'(- customerid:.*)', '\\1 # CF Istituto/Cliente', content_yaml)
        content_yaml = re.sub(r'(\s+username:.*)', '\\1 # Codice Utente o mail personale', content_yaml)
        content_yaml = re.sub(r'(\s+alunni:.*)', '\\1 # Gruppo alunni: definisce nome studente, tipologia di notifica e relativi parametri', content_yaml)
        content_yaml = re.sub(r'(\s+NOME_ALUNNO_A:.*)', '\\1 # Inserisci qui il nome dello studente che trovi nel menu a tendina sul portale AxiosFamiglia', content_yaml)
        content_yaml = re.sub(r'(\s+tipo:.*)', "\\1 # Tipi di notifiche disponibili: html, screenshot, smtp, telegram", content_yaml)
        content_yaml = re.sub(r'(\s+param:.*)', "\\1 # Parametro caratteristico della notifica scelta [default: eredita il parametro dalla configurazione generale]", content_yaml)

        content_yaml = re.sub(r'(params_notifiche:.*)', '\\1 # Gruppo parametri globali di notifica: raccoglie informazioni generali per rendere possibile la tipologia di notifica', content_yaml)
        content_yaml = re.sub(r'(\s+(html|screenshot):.*)', '\\1 # Gruppo di configurazione globale per la notifica \\2', content_yaml)
        content_yaml = re.sub(r'(\s+(telegram):.*)', '\\1 # Gruppo di configurazione globale per la notifica \\2 (https://github.com/robyquin/axios-get/blob/master/docs/Telegram_token_bot.md)', content_yaml)
        content_yaml = re.sub(r'(\s+(smtp):.*)', '\\1 # Gruppo di configurazione globale per la notifica \\2 (https://github.com/robyquin/axios-get/blob/master/docs/SMTP_server.md)', content_yaml)
        content_yaml = re.sub(r'(\s+path:.*)', '\\1 # Specifica qui il percorso relativo o assoluto della cartella di destinazione', content_yaml)
        content_yaml = re.sub(r'(\s+n_allegati:.*)', '\\1 # Specifica il numero di screenshot da allegare alla notifica [>=0]', content_yaml)

        content_yaml = re.sub(r'(NOME_ALUNNO_[B-D]:.*)', '# \\1 # Inserisci qui il nome dello studente successivo che trovi nel menu', content_yaml)
        content_yaml = re.sub(r'(tipo: (html|screenshot|telegram))', '# \\1', content_yaml)
        content_yaml = re.sub(r'(param: (\.|CHAT_ID))', '# \\1', content_yaml)
        content_yaml = re.sub(r'(- EMAIL_ALTRI.*)', '# \\1 # Specifica, come un elenco, altri destinatari della email', content_yaml)
        return content_yaml

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
