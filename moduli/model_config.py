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
        
        if isinstance(self.tipo, str):
            if self.tipo not in ['smtp', 'html', 'screenshot', 'telegram']:
                raise ValueError(f"[ConfigurazioneAlunno].tipo = '{self.tipo}', ma deve essere una tra queste: 'smtp', 'html', 'screenshot', 'telegram'")
        else:
            raise TypeError(f"[ConfigurazioneAlunno].tipo `{type(self.tipo).__name__}`, ma deve essere una stringa")
        
        if not isinstance(self.param, str):
            raise TypeError(f"[ConfigurazioneAlunno].param `{type(self.param).__name__}`, ma deve essere una stringa")
        
        if self.nome_alternativo is not None and not isinstance(self.nome_alternativo, str):
            raise TypeError(f"[ConfigurazioneAlunno].nome_alternativo `{type(self.nome_alternativo).__name__}`, ma deve essere una stringa o null")


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
        if not isinstance(self.customerid, str) and not isinstance(self.customerid, int):
            raise TypeError(f"[ConfigurazioneIstituto].customerid `{type(self.customerid).__name__}`, ma deve essere una stringa o un intero")
        
        if not isinstance(self.username, str) and not isinstance(self.username, int):
            raise TypeError(f"[ConfigurazioneIstituto].username `{type(self.username).__name__}`, ma deve essere una stringa o un intero")

        if not isinstance(self.password, str):
            raise TypeError(f"[ConfigurazioneIstituto].password `{type(self.password).__name__}`, ma deve essere una stringa")
        
        for nome_alunno, config_alunno in self.alunni.items():
           ConfigurazioneAlunno(**dict(config_alunno))


@dataclass
class ConfigNotificaLocale:
    """
    Definizione della configurazione delle notifiche locali: Html e Screenshot
    """
    path: str

    def __post_init__(self):

        if not isinstance(self.path, str):
            raise TypeError(f"[ConfigNotificaLocale].path `{type(self.path).__name__}`, ma deve essere una stringa")


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

        if not isinstance(self.smtp_server, str):
            raise TypeError(f"[ConfigNotificaSmtp].smtp_server `{type(self.smtp_server).__name__}`, ma deve essere una stringa")

        if not isinstance(self.smtp_port, int):
            raise TypeError(f"[ConfigNotificaSmtp].smtp_port `{type(self.smtp_port).__name__}`, ma deve essere un intero")

        if not isinstance(self.smtp_username, str):
            raise TypeError(f"[ConfigNotificaSmtp].smtp_username `{type(self.smtp_username).__name__}`, ma deve essere una stringa")

        if not isinstance(self.smtp_password, str):
            raise TypeError(f"[ConfigNotificaSmtp].smtp_password `{type(self.smtp_password).__name__}`, ma deve essere una stringa")

        for d in self.destinatari:
            if not isinstance(d, str):
                raise TypeError(f"[ConfigNotificaSmtp].destinatario ==> {d} `{type(self.d).__name__}`, ma deve essere una stringa")
            else:
                if ('@' not in d):
                    raise ValueError(f"[ConfigNotificaSmtp].destinatario ==> {d} non è un indirizzo email")
        
        if isinstance(self.n_allegati, int):
            if self.n_allegati < 0:
                raise ValueError("[ConfigNotificaSmtp].n_allegati deve essere >= 0")
        else:
            raise TypeError(f"[ConfigNotificaSmtp].n_allegati `{type(self.n_allegati).__name__}`, ma deve essere un intero")


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
            raise TypeError(f"[ConfigNotificaTelegram].BOT_TOKEN `{type(self.BOT_TOKEN).__name__}`, ma deve essere una stringa")
        
        if isinstance(self.n_allegati, int):
            if self.n_allegati < 0:
                raise ValueError("[ConfigNotificaTelegram].n_allegati deve essere >= 0")
        else:
            raise TypeError(f"[ConfigNotificaTelegram].n_allegati `{type(self.n_allegati).__name__}`, ma deve essere un intero")
        
        if self.CHAT_ID is not None and not isinstance(self.CHAT_ID, str):
            raise TypeError(f"[ConfigNotificaTelegram].CHAT_ID `{type(self.CHAT_ID).__name__}`, ma deve essere una stringa o null")


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
            raise TypeError(f"[ParamsNotifiche].html `{type(self.html).__name__}`, ma deve essere una ConfigNotificaLocale o null")
        elif isinstance(self.html, dict):
            ConfigNotificaLocale(**dict(self.html))

        if self.screenshot is not None and not isinstance(self.screenshot, dict):
            raise TypeError(f"[ParamsNotifiche].screenshot `{type(self.screenshot).__name__}`, ma deve essere una ConfigNotificaLocale o null")
        elif isinstance(self.screenshot, dict):
            ConfigNotificaLocale(**dict(self.screenshot))
        
        if self.smtp is not None and not isinstance(self.smtp, dict):
            raise TypeError(f"[ParamsNotifiche].smtp `{type(self.smtp).__name__}`, ma deve essere una ConfigNotificaSmtp o null")
        elif isinstance(self.smtp, dict):
            ConfigNotificaSmtp(**dict(self.smtp))
        
        if self.telegram is not None and not isinstance(self.telegram, dict):
            TypeError(f"[ParamsNotifiche].telegram `{type(self.telegram).__name__}`, ma deve essere una ConfigNotificaTelegram o null")
        elif isinstance(self.telegram, dict):
            ConfigNotificaTelegram(**dict(self.telegram))


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
