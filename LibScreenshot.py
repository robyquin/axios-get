#!python
"""
Gestore di Screenshot.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""


import sys
import io
import os
from pathlib import Path
import textwrap
import re
from html import unescape as html_unescape
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

if getattr(sys, 'frozen', False):
    # Se l'applicazione è compilata con PyInstaller
    DIR=str(os.path.dirname(sys.executable))+os.path.sep
    sys.stderr = open("errori.txt", "w", encoding="utf-8")
    sys.stdout = open("log.txt", "w", encoding="utf-8")
else:
    DIR=str(Path(os.path.dirname(__file__)).absolute())+os.path.sep

class ScreenShot():

    def diario2image(self, html: str) -> tuple[io.BytesIO, str]:

        LARGHEZZA_FISSA = 1300
        ALTEZZA_MASSIMA_STIMATA = 10000
        width, height = LARGHEZZA_FISSA, ALTEZZA_MASSIMA_STIMATA

        buffer_memoria = io.BytesIO()

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
        html = re.sub("<a.*?href='(.*?)'.*?>(.*?)</a>",r" \g<1>",html)
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
            path_font = os.path.join(DIR, "assets", "fonts", "OpenSansEmoji.ttf")
            font_h2 = ImageFont.truetype(path_font, size=64)
            font_h3 = ImageFont.truetype(path_font, size=48)
            font_text = ImageFont.truetype(path_font, size=32)
            font_credit = ImageFont.truetype(path_font, size=16)
        except IOError:
            font_h2 = ImageFont.load_default(size=64)
            font_h3 = ImageFont.load_default(size=48)
            font_text = ImageFont.load_default(size=32)
            font_credit = ImageFont.load_default(size=16)

        lines = html.split('\n')
        lines.append("<credit>⚡ Generato automaticamente con Axios-Get</credit>")
        lines.append("<credit>🔗 https://github.com/robyquin/axios-get - Open Source (MIT)</credit>")
        y_app = 50
        filename = "testo_formattato"
        for l0 in lines:
            width_wrap = 82
            align_text = "left"
            space_lines = 10
            if(re.search(r"<h2.*?>(.*?)</h2>", l0) is not None):
                m = re.search(r"<h2.*?>(.*?)</h2>", l0)
                font = font_h2
                l0 = m.group(1)
                data_l0 = l0
                if (len(l0.split(", ")) > 1):
                    data_l0 = l0.split(", ")[1]
                try:
                    dt = datetime.strptime(data_l0, "%d/%m/%Y")
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

            bbox = draw.textbbox((0, 0), textwrap.fill(html_unescape(l0), width=width_wrap, subsequent_indent='        '), font=font, align=align_text, stroke_width=sw, spacing=space_lines)
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
                textwrap.fill(html_unescape(l0), width=width_wrap, subsequent_indent='        '),
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

            immagine_finale.save(buffer_memoria, format='PNG')
            immagine_finale.close()

        return buffer_memoria, filename
