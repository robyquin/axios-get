#!python
"""
Gestore di Notifiche.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import sys
import os
import re
import textwrap
from datetime import datetime

import smtplib
import ssl
from email.message import EmailMessage

import requests
from PIL import Image, ImageDraw, ImageFont

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
        path_file = self.config['file_html']['path']
        absolute_path = os.path.join(path_file,"compiti_"+alunno+".html")

        # 2. Salvataggio del contenuto
        try:
            # 'with' assicura che il file venga chiuso automaticamente alla fine,
            # anche se si verifica un errore durante la scrittura.
            with open(absolute_path, "w", encoding="utf-8") as file:
                file.write(html)
            print("Scrittura completata con successo!\n---")

        except PermissionError:
            print(f"Errore: Non hai i permessi necessari per scrivere nel file '{absolute_path}'.", file=sys.stderr)

        except FileNotFoundError:
            print(f"Errore: La cartella specificata per il file '{absolute_path}' non esiste.", file=sys.stderr)

        except Exception as e:
            print(f"Si è verificato un errore imprevisto: {e}", file=sys.stderr)

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

        if (port == 587):
            starttls = True
        else:
            starttls = False

        receiver_email = self.config['smtp']['destinatari']

        # 2. Creazione del contenuto dell'email
        msg = EmailMessage()
        msg["Subject"] = "Diario Axios - "+oggi
        msg["From"] = f"Axios-Get <{username}>"
        msg["To"] = ", ".join(receiver_email)
        msg.set_content(html, subtype='html')

        # 3. Creazione di un contesto SSL sicuro di default
        context = ssl.create_default_context()
        context.set_ciphers('HIGH:!DH:!aNULL@SECLEVEL=1')

        # 4. Connessione al server e invio del messaggio
        try:
            if (not starttls):
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(username, password)
                    server.send_message(msg)
            else:
                # Stabilisce una connessione in chiaro sulla porta 587
                with smtplib.SMTP(smtp_server, port, timeout=10) as server:
                    server.ehlo()  # Identifica il client presso il server SMTP
                    server.starttls(context=context) # Aggiorna la connessione a TLS in modo sicuro
                    server.ehlo()  # Re-identifica il client all'interno della connessione crittografata

                    server.login(username, password)
                    server.send_message(msg)

            print("Email inviata con successo!\n---")
        except Exception as e:
            print(f"Si è verificato un errore durante l'invio: {e}", file=sys.stderr)

class NotificaTelegram(Notifica):
    """
    Classe di definizione delle Notifiche Telegram

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità 
    inviando il messaggio in una chat di Telegram.
    """
    def send_notifica(self, html: str, alunno: str) -> None:

        # 1. Configurazione dei parametri del server e delle credenziali
        BOT_TOKEN = self.config['telegram']['BOT_TOKEN']
        CHAT_ID = self.config['telegram']['CHAT_ID']

        # 2. Trasfomazione HTML in messaggio Telegram
        html = re.sub("<head>(.*?)</head>","",html)
        html = re.sub("<.{0,1}html>","",html)
        html = re.sub("<.{0,1}body>","",html)
        html = re.sub("<h1.*?>(.*?)</h1>\n+",r"<u><b>\g<1></b></u>\n\n",html, flags=re.DOTALL)
        html = re.sub("<h2.*?>(.*?)</h2>\n*",r"<u><b>\g<1></b></u>\n\n",html, flags=re.DOTALL)
        html = re.sub("<h3.*?>(.*?)</h3>\n*",r"<u><b>\g<1></b></u>\n\n",html, flags=re.DOTALL)
        html = re.sub("<h4.*?>(.*?)</h4>\n*",r"<u><b>\g<1></b></u>\n\n",html, flags=re.DOTALL)
        html = re.sub("<hr>","\n---\n",html)
        # html = re.sub("<a.*?href='(.*?)'.*?>(.*?)</a>",r" \g<2> \g<1>",html)
        html = re.sub(r'<li.*?>(.*?)</li>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
        html = re.sub(r'<div.*?>(.*?)</div>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
        html = re.sub(r'<p.*?>(.*?)</p>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
        html = re.sub("<li.*?class='compiti'.*?>(.*?)</li>\n*",r"📗 \g<1>\n",html)
        html = re.sub("<li.*?class='verifica'.*?>(.*?)</li>\n*",r"💥 \g<1>\n",html)
        html = re.sub("<li.*?class='file'.*?>(.*?)</li>\n*",r"🔗 \g<1>\n",html)
        html = re.sub("<div>(.*?)</div>\n*",r"\n\g<1>\n\n",html)
        html = re.sub("<.{0,1}ul>", "\n", html)
        html = re.sub("<p.*?>(.*?)</p>",r"\n\g<1>",html)
        html = re.sub("<br>", "", html)
        html = re.sub("\n{3,}", "\n\n", html, flags=re.DOTALL)

        link = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        parametri={
            "chat_id": str(CHAT_ID),
            "parse_mode": "HTML",
            "text": html,
            "disable_notification": True
        }

        print(requests.get(link, params=parametri).json())
        print("---")

class NotificaScreenShot(Notifica):
    """
    Classe di definizione delle Notifiche ScreenShot

    Questa classe eredita da :class:`Notifica` e ne estende le funzionalità 
    creando degli screenshot.
    """
    def send_notifica(self, html: str, alunno: str) -> None:

        path_screenshot = self.config['screenshot']['path']
        if (not os.path.exists(os.path.join(path_screenshot,f"screenshot_{alunno}"))):
            os.makedirs(os.path.join(path_screenshot,f"screenshot_{alunno}"))
        path_screenshot = os.path.join(path_screenshot,f"screenshot_{alunno}")

        LARGHEZZA_FISSA = 1300
        ALTEZZA_MASSIMA_STIMATA = 10000
        width, height = LARGHEZZA_FISSA, ALTEZZA_MASSIMA_STIMATA

        m_html = re.findall(r"<h2.*?</ul>\n\n", html, re.DOTALL)

        for i, html in enumerate(m_html):
            image = Image.new("RGBA", (width, height),  (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            html = re.sub("<head>(.*?)</head>","",html)
            html = re.sub("<.{0,1}html>","",html)
            html = re.sub("<.{0,1}body>","",html)
            html = re.sub("<h1.*?>(.*?)</h1>\n+",r"<h1>\g<1></h1>\n\n",html, flags=re.DOTALL)
            html = re.sub("<h2.*?>(.*?)</h2>\n*",r"<h2>\g<1></h2>\n\n",html, flags=re.DOTALL)
            html = re.sub("<h3.*?>(.*?)</h3>\n*",r"<h3>\g<1></h3>\n\n",html, flags=re.DOTALL)
            html = re.sub("<h4.*?>(.*?)</h4>\n*",r"<h4>\g<1></h4>\n\n",html, flags=re.DOTALL)
            html = re.sub("<hr>","\n---\n",html)
            # html = re.sub("<a.*?href='(.*?)'.*?>(.*?)</a>",r" \g<2> \g<1>",html)
            html = re.sub(r'<li.*?>(.*?)</li>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
            html = re.sub(r'<div.*?>(.*?)</div>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
            html = re.sub(r'<p.*?>(.*?)</p>', lambda m: m.group(0).replace('\n', ' '), html, flags=re.DOTALL)
            html = re.sub("<li.*?class='compiti'.*?>(.*?)</li>\n*",r"📖 \g<1>\n",html)
            html = re.sub("<li.*?class='verifica'.*?>(.*?)</li>\n*",r"💥 \g<1>\n",html)
            html = re.sub("<li.*?class='file'.*?>(.*?)</li>\n*",r"🔗 \g<1>\n",html)
            html = re.sub("<div>(.*?)</div>\n*",r"\n\g<1>\n\n",html)
            html = re.sub("<.{0,1}ul>", "\n", html)
            html = re.sub("<p.*?>(.*?)</p>",r"\n\g<1>",html)
            html = re.sub("<b.*?>(.*?)</b>",r"\g<1>",html)
            html = re.sub("<i.*?>(.*?)</i>",r"\g<1>",html)
            html = re.sub("<br>", "", html)
            html = re.sub("\n{2,}", "\n", html, flags=re.DOTALL)

            try:
                font_h2 = ImageFont.truetype("OpenSansEmoji.ttf", size=64)
                font_h3 = ImageFont.truetype("OpenSansEmoji.ttf", size=48)
                font_text = ImageFont.truetype("OpenSansEmoji.ttf", size=32)
                font_credit = ImageFont.truetype("OpenSansEmoji.ttf", size=16)
            except IOError:
                font = ImageFont.load_default()

            lines = html.split('\n')
            lines.append("<credit>⚡ Generato automaticamente con Axios-Get</credit>")
            lines.append("<credit>🔗 https://github.com/robyquin/axios-get - Open Source (MIT)</credit>")
            y_app = 50
            filename = f"{i}_testo_formattato_{alunno}"
            for l0 in lines:
                width_wrap = 82
                align_text = "left"
                space_lines = 10
                if(re.search(r"<h2.*?>(.*?)</h2>", l0) is not None):
                    m = re.search(r"<h2.*?>(.*?)</h2>", l0)
                    font = font_h2
                    l0 = m.group(1)
                    if (len(l0.split(", ")) > 1):
                        l0 = l0.split(", ")[1]
                    try:
                        dt = datetime.strptime(l0, "%d/%m/%Y")
                        filename = datetime.strftime(dt, "%Y-%m-%d")
                    except Exception as e:
                        print(f"{e}")
                        width_wrap = 40
                        filename = "Materiale_didattico"
                    sw = 0.75
                elif(re.search(r"<h3.*?>(.*?)</h3>", l0) is not None):
                    m = re.search(r"<h3.*?>(.*?)</h3>", l0)
                    font = font_h3
                    l0 = "  "+m.group(1)
                    sw = 0.5
                elif(re.search(r"<h4.*?>(.*?)</h4>", l0) is not None):
                    m = re.search(r"<h4.*?>(.*?)</h4>", l0)
                    font = font_h3
                    l0 = "  "+m.group(1)
                    sw = 0.5
                elif(re.search(r"<credit.*?>(.*?)</credit>", l0) is not None):
                    m = re.search(r"<credit.*?>(.*?)</credit>", l0)
                    font = font_credit
                    l0 = "  "+m.group(1)
                    sw = 0.25
                    align_text = "center"
                    space_lines = 2
                else:
                    l0 = "        "+l0
                    sw = 0
                    font = font_text

                bbox = draw.textbbox((0, 0), textwrap.fill(l0, width=width_wrap, subsequent_indent='        '), font=font, align=align_text, stroke_width=sw, spacing=space_lines)
                # text_width = (bbox[2] - bbox[0])
                text_height = (bbox[3] - bbox[1])
                if (align_text=="center"):
                    x = LARGHEZZA_FISSA // 2 - (bbox[2] - bbox[0]) // 2
                else:
                    x = 50
                y = y_app
                y_app = y + text_height + space_lines*3
                draw.text(
                    (x, y),
                    textwrap.fill(l0, width=width_wrap, subsequent_indent='        '),
                    font=font,
                    fill=(0, 0, 0),
                    align=align_text,
                    spacing=space_lines,
                    stroke_width=sw,
                )

            bbox = image.getbbox()
            draw.rounded_rectangle([(0, 0), (LARGHEZZA_FISSA-3, bbox[3]+30+25-3)], radius=50, fill=None, outline='black', width=3, corners=None)

            if bbox:
                altezza_finale = bbox[3]
                immagine_finale = Image.new("RGBA", (LARGHEZZA_FISSA, altezza_finale+30+25), color='beige')
                immagine_crop = image.crop((0, 0, LARGHEZZA_FISSA, altezza_finale+30+25))
                immagine_finale.paste(immagine_crop, (0, 0), immagine_crop)

                immagine_finale.save(os.path.join(path_screenshot,filename+".png"))
                immagine_finale.close()
