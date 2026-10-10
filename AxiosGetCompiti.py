#!python
"""
AxiosGetCompiti.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import sys
import os
from pathlib import Path

import yaml

from LibAxiosFamiglia import LibAxiosFamiglia
import notifica

if getattr(sys, 'frozen', False):
    # Se l'applicazione è compilata con PyInstaller
    DIR=str(os.path.dirname(sys.executable))+os.path.sep
    sys.stderr = open("errori.txt", "w", encoding="utf-8")
    sys.stdout = open("log.txt", "w", encoding="utf-8")
else:
    DIR=str(Path(os.path.dirname(__file__)).absolute())+os.path.sep

def file_config_default():
    """
    Crea un file di default iniziale
    """
    config_default = {
        'axios': {
            'credenziali': {
                'customerid': 'customerid',
                'username': 'username',
                'password': 'password'
            },
            'alunni': [
                'NOME_ALUNNO'
                ]
        },
        'tipo_notifica': 'file_html',
        'file_html': {
            'path': '.'
        },
        'smtp': {
            'smtp_server': 'smtp.example.it',
            'smtp_port': 465,
            'smtp_username': 'Username',
            'smtp_password': 'PaSsWoRd',
            'mittente': 'Genitore <genitore1@example.it>',
            'destinatari': [
                'genitore1@example.it',
                'Alunno1@example.it'
                ]
        }
    }
    try:
        with open(DIR+"credenziali_default.yml", "w", encoding="utf-8") as file_config:
            file_config.write(yaml.dump(config_default, sort_keys=False))
    except Exception as e:
        print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
    raise FileNotFoundError(DIR+"credenziali_default.yml")

if __name__ == "__main__":

    if (os.path.exists(DIR+"credenziali.yml")):
        with open(DIR+"credenziali.yml", "r", encoding="utf-8") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        tipo_notifica = None
        if('tipo_notifica' in config.keys()):
            if (config['tipo_notifica'] == 'file_html'):
                tipo_notifica = notifica.NotificaFileHTML(DIR+"credenziali.yml")
            elif (config['tipo_notifica'] == 'smtp'):
                tipo_notifica = notifica.NotificaMail(DIR+"credenziali.yml")

        if (tipo_notifica is not None):
            try:
                axios = LibAxiosFamiglia(config['axios']['credenziali'], tipo_notifica)
                for alunno in config['axios']['alunni']:
                    axios.get_session_registrofamiglie(alunno)
            except Exception as e:
                print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
        else:
            print("Error: occorre configurare e selezionare un tipo di notifica")
    else:
        try:
            file_config_default()
        except FileNotFoundError as e:
            print(f"File di configurazione non trovato! Creazione del file di default: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
