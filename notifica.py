#!python
"""
Gestore di Notifiche.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

from datetime import datetime

import smtplib
import ssl
from email.message import EmailMessage

import yaml

class Notifica():
    """
    Classe di definizione delle Notifiche

    :param path_config: percorso al file di configurazione YAML
    :type path_config: str
    """
    def __init__(self, path_config: str) -> None:
        with open(path_config, "r", encoding="utf-8") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def send_notifica(self, html: str) -> None:
        """
        Definisce il mezzo della notifica
        
        :param html: corpo del messaggio di notifica
        :type html: str
        """
        pass

class NotificaMail(Notifica):
    """
    Classe di definizione delle Notifiche Email

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità 
    configurando il client SMTP.
    """
    def send_notifica(self, html: str) -> None:
        oggi = datetime.strftime(datetime.now(), "%d/%m/%Y")

        # 1. Configurazione dei parametri del server e delle credenziali
        smtp_server = self.config['smtp']['smtp_server']
        port = self.config['smtp']['smtp_port']
        username = self.config['smtp']['smtp_username']
        password = self.config['smtp']['smtp_password']

        sender_email = self.config['smtp']['mittente']
        receiver_email = self.config['smtp']['destinatari']

        # 2. Creazione del contenuto dell'email
        msg = EmailMessage()
        msg["Subject"] = "Diario Axios - "+oggi
        msg["From"] = sender_email
        msg["To"] = ", ".join(receiver_email)
        msg.set_content(html, subtype='html')

        # 3. Creazione di un contesto SSL sicuro di default
        context = ssl.create_default_context()
        context.set_ciphers('HIGH:!DH:!aNULL@SECLEVEL=1')

        # 4. Connessione al server e invio del messaggio
        try:
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)
            print("Email inviata con successo!\n---")
        except Exception as e:
            print(f"Si è verificato un errore durante l'invio: {e}\n---")
