#!python
"""
Modulo di rappresentazione del file YAML di configurazione.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

from typing import Literal
from pydantic import BaseModel, Field, model_validator


class ConfigurazioneAlunno(BaseModel):
    """
    Definizione della configurazione alunno
    """
    tipo: Literal['smtp', 'html', 'screenshot', 'telegram']
    param: str
    nome_alternativo: str | None = None


class RegistroAlunni(BaseModel):
    """
    Definizione del dizionario alunni
    """
    alunni: dict[str, ConfigurazioneAlunno]


class ConfigurazioneIstituto(BaseModel):
    """
    Definizione della lista configurazione degli istituti
    """
    customerid: str | int
    username: str | int
    password: str
    alunni: dict[str, ConfigurazioneAlunno]


class ConfigNotificaLocale(BaseModel):
    """
    Definizione della configurazione delle notifiche locali: Html e Screenshot
    """
    path: str


class ConfigNotificaSmtp(BaseModel):
    """
    Definizione della configurazione della notifica SMTP
    """
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    destinatari: list[str]
    n_allegati: int = Field(ge=0)


class ConfigNotificaTelegram(BaseModel):
    """
    Definizione della configurazione della notifica Telegram
    """
    BOT_TOKEN: str
    CHAT_ID: str | None = None
    n_allegati: int = Field(ge=0)


class ParamsNotifiche(BaseModel):
    """
    Definizione della configurazione dei parametri globali delle notifiche
    """
    html: ConfigNotificaLocale | None = None
    screenshot: ConfigNotificaLocale | None = None
    smtp: ConfigNotificaSmtp | None = None
    telegram: ConfigNotificaTelegram | None = None


class ConfigCredenzialiYaml(BaseModel):
    """
    Definizione della configurazione completa
    """
    version: str = Field(pattern=r"^\d+\.\d+\.\d+\w*$")
    credenziali: list[ConfigurazioneIstituto]
    params_notifiche: ParamsNotifiche

    @model_validator(mode='after')
    def verifica_coerenza_notifiche(self) -> 'ConfigCredenzialiYaml':
        """
        Verifica la coerenza trasversale dei parametri di configurazione.

        :return: ConfigCredenzialiYaml - Risultato dell'operazione
        :rtype: ConfigCredenzialiYaml

        :raises ValueError: Se un canale di notifica non è configurato
        """
        errori = []

        for credenziali_config in self.credenziali:
            for nome_alunno, config in credenziali_config.alunni.items():
                canale = config.tipo

                if getattr(self.params_notifiche, canale) is None:
                    errori.append(
                        f"L'alunno '{nome_alunno}' usa il tipo '{canale}', "
                        f"ma '{canale}' non è configurato in 'params_notifiche'."
                    )
        if errori:
            raise ValueError(" | ".join(errori))
        return self
