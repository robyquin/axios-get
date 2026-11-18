#!python
"""
AxiosGetCompiti GUI.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import sys
import os
from pathlib import Path
import re

import tkinter as tk
from tkinter import ttk, scrolledtext
from queue import Queue
import threading
import argparse

from moduli.logging_config import logging, log

from AxiosGetCompiti import run_axios_get_compiti
from AxiosGetCompitiConfigurator import ApplicationGUIConfigurator

logger = log

class GuiHandler(logging.Handler):

    def __init__(self, event_queue):
        super().__init__()
        self.event_queue = event_queue

    def emit(self, record):
        try:
            self.event_queue.put({
                "level": record.levelname,
                "message": self.format(record)
            })
        except Exception:
            self.handleError(record)

class ApplicationGUI:

    def __init__(self, logger, run_function):
        self.logger = logger
        self.run_function = run_function

        # Coda per ricevere i messaggi
        self.event_queue = Queue()

        # Finestra grid 4x3
        self.root = tk.Tk()

        ttk.Style().theme_use("clam")
        self.root.title("Axios-get GUI")
        self.root.geometry("800x400")

        # Pulsante avvio
        self.start_button = ttk.Button(self.root, text="Avvia", command=self.start)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        # Pulsante configuratore
        self.config_button = ttk.Button(self.root, text="Configurazione", command=self.avvia_configuratore)
        self.config_button.grid(row=1, column=0, padx=10, pady=10)

        # Area messaggi
        self.log_text = scrolledtext.ScrolledText(self.root, font=("Consolas", 10), wrap=tk.WORD, width=40, height=10)
        self.log_text.grid(row=0, column=1, columnspan=2, rowspan=3, sticky="ewns", padx=10, pady=10)
        self.log_text.tag_config("INFO", foreground="black")
        self.log_text.tag_config("WARNING", foreground="orange")
        self.log_text.tag_config("ERROR", foreground="red")
        self.log_text.tag_config("DEBUG", foreground="gray")
        self.log_text.tag_config("Bold", foreground="#569cd6", font=("Consolas", 10, "bold")) # Blu
        self.log_text.config(state="disabled")

        self.label_credit = tk.Text(self.root, font=("Consolas", 8), wrap=tk.WORD, relief="flat", bd=0, height=4, bg=self.root.cget("bg"))
        self.label_credit.tag_config("Bold", foreground="#569cd6", font=("Consolas", 8, "bold"))
        self.label_credit.insert("end","Axios-get\n", "Bold")
        self.label_credit.insert("end","Autore: Roberto Quintiliani\n")
        self.label_credit.insert("end","Licenza: Open Source (MIT)\n")
        self.label_credit.insert("end","Progetto: https://github.com/robyquin/axios-get")
        self.label_credit.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        self.label_credit.config(state="disabled")

        self.status_label = tk.Label(self.root, text="Pronto", anchor="w", relief="sunken", padx=5, fg="green")
        self.status_label.grid(row=4, column=0, columnspan=3, sticky="ew")

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        # Handler per intercettare il logger
        self.gui_handler = GuiHandler(self.event_queue)
        self.gui_handler.setLevel("INFO")
        self.logger.addHandler(self.gui_handler)

        # Controllo periodico della coda
        self.root.after(100, self.check_events)

    def start(self):

        self.start_button.config(state="disabled")
        self.status_label.config(text="Elaborazione in corso...", fg="orange")

        self.log_text.config(state="normal")
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state="disabled")

        threading.Thread(
            target=self.run_worker,
            daemon=True
        ).start()

    def run_worker(self):

        success = False

        try:
            self.run_function()
            success = True
        except Exception:
            self.logger.exception(
                "Errore durante l'elaborazione"
            )
        finally:
            self.event_queue.put({
                "type": "finished",
                "success": success
            })

    def check_events(self):

        while not self.event_queue.empty():
            event = self.event_queue.get()
            # Fine elaborazione
            if event.get("type") == "finished":
                self.start_button.config(state="normal")
                if event["success"]:
                    self.status_label.config(text="Elaborazione completata", fg="green")
                else:
                    self.status_label.config(text="Elaborazione terminata con errori", fg="red")
                continue

            # Messaggi del logger
            level = event["level"]
            message = event["message"]

            self.log_text.config(state="normal")

            inizio_riga = self.log_text.index("end-1c linestart")
            # fine_riga = self.log_text.index("end-1c lineend")

            self.log_text.insert(
                "end",
                f"[{level}] {message}\n",
                level
            )

            regole = [
                (r"\*\*([a-zA-Z0-9_\-\.\s]+)\*\*", "Bold", 1),
            ]

            for pattern, tag, gruppo in regole:
                for match in re.finditer(pattern, f"[{level}] {message}\n", re.MULTILINE):
                    start = f"{inizio_riga} + {match.start(gruppo)} chars"
                    end = f"{inizio_riga} + {match.end(gruppo)} chars"
                    self.log_text.tag_add(tag, start, end)

            self.log_text.see("end")
            self.log_text.config(state="disabled")

        self.root.after(100, self.check_events)

    def run(self):
        self.root.mainloop()

    def avvia_configuratore(self):
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

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--silent",
        action="store_true",
        help="Esegue senza interfaccia grafica"
    )

    args = parser.parse_args()

    if (getattr(sys, 'frozen', False)):
        # Se l'applicazione è compilata con PyInstaller
        DIR=str(os.path.dirname(sys.executable))
        if (os.path.exists(os.path.join(DIR, "schedula_axios-get.xml_tmp"))):
            content = ""
            with open(os.path.join(DIR, "schedula_axios-get.xml_tmp"), "r", encoding="utf-16") as file_schedule:
                content = file_schedule.read()
            content = content.replace("<Command>Axios-Get</Command>", f"<Command>{str(os.path.abspath(sys.executable))}</Command>")
            content = content.replace("<WorkingDirectory>Axios-Get</WorkingDirectory>", f"<WorkingDirectory>{str(os.path.dirname(sys.executable))}</WorkingDirectory>")
            with open(os.path.join(DIR, "schedula_axios-get.xml"), "w", encoding="utf-16") as file_schedule:
                content = file_schedule.write(content)
                os.remove(os.path.join(DIR, "schedula_axios-get.xml_tmp"))
    else:
        DIR=str(Path(os.path.dirname(__file__)).absolute())

    # Handler file senza colori
    file_handler = logging.FileHandler(filename=os.path.join(DIR, "output.log"), mode="w", encoding='utf-8')
    file_formatter = logging.Formatter("%(asctime)-15s [%(levelname)s] %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    if (args.silent):
        logger.info("Avvio in modalità silent")
        run_axios_get_compiti(DIR)
        logger.info("Elaborazione completata")
        return 0
    else:

        gui = ApplicationGUI(
            logger=logger,
            run_function=lambda: run_axios_get_compiti(DIR)
        )

        gui.run()
        return 0

if __name__ == "__main__":

    try:
        sys.exit(main())
    except Exception:
        logger.exception("Errore fatale applicazione")
        sys.exit(1)
