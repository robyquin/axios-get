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
else:
    DIR=str(Path(os.path.dirname(__file__)).absolute())+os.path.sep


if __name__ == "__main__":

    with open(DIR+"credenziali.yml", "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    tipo_notifica = None
    if('tipo_notifica' in config.keys()):
        if (config['tipo_notifica'] == 'file_html'):
            tipo_notifica = notifica.NotificaFileHTML(DIR+"credenziali.yml")
        elif (config['tipo_notifica'] == 'smtp'):
            tipo_notifica = notifica.NotificaMail(DIR+"credenziali.yml")

    if (tipo_notifica is not None):
        axios = LibAxiosFamiglia(config['axios']['credenziali'], tipo_notifica)
        for alunno in config['axios']['alunni']:
            axios.get_session_registrofamiglie(alunno)
    else:
        print("Error: occorre configurare e selezionare un tipo di notifica")
