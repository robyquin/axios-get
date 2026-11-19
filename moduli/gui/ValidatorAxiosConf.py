#!python
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class ConfigurazioneAlunno(BaseModel):
    tipo: Literal['smtp', 'html', 'screenshot', 'telegram']
    param: str
    nome_alternativo: str | None = None

class RegistroAlunni(BaseModel):
    alunni: dict[str, ConfigurazioneAlunno]

class ConfigurazioneIstituto(BaseModel):
    customerid: str
    username: str
    password: str
    alunni: dict[str, ConfigurazioneAlunno]

class ConfigNotificaLocale(BaseModel):
    path: str

class ConfigNotificaSmtp(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    destinatari: list[str]
    n_allegati: int = Field(ge=0)

class ConfigNotificaTelegram(BaseModel):
    BOT_TOKEN: str
    CHAT_ID: str
    n_allegati: int = Field(ge=0)

class ParamsNotifiche(BaseModel):
    html: ConfigNotificaLocale | None = None
    screenshot: ConfigNotificaLocale | None = None
    smtp: ConfigNotificaSmtp | None = None
    telegram: ConfigNotificaTelegram | None = None

class ConfigCredenzialiYaml(BaseModel):
    version: str = Field(pattern=r"^\d+\.\d+\.\d+\w*$")
    credenziali: list[ConfigurazioneIstituto]
    params_notifiche: ParamsNotifiche

    @model_validator(mode='after')
    def verifica_coerenza_notifiche(self) -> 'ConfigCredenzialiYaml':
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

# modello = ConfigCredenzialiYaml.model_validate(config_default)
# print(modello.model_dump())