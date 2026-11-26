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
    tipo: str | None = None
    param: str | None = None
    nome_alternativo: str | None = None

    def __post_init__(self):

        if (self.tipo is not None):
            if (isinstance(self.tipo, str)):
                if (self.tipo not in ['smtp', 'html', 'screenshot', 'telegram']):
                    raise ValueError(f"[ConfigurazioneAlunno].tipo = '{self.tipo}', ma deve essere una tra queste: 'smtp', 'html', 'screenshot', 'telegram'")
            else:
                raise TypeError(f"[ConfigurazioneAlunno].tipo `{type(self.tipo).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigurazioneAlunno].tipo campo mancate, ma obbligatorio!")

        if (self.param is not None):
            if (not isinstance(self.param, str)):
                raise TypeError(f"[ConfigurazioneAlunno].param `{type(self.param).__name__}`, ma deve essere una stringa")
            else:
                if (self.tipo == 'smtp' and not re.fullmatch(r"^[\w\.]+@[\w\.]+$", self.param)):
                    raise ValueError(f"[ConfigurazioneAlunno].param ==> {self.param} non sembra essere un indirizzo email")

        else:
            raise TypeError("[ConfigurazioneAlunno].param campo mancate, ma obbligatorio!")

        if (self.nome_alternativo is not None and not isinstance(self.nome_alternativo, str)):
            raise TypeError(f"[ConfigurazioneAlunno].nome_alternativo `{type(self.nome_alternativo).__name__}`, ma deve essere una stringa o null")


@dataclass
class ConfigurazioneIstituto:
    """
    Definizione della lista configurazione degli istituti
    """
    customerid: str | int | None = None
    username: str | int | None = None
    password: str | None = None
    alunni: dict[str, ConfigurazioneAlunno] | None = None

    def __post_init__(self):

        if (self.customerid is not None):
            if (not isinstance(self.customerid, str) and not isinstance(self.customerid, int)):
                raise TypeError(f"[ConfigurazioneIstituto].customerid `{type(self.customerid).__name__}`, ma deve essere una stringa o un intero")
        else:
            raise TypeError("[ConfigurazioneIstituto].customerid campo mancate, ma obbligatorio!")

        if (self.username is not None):
            if (not isinstance(self.username, str) and not isinstance(self.username, int)):
                raise TypeError(f"[ConfigurazioneIstituto].username `{type(self.username).__name__}`, ma deve essere una stringa o un intero")
        else:
            raise TypeError("[ConfigurazioneIstituto].username campo mancate, ma obbligatorio!")

        if (self.password is not None):
            if (not isinstance(self.password, str)):
                raise TypeError(f"[ConfigurazioneIstituto].password `{type(self.password).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigurazioneIstituto].password campo mancate, ma obbligatorio!")

        if (self.alunni is not None):
            if (isinstance(self.alunni, dict)):
                if (len(self.alunni.items()) > 0):
                    for nome_alunno, config_alunno in self.alunni.items():
                        ConfigurazioneAlunno(**dict(config_alunno))
                else:
                    raise ValueError(f"[ConfigurazioneIstituto].alunni `{type(self.alunni).__name__}` vuoto, deve contenere almeno una configurazione alunno")
            else:
                raise TypeError(f"[ConfigurazioneIstituto].alunni `{type(self.alunni).__name__}`, ma deve essere una dizionario")
        else:
            raise TypeError("[ConfigurazioneIstituto].alunni campo mancate, ma obbligatorio!")


@dataclass
class ConfigNotificaLocale:
    """
    Definizione della configurazione delle notifiche locali: Html e Screenshot
    """
    path: str | None = None

    def __post_init__(self):

        if (self.path is not None):
            if (not isinstance(self.path, str)):
                raise TypeError(f"[ConfigNotificaLocale].path `{type(self.path).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigNotificaLocale].path campo mancate, ma obbligatorio!")


@dataclass
class ConfigNotificaSmtp:
    """
    Definizione della configurazione della notifica SMTP
    """
    smtp_server: str | None = None
    smtp_port: int | None = None
    smtp_username: str | None = None
    smtp_password: str | None = None
    destinatari: list[str] | None = None
    n_allegati: int | None = None

    def __post_init__(self):

        if (self.smtp_server is not None):
            if (not isinstance(self.smtp_server, str)):
                raise TypeError(f"[ConfigNotificaSmtp].smtp_server `{type(self.smtp_server).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigNotificaSmtp].smtp_server campo mancate, ma obbligatorio!")

        if (self.smtp_port is not None):
            if (not isinstance(self.smtp_port, int)):
                raise TypeError(f"[ConfigNotificaSmtp].smtp_port `{type(self.smtp_port).__name__}`, ma deve essere un intero")
        else:
            raise TypeError("[ConfigNotificaSmtp].smtp_port campo mancate, ma obbligatorio!")

        if (self.smtp_username is not None):
            if (not isinstance(self.smtp_username, str)):
                raise TypeError(f"[ConfigNotificaSmtp].smtp_username `{type(self.smtp_username).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigNotificaSmtp].smtp_username campo mancate, ma obbligatorio!")

        if (self.smtp_password is not None):
            if (not isinstance(self.smtp_password, str)):
                raise TypeError(f"[ConfigNotificaSmtp].smtp_password `{type(self.smtp_password).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigNotificaSmtp].smtp_password campo mancate, ma obbligatorio!")

        if (self.destinatari is not None):
            if (isinstance(self.destinatari, list)):
                for d in self.destinatari:
                    if (not isinstance(d, str)):
                        raise TypeError(f"[ConfigNotificaSmtp].destinatario ==> {d} `{type(d).__name__}`, ma deve essere una stringa")
                    else:
                        if (not re.fullmatch(r"^[\w\.]+@[\w\.]+$", d)):
                            raise ValueError(f"[ConfigNotificaSmtp].destinatario ==> {d} non sembra essere un indirizzo email")
            else:
                raise TypeError(f"[ConfigNotificaSmtp].destinatari `{type(self.destinatari).__name__}`, ma deve essere una lista")
        else:
            raise TypeError("[ConfigNotificaSmtp].destinatari campo mancate, ma obbligatorio!")

        if (self.n_allegati is not None):
            if (isinstance(self.n_allegati, int)):
                if (self.n_allegati < 0):
                    raise ValueError("[ConfigNotificaSmtp].n_allegati deve essere >= 0")
            else:
                raise TypeError(f"[ConfigNotificaSmtp].n_allegati `{type(self.n_allegati).__name__}`, ma deve essere un intero")
        else:
            raise TypeError("[ConfigNotificaSmtp].n_allegati campo mancate, ma obbligatorio!")


@dataclass
class ConfigNotificaTelegram:
    """
    Definizione della configurazione della notifica Telegram
    """
    BOT_TOKEN: str | None = None
    n_allegati: int | None = None
    CHAT_ID: str | None = None

    def __post_init__(self):

        if (self.BOT_TOKEN is not None):
            if (not isinstance(self.BOT_TOKEN, str)):
                raise TypeError(f"[ConfigNotificaTelegram].BOT_TOKEN `{type(self.BOT_TOKEN).__name__}`, ma deve essere una stringa")
        else:
            raise TypeError("[ConfigNotificaTelegram].BOT_TOKEN campo mancate, ma obbligatorio!")

        if (self.n_allegati is not None):
            if (isinstance(self.n_allegati, int)):
                if (self.n_allegati < 0):
                    raise ValueError("[ConfigNotificaTelegram].n_allegati deve essere >= 0")
            else:
                raise TypeError(f"[ConfigNotificaTelegram].n_allegati `{type(self.n_allegati).__name__}`, ma deve essere un intero")
        else:
            raise TypeError("[ConfigNotificaTelegram].n_allegati campo mancate, ma obbligatorio!")

        if (self.CHAT_ID is not None and not isinstance(self.CHAT_ID, str)):
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

        if (self.html is not None and not isinstance(self.html, dict)):
            raise TypeError(f"[ParamsNotifiche].html `{type(self.html).__name__}`, ma deve essere una ConfigNotificaLocale o null")
        elif (isinstance(self.html, dict)):
            ConfigNotificaLocale(**dict(self.html))

        if (self.screenshot is not None and not isinstance(self.screenshot, dict)):
            raise TypeError(f"[ParamsNotifiche].screenshot `{type(self.screenshot).__name__}`, ma deve essere una ConfigNotificaLocale o null")
        elif (isinstance(self.screenshot, dict)):
            ConfigNotificaLocale(**dict(self.screenshot))

        if (self.smtp is not None and not isinstance(self.smtp, dict)):
            raise TypeError(f"[ParamsNotifiche].smtp `{type(self.smtp).__name__}`, ma deve essere una ConfigNotificaSmtp o null")
        elif (isinstance(self.smtp, dict)):
            ConfigNotificaSmtp(**dict(self.smtp))

        if (self.telegram is not None and not isinstance(self.telegram, dict)):
            raise TypeError(f"[ParamsNotifiche].telegram `{type(self.telegram).__name__}`, ma deve essere una ConfigNotificaTelegram o null")
        elif (isinstance(self.telegram, dict)):
            ConfigNotificaTelegram(**dict(self.telegram))

        if (self.html is None and self.screenshot is None and self.smtp is None and self.telegram is None):
            raise ValueError("[ParamsNotifiche] deve essere presente almeno una configurazione tra queste: 'html', 'screenshot', 'smtp', 'telegram'")


@dataclass
class ConfigCredenzialiYaml:
    """
    Definizione della configurazione completa
    """
    version: str | None = None
    credenziali: list[ConfigurazioneIstituto] | None = None
    params_notifiche: ParamsNotifiche | None = None

    def __post_init__(self):

        if (isinstance(self.version, str)):
            if (not re.fullmatch(r"^\d+\.\d+\.\d+\w*$", self.version)):
                raise ValueError("[ConfigCredenzialiYaml].version non rispetta il formato [int].[int].[int]")
        else:
            raise TypeError(f"[ConfigCredenzialiYaml].version `{type(self.version).__name__}`, ma deve essere una stringa")

        if (self.credenziali is not None):
            for c in self.credenziali:
                ConfigurazioneIstituto(**dict(c))
        else:
            raise TypeError("[ConfigCredenzialiYaml].credenziali campo mancate, ma obbligatorio!")

        if (self.params_notifiche is not None):
            ParamsNotifiche(**dict(self.params_notifiche))
        else:
            raise TypeError("[ConfigCredenzialiYaml].params_notifiche campo mancate, ma obbligatorio!")

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
                if (dict(self.params_notifiche).get(canale, None) is None):
                    errori.append(
                        f"L'alunno '{nome_alunno}' usa il tipo '{canale}', "
                        f"ma '{canale}' non è configurato in 'params_notifiche'."
                    )
        if (errori):
            raise ValueError(" | ".join(errori))
        return self


if (__name__ == "__main__"):
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
