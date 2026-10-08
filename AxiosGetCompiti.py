#!python
"""
AxiosGetCompiti.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import os
from pathlib import Path

import yaml

from LibAxiosFamiglia import LibAxiosFamiglia
import notifica

DIR=str(Path(os.path.dirname(__file__)).absolute())+os.path.sep

if __name__ == "__main__":

    with open(DIR+"credenziali.yml", "r", encoding="utf-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    axios = LibAxiosFamiglia(config['axios']['credenziali'], notifica.NotificaMail(DIR+"credenziali.yml"))
    for alunno in config['axios']['alunni']:
        axios.get_session_registrofamiglie(alunno)
