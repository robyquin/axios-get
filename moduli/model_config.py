#!python
"""
Modulo di rappresentazione del file YAML di configurazione.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import re
from typing import Literal
from dataclasses import dataclass, asdict


@dataclass
class ConfigurazioneAlunno:
    """
    Definizione della configurazione alunno
    """
    tipo: Literal['smtp', 'html', 'screenshot', 'telegram']
    param: str
    nome_alternativo: str | None = None




@dataclass
class RegistroAlunni:
    """
    Definizione del dizionario alunni
    """
    alunni: dict[str, ConfigurazioneAlunno]


@dataclass
class ConfigurazioneIstituto:
    """
    Definizione della lista configurazione degli istituti
    """
    customerid: str | int
    username: str | int
    password: str
    alunni: dict[str, ConfigurazioneAlunno]

    def __post_init__(self):
        if isinstance(self.customerid, str) and not isinstance(self.customerid, int):
            raise TypeError("customerid deve essere una stringa o un intero")
        if isinstance(self.username, str) and not isinstance(self.username, int):
            raise TypeError("username deve essere una stringa o un intero")


@dataclass
class ConfigNotificaLocale:
    """
    Definizione della configurazione delle notifiche locali: Html e Screenshot
    """
    path: str


@dataclass
class ConfigNotificaSmtp:
    """
    Definizione della configurazione della notifica SMTP
    """
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    destinatari: list[str]
    n_allegati: int

    def __post_init__(self):
        if self.n_allegati < 0:
            raise ValueError("Numero di allegati deve essere >= 0")


@dataclass
class ConfigNotificaTelegram:
    """
    Definizione della configurazione della notifica Telegram
    """
    BOT_TOKEN: str
    n_allegati: int
    CHAT_ID: str | None = None

    def __post_init__(self):
        if self.n_allegati < 0:
            raise ValueError("Numero di allegati deve essere >= 0")
        if self.CHAT_ID is not None and not isinstance(self.CHAT_ID, str):
            raise TypeError("CHAT_ID deve essere una stringa o None")


@dataclass
class ParamsNotifiche:
    """
    Definizione della configurazione dei parametri globali delle notifiche
    """
    html: ConfigNotificaLocale | None = None
    screenshot: ConfigNotificaLocale | None = None
    smtp: ConfigNotificaSmtp | None = None
    telegram: ConfigNotificaTelegram | None = None

    def __post_init__(self):
        if self.html is not None and not isinstance(self.html, ConfigNotificaLocale):
            raise TypeError("html deve essere una stringa o None")
        if self.screenshot is not None and not isinstance(self.screenshot, ConfigNotificaLocale):
            raise TypeError("screenshot deve essere una stringa o None")
        if self.smtp is not None and not isinstance(self.smtp, ConfigNotificaSmtp):
            raise TypeError("smtp deve essere una ConfigNotificaSmtp o None")
        if self.telegram is not None and not isinstance(self.telegram, ConfigNotificaTelegram):
            raise TypeError("telegram deve essere una ConfigNotificaTelegram o None")


@dataclass
class ConfigCredenzialiYaml:
    """
    Definizione della configurazione completa
    """
    version: str
    credenziali: list[ConfigurazioneIstituto]
    params_notifiche: ParamsNotifiche

    def __post_init__(self):
        if not re.fullmatch(r"^\d+\.\d+\.\d+\w*$", self.version):
            raise ValueError("version non rispetta il formato")
        self.verifica_coerenza_notifiche()

    # @model_validator(mode='after')
    def verifica_coerenza_notifiche(self) -> 'ConfigCredenzialiYaml':
        """
        Verifica la coerenza trasversale dei parametri di configurazione.

        :return: ConfigCredenzialiYaml-Risultato dell'operazione
        :rtype: ConfigCredenzialiYaml

        :raises ValueError: Se un canale di notifica non è configurato
        """
        errori = []

        for credenziali_config in self.credenziali:
            for nome_alunno, config in credenziali_config['alunni'].items():
                canale = config['tipo']
                if dict(self.params_notifiche).get(canale, None) is None:
                    errori.append(
                        f"L'alunno '{nome_alunno}' usa il tipo '{canale}', "
                        f"ma '{canale}' non è configurato in 'params_notifiche'."
                    )
        if errori:
            raise ValueError(" | ".join(errori))
        return self

if __name__ == "__main__":
    import yaml
    with open("./credenziali.yml", 'r') as yml_f:
        config_default = yaml.safe_load(yml_f.read())
        ConfigCredenzialiYaml(**config_default)