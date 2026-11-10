#!python
"""
AxiosGetCompiti.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

__version__ = "1.1.0"

import sys
import os
from pathlib import Path

import yaml

from moduli.lib_axios_famiglia import LibAxiosFamiglia
import moduli.lib_notifica as notifica

def file_config_default(DIR: str) -> None:
    """
    Crea un file di default iniziale

    :param DIR: percorso di salvataggio log e error
    :type DIR: str

    :raises FileNotFoundError: file non trovato.
    """
    config_default = {
        'version': __version__,
        'credenziali': {
            'customerid': 'customerid',
            'username': 'username',
            'password': 'password',
            'alunni': {
                'NOME_ALUNNO_A' : {
                    'tipo': 'html',
                    'param': '.'
                }
            }
        },
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
                    'tutore@example.it'
                    ],
                'n_allegati': 0
            },
            'telegram': {
                'BOT_TOKEN': 'TOKEN',
                'n_allegati': 0
            },
            'screenshot': {
                'path': '.'
            }
        }
    }
    try:
        if (os.path.exists(os.path.join(DIR, "schedula_axios-get.xml_tmp")) and getattr(sys, 'frozen', False)):
            content = ""
            with open(os.path.join(DIR, "schedula_axios-get.xml_tmp"), "r", encoding="utf-16") as file_schedule:
                content = file_schedule.read()
            content = content.replace("<Command>Axios-Get</Command>", f"<Command>{str(os.path.abspath(sys.executable))}</Command>")
            content = content.replace("<WorkingDirectory>Axios-Get</WorkingDirectory>", f"<WorkingDirectory>{str(os.path.dirname(sys.executable))}</WorkingDirectory>")
            with open(os.path.join(DIR, "schedula_axios-get.xml"), "w", encoding="utf-16") as file_schedule:
                content = file_schedule.write(content)
                os.remove(os.path.join(DIR, "schedula_axios-get.xml_tmp"))
        with open(os.path.join(DIR, "credenziali_default.yml"), "w", encoding="utf-8") as file_config:
            file_config.write(yaml.dump(config_default, sort_keys=False))
    except Exception as e:
        print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
    raise FileNotFoundError(os.path.join(DIR, "credenziali_default.yml"))

if __name__ == "__main__":

    if getattr(sys, 'frozen', False):
        # Se l'applicazione è compilata con PyInstaller
        DIR=str(os.path.dirname(sys.executable))
        if(os.path.exists(os.path.join(DIR, "errori.txt"))):
            os.remove(os.path.join(DIR, "errori.txt"))
        if(os.path.exists(os.path.join(DIR, "log.txt"))):
            os.remove(os.path.join(DIR, "log.txt"))
        sys.stderr = open(os.path.join(DIR, "errori.txt"), "a", encoding="utf-8")
        sys.stdout = open(os.path.join(DIR, "log.txt"), "a", encoding="utf-8")
    else:
        DIR=str(Path(os.path.dirname(__file__)).absolute())

    if (os.path.exists(os.path.join(DIR, "credenziali.yml"))):
        with open(os.path.join(DIR, "credenziali.yml"), "r", encoding="utf-8") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        LibAxiosFamiglia(DIR, config)
    else:
        try:
            file_config_default(DIR)
        except FileNotFoundError as e:
            print(f"File di configurazione non trovato! Creazione del file di default: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
