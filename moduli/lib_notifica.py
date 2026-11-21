#!python
"""
Gestore di Notifiche.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import os
import re
from datetime import datetime

import smtplib
import ssl
from email.message import EmailMessage

import requests

from .lib_screenshot import ScreenShot
from .logging_config import log


class Notifica():
    """
    Classe di definizione delle Notifiche

    :param DIR: percorso di salvataggio log e error
    :type DIR: str
    :param config: dizionario di configurazione notifica
    :type config: dict
    :param parametro: parametro specifico per l'alunno
    :type parametro: int | str
    """
    def __init__(self, DIR: str, config: dict, parametro: int | str) -> None:
        self.DIR = DIR
        self.config = config
        self.param = parametro

    def send_notifica(self, html: str, alunno: str) -> None:
        """
        Definisce il mezzo della notifica

        :param html: corpo del messaggio di notifica
        :type html: str
        :param alunno: nome dell'alunno/a
        :type alunno: str
        """
        pass


class NotificaFileHTML(Notifica):
    """
    Classe di definizione delle Notifiche FileHTML

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità
    salvando il file nel absolute_path specifico.
    """
    def send_notifica(self, html: str, alunno: str) -> None:
        # 1. Configurazione dei parametri di collocazione
        path_file = self.param
        absolute_path = os.path.join(path_file, "compiti_" + alunno + ".html")

        # 2. Salvataggio del contenuto
        try:
            # 'with' assicura che il file venga chiuso automaticamente alla fine,
            # anche se si verifica un errore durante la scrittura.
            with open(absolute_path, "w", encoding="utf - 8") as file:
                file.write(html)
            log.info(f"Notifica Html salvata con successo: {absolute_path}")
        except Exception as e:
            raise RuntimeError(f"NotificaFileHTML - {e}") from e


class NotificaMail(Notifica):
    """
    Classe di definizione delle Notifiche Email

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità
    configurando il client SMTP.
    """
    def send_notifica(self, html: str, alunno: str) -> None:
        oggi = datetime.strftime(datetime.now(), "%d/%m/%Y")

        # 1. Configurazione dei parametri del server e delle credenziali
        smtp_server = self.config['smtp']['smtp_server']
        port = self.config['smtp']['smtp_port']
        username = self.config['smtp']['smtp_username']
        password = self.config['smtp']['smtp_password']
        n_screenshot = 0
        if ('n_allegati' in self.config['smtp'].keys()):
            if (isinstance(self.config['smtp']['n_allegati'], int)):
                n_screenshot = self.config['smtp']['n_allegati']
            else:
                log.warning("n_allegati non è un intero, [default: 0]")

        if (port == 587):
            starttls = True
        else:
            starttls = False

        receiver_email = []
        if (self.param != ''):
            receiver_email.append(self.param)
        receiver_email.extend(self.config['smtp']['destinatari'])

        # 2. Creazione del contenuto dell'email
        msg = EmailMessage()
        msg["Subject"] = "Diario Axios - " + oggi
        msg["From"] = f"Axios - Get <{username}>"
        msg["To"] = ", ".join(receiver_email)
        msg.set_content(html, subtype='html')

        # 3. Creazione di un contesto SSL sicuro di default
        context = ssl.create_default_context()
        context.set_ciphers('HIGH:!DH:!aNULL@SECLEVEL=1')

        m_html = re.findall(r"<!-- BEGIN SCREENSHOT -->(.*?)<!-- END SCREENSHOT -->", html, re.DOTALL)

        for i, diario in enumerate(m_html):
            if (i < n_screenshot):
                dati_bytesio, filename = ScreenShot(self.DIR).diario2image(diario)
                msg.add_attachment(
                    dati_bytesio.getvalue(),
                    maintype='image',
                    subtype='png',
                    filename=filename + ".png"
                )
            elif (i == len(m_html) - 1 and n_screenshot != 0):
                dati_bytesio, filename = ScreenShot(self.DIR).diario2image(diario)
                msg.add_attachment(
                    dati_bytesio.getvalue(),
                    maintype='image',
                    subtype='png',
                    filename=filename + ".png"
                )

        # 4. Connessione al server e invio del messaggio
        try:
            if (not starttls):
                with smtplib.SMTP_SSL(smtp_server, port, context=context, timeout=30) as server:
                    server.login(username, password)
                    server.send_message(msg)
            else:
                # Stabilisce una connessione in chiaro sulla porta 587
                with smtplib.SMTP(smtp_server, port, timeout=30) as server:
                    server.ehlo()  # Identifica il client presso il server SMTP
                    server.starttls(context=context)  # Aggiorna la connessione a TLS in modo sicuro
                    server.ehlo()  # Re - identifica il client all'interno della connessione crittografata

                    server.login(username, password)
                    server.send_message(msg)

            log.info("Notifica Email inviata con successo!")
        except Exception as e:
            raise RuntimeError(f"NotificaMail: {e}") from e


class NotificaTelegram(Notifica):
    """
    Classe di definizione delle Notifiche Telegram

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità
    inviando il messaggio in una chat di Telegram.
    """
    def send_notifica(self, html: str, alunno: str) -> None:

        # 1. Configurazione dei parametri del server e delle credenziali
        BOT_TOKEN = self.config['telegram']['BOT_TOKEN']
        CHAT_ID = self.param
        n_screenshot = 0
        if ('n_allegati' in self.config['telegram'].keys()):
            if (isinstance(self.config['telegram']['n_allegati'], int)):
                n_screenshot = self.config['telegram']['n_allegati']
            else:
                log.warning("n_allegati non è un intero, [default: 0]")
        m_html = re.findall(r"<!-- BEGIN SCREENSHOT -->(.*?)<!-- END SCREENSHOT -->", html, re.DOTALL)

        # 2. Trasfomazione HTML in messaggio Telegram
        html = re.sub("<head>(.*?)</head>", "", html)
        html = re.sub("<.{0, 1}html>", "", html)
        html = re.sub("<.{0, 1}body>", "", html)
        html = re.sub("<!--.*?-->", "", html)
        html = re.sub("<h1.*?>(.*?)</h1>\n+", r"<u><b>\g<1></b></u>\n\n", html, flags=re.DOTALL)
        html = re.sub("<h2.*?>(.*?)</h2>\n*", r"<u><b>\g<1></b></u>\n\n", html, flags=re.DOTALL)
        html = re.sub("<h3.*?>(.*?)</h3>\n*", r"<u><b>\g<1></b></u>\n\n", html, flags=re.DOTALL)
        html = re.sub("<h4.*?>(.*?)</h4>\n*", r"<u><b>\g<1></b></u>\n\n", html, flags=re.DOTALL)
        html = re.sub("<hr>", "\n---\n", html)
        # html = re.sub("<a.*?href='(.*?)'.*?>(.*?)</a>", r" \g<2> \g<1>", html)
        html = re.sub(r'<li.*?>(.*?)</li>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
        html = re.sub(r'<div.*?>(.*?)</div>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
        html = re.sub(r'<p.*?>(.*?)</p>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
        html = re.sub("<li.*?class='compiti'.*?style='color:green'>(.*?)</li>\n*", r"📗 <i>\g<1></i>\n", html)
        html = re.sub("<li.*?class='verifica'.*?style='color:green'>(.*?)</li>\n*", r"💥 <i>\g<1></i>\n", html)
        html = re.sub("<li.*?class='annotazione'.*?style='color:green'>(.*?)</li>\n*", r"📚 <i>\g<1></i>\n", html)
        html = re.sub("<li.*?class='compiti'.*?style='color:orange'>(.*?)</li>\n*", r"📗 <b><i>\g<1></i></b>\n", html)
        html = re.sub("<li.*?class='verifica'.*?style='color:orange'>(.*?)</li>\n*", r"💥 <b><i>\g<1></i></b>\n", html)
        html = re.sub("<li.*?class='annotazione'.*?style='color:orange'>(.*?)</li>\n*", r"📚 <b><i>\g<1></i></b>\n", html)
        html = re.sub("<li.*?class='compiti'.*?>(.*?)</li>\n*", r"📗 \g<1>\n", html)
        html = re.sub("<li.*?class='verifica'.*?>(.*?)</li>\n*", r"💥 \g<1>\n", html)
        html = re.sub("<li.*?class='annotazione'.*?>(.*?)</li>\n*", r"📚 \g<1>\n", html)
        html = re.sub("<li.*?class='file'.*?>(.*?)</li>\n*", r"🔗 \g<1>\n", html)
        html = re.sub("<div>(.*?)</div>\n*", r"\n\g<1>\n\n", html)
        html = re.sub("<.{0, 1}ul.*?>", "\n", html)
        html = re.sub("<p.*?>(.*?)</p>", r"\n\g<1>", html)
        html = re.sub("<br>", "", html)
        html = re.sub("\n{3, }", "\n\n", html, flags=re.DOTALL)

        link = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        link_screenshot = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'

        parametri = {
            "chat_id": str(CHAT_ID),
            "parse_mode": "HTML",
            "text": html,
            "disable_notification": True
        }

        try:
            risposta = requests.get(link, params=parametri, timeout=(10, 30)).json()
            if (risposta.get("ok")):
                # Il messaggio è stato inviato con successo
                id_nuovo_messaggio = risposta["result"]["message_id"]
                log.info(f"Notifica messaggio Telegram inviata con successo! ID: {id_nuovo_messaggio}")

                for i, diario in enumerate(m_html):
                    try:
                        if (i < n_screenshot):
                            dati_bytesio, filename = ScreenShot(self.DIR).diario2image(diario)
                            YY, MM, DD = filename.split("-")
                            payload = {
                                'chat_id': str(CHAT_ID),
                                'caption': f'Pagina diario {DD}/{MM}/{YY}'
                            }
                            files = {
                                'photo': (filename, dati_bytesio.getvalue(), 'image/png')
                            }
                            risposta_allegato = requests.post(link_screenshot, data=payload, files=files, timeout=(10, 30)).json()
                            if (risposta_allegato.get("ok")):
                                id_nuovo_allegato = risposta_allegato["result"]["message_id"]
                                log.info(f"Notifica allegato Telegram inviato con successo! ID: {id_nuovo_allegato}")
                            else:
                                codice_errore_allegato = risposta_allegato.get("error_code")
                                descrizione_allegato = risposta_allegato.get("description")
                                raise RuntimeError(f"NotificaTelegram immagini - ({codice_errore_allegato}): {descrizione_allegato}")
                        elif (i == len(m_html) - 1 and n_screenshot != 0):
                            dati_bytesio, filename = ScreenShot(self.DIR).diario2image(diario)
                            payload = {
                                'chat_id': str(CHAT_ID),
                                'caption': f'Pagina diario {filename}'
                            }
                            files = {
                                'photo': (filename, dati_bytesio.getvalue(), 'image/png')
                            }
                            risposta_allegato = requests.post(link_screenshot, data=payload, files=files, timeout=(10, 30)).json()
                            if (risposta_allegato.get("ok")):
                                id_nuovo_allegato = risposta_allegato["result"]["message_id"]
                                log.info(f"Notifica allegato Telegram inviato con successo! ID: {id_nuovo_allegato}")
                            else:
                                codice_errore_allegato = risposta_allegato.get("error_code")
                                descrizione_allegato = risposta_allegato.get("description")
                                raise RuntimeError(f"NotificaTelegram immagini - ({codice_errore_allegato}): {descrizione_allegato}")
                    except Exception as e:
                        raise RuntimeError(f"NotificaTelegram immagini - {e}") from e
            else:
                # Telegram ha rifiutato la richiesta
                codice_errore = risposta.get("error_code")
                descrizione = risposta.get("description")
                raise RuntimeError(f"NotificaTelegram - ({codice_errore}): {descrizione}")
        except Exception as e:
            raise RuntimeError(f"NotificaTelegram - {e}") from e


class NotificaScreenShot(Notifica):
    """
    Classe di definizione delle Notifiche ScreenShot

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità
    creando degli screenshot.
    """
    def send_notifica(self, html: str, alunno: str) -> None:

        path_screenshot = self.param
        if (not os.path.exists(os.path.join(path_screenshot, f"screenshot_{alunno}"))):
            os.makedirs(os.path.join(path_screenshot, f"screenshot_{alunno}"))
        path_screenshot = os.path.join(path_screenshot, f"screenshot_{alunno}")

        m_html = re.findall(r"<!-- BEGIN SCREENSHOT -->(.*?)<!-- END SCREENSHOT -->", html, re.DOTALL)

        for _, html in enumerate(m_html):
            try:
                dati_bytesio, filename = ScreenShot(self.DIR).diario2image(html)
                absolute_path = os.path.join(path_screenshot, filename + ".png")
                with open(absolute_path, "wb") as f:
                    f.write(dati_bytesio.getvalue())
                log.info(f"Notifica Screenshot salvata con successo: {absolute_path}")
            except Exception as e:
                raise RuntimeError(f"NotificaScreenShot - {e}") from e
