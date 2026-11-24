#!python
"""
Modulo di rappresentazione del file YAML di configurazione.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import re
from dataclasses import dataclass


@dataclass
class ConfigurazioneAlunno:
    """
    Definizione della configurazione alunno
    """
    tipo: str
    param: str
    nome_alternativo: str | None = None

    def __post_init__(self):
        if self.nome_alternativo is not None and not isinstance(self.nome_alternativo, str):
            raise ValueError("nome_alternativo deve essere una stringa o None")
        if isinstance(self.tipo, str):
            if self.tipo not in ['smtp', 'html', 'screenshot', 'telegram']:
                raise ValueError("il valore tipo deve essere una tra queste: 'smtp', 'html', 'screenshot', 'telegram'")
        else:
            raise ValueError("il valore tipo deve essere una stringa tra queste: 'smtp', 'html', 'screenshot', 'telegram'")


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
            raise ValueError("customerid deve essere una stringa o un intero")
        if isinstance(self.username, str) and not isinstance(self.username, int):
            raise ValueError("username deve essere una stringa o un intero")
        for nome_alunno, config_alunno in self.alunni.items():
           ConfigurazioneAlunno(**dict(config_alunno))


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
        if not isinstance(self.BOT_TOKEN, str):
            raise ValueError("BOT_TOKEN deve essere una stringa")
        if self.n_allegati < 0:
            raise ValueError("Numero di allegati deve essere >= 0")
        if self.CHAT_ID is not None and not isinstance(self.CHAT_ID, str):
            raise ValueError("CHAT_ID deve essere una stringa o None")


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
        if self.html is not None and not isinstance(self.html, dict):
            raise ValueError("html deve essere una ConfigNotificaLocale o None")
        if self.screenshot is not None and not isinstance(self.screenshot, dict):
            raise ValueError("screenshot deve essere una ConfigNotificaLocale o None")
        if self.smtp is not None and not isinstance(self.smtp, dict):
            raise ValueError("smtp deve essere una ConfigNotificaSmtp o None")
        if self.telegram is not None and not isinstance(self.telegram, dict):
            raise ValueError("telegram deve essere una ConfigNotificaTelegram o None")


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
        for c in self.credenziali:
            ConfigurazioneIstituto(**dict(c))
        ParamsNotifiche(**dict(self.params_notifiche))
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
        try:
            ConfigCredenzialiYaml(**config_default)
        except ValueError as e:
            print(f"ValueErrore: {e} ✖")
        except TypeError as e:
            print(f"TypeError: {e} ✖")
        except Exception as e:
            print(f"Errore: {e} ✖")
