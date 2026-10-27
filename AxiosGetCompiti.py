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
            'destinatari': [
                'genitore1@example.it',
                'Alunno1@example.it'
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

        tipo_notifica = None
        if('tipo_notifica' in config.keys()):
            if (config['tipo_notifica'] == 'file_html'):
                tipo_notifica = notifica.NotificaFileHTML(DIR, os.path.join(DIR, "credenziali.yml"))
            elif (config['tipo_notifica'] == 'smtp'):
                tipo_notifica = notifica.NotificaMail(DIR, os.path.join(DIR, "credenziali.yml"))
            elif (config['tipo_notifica'] == 'telegram'):
                tipo_notifica = notifica.NotificaTelegram(DIR, os.path.join(DIR, "credenziali.yml"))
            elif (config['tipo_notifica'] == 'screenshot'):
                tipo_notifica = notifica.NotificaScreenShot(DIR, os.path.join(DIR, "credenziali.yml"))

        if (tipo_notifica is not None):
            try:
                axios = LibAxiosFamiglia(DIR, config['axios']['credenziali'], tipo_notifica)
                for alunno in config['axios']['alunni']:
                    axios.get_session_collabora(alunno)
                    axios.get_session_registrofamiglie(alunno)
            except Exception as e:
                print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
        else:
            print("Error: occorre configurare e selezionare un tipo di notifica", file=sys.stderr)
    else:
        try:
            file_config_default(DIR)
        except FileNotFoundError as e:
            print(f"File di configurazione non trovato! Creazione del file di default: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)
