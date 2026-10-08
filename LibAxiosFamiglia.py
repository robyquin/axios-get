#!python
"""
Gestore di acquisizione dati da Axios.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

from datetime import datetime
import os
import re
from pathlib import Path
import json
from enum import IntEnum
import hashlib

import requests

import notifica

class UrlIdType(IntEnum):
    """
    Definizione di corrispondeza nomi e posizione dell'array Link.
    """
    method = 0
    url = 1
    params = 2
    filename = 3
    data = 4
    type_data = 5
    redirect = 6

DIR=str(Path(os.path.dirname(__file__)).absolute())+os.path.sep

class LibAxiosFamiglia():
    """
    Classe che permette l'acquisizione di dati da Axios. 
    """

    def __init__(self, credenziali: dict, class_notifica: notifica.Notifica):
        self.DefaultUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:156.0) Gecko/20100101 Firefox/156.0"

        self.customerid = str(credenziali['customerid'])
        self.username = str(credenziali['username'])
        self.password = str(credenziali['password'])
        self.alunni = {}
        self.notifica = class_notifica

        self.session = requests.session()

    def __delete__(self, instance):
        self.session.close()

    def get_session_registrofamiglie(self, Alunno: str) -> None:
        """
        Gestisce una sessione di Registro Famiglie per l'alunno specificato

        :param Alunno: Nome dell'alunno
        :type Alunno: str
        """
        self.session.headers['User-Agent'] = self.DefaultUserAgent
        self.session.headers['Referer'] = "https://registrofamiglie.axioscloud.it/"

        link_registrofamiglie = [
            ['GET','https://registrofamiglie.axioscloud.it/', {}, '00_home.html'],
            ['POST','https://registrofamiglie.axioscloud.it/Pages/SD/SD_Login.aspx', {}, '01_login.html', {'customerid': self.customerid, 'username': self.username, 'password': self.password, 'customeridSpid': '' }, '', False],
            ['GET','https://registrofamiglie.axioscloud.it/Pages/SD/SD_Dashboard.aspx', {}, '02_dashboard.html'],
            ['GET','https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'DashboardLoad'}, '03_load_dashboard.html'],
            ['POST', 'https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'FAMILY_REGISTRO_CLASSE_COMPITI_LISTA'}, '04_action.json', {"draw":1,"columns":{},"order":[],"start":0,"length":50,"search":{"value":"","regex":False},"iMatId":""}, 'json', True],
            ['GET','https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'FAMILY_REGISTRO_CLASSE_NOTE', 'Others': 2}, '05_annotazioni.json'],
            ['GET', 'https://registrofamiglie.axioscloud.it/Pages/SD/SD_Logout.aspx', {}, '06_logout.html']
        ]

        self.__get_session(Alunno, link_registrofamiglie, "registrofamiglie_")

    def __get_session(self, Alunno, link_sequence, prefix):
        for link in link_sequence:
            if (link[UrlIdType.method] == 'GET'):
                res = self.session.get(link[UrlIdType.url], params=link[UrlIdType.params], allow_redirects=True)
                if ('Action' in link[UrlIdType.params].keys()):
                    if (link[UrlIdType.params]['Action'] == 'DashboardLoad'):
                        self.__get_alunni(res.text, Alunno)
            else:
                if (link[UrlIdType.type_data]=='json'):
                    res = self.session.post(link[UrlIdType.url], json=link[UrlIdType.data], params=link[UrlIdType.params], allow_redirects=link[UrlIdType.redirect], headers={'Content-Type': 'application/x-www-form-urlencoded'})
                else:
                    res = self.session.post(link[UrlIdType.url], data=link[UrlIdType.data], params=link[UrlIdType.params], allow_redirects=link[UrlIdType.redirect], headers={'Content-Type': 'application/x-www-form-urlencoded'})
                if ('Action' in link[UrlIdType.params].keys()):
                    if (link[UrlIdType.params]['Action'] == 'FAMILY_REGISTRO_CLASSE_COMPITI_LISTA'):
                        sha1_hash = hashlib.sha1(res.text.encode('utf-8')).hexdigest()
                        sha1_hash_old = ""
                        if(os.path.exists(DIR+prefix+link[UrlIdType.filename])):
                            with open(DIR+prefix+link[UrlIdType.filename], "rb") as f:
                                sha1_hash_old = hashlib.file_digest(f, "sha1").hexdigest()
                        if (sha1_hash != sha1_hash_old):
                            self.notifica.send_notifica(self.elaborazione_json(json.loads(res.text), Alunno))
                            print(sha1_hash, sha1_hash_old)
                            print("---")
                        else:
                            print("Nessuna notifica: non ci sono modifiche!\n---")

            # DEBUG
            print(res.request.method, res.request.url)     # L'URL finale
            if (res.request.method == 'POST'):
                print(res.request.body)    # I dati inviati (es: test=123)
            print(res.request.headers) # Gli header di quella specifica chiamata
            print("---")
            if (prefix is not None and link[UrlIdType.filename] is not None):
                with open(DIR+prefix+link[UrlIdType.filename], 'w', encoding='utf-8') as fp:
                    fp.write(res.text)
                    fp.close()

    def __get_alunni(self, text, Alunno):
        m = re.search(r"<a.*data-action='FAMILY_CHANGE_ALUNNO'.*?data-others='(.*?)'.*?<b>(.*?)</b>.*?</a>", text)
        if (len(m.groups()) > 0):
            self.alunni[m.group(2)] = m.group(1)
        if (Alunno in self.alunni.keys()):
            link=['POST', 'https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'FAMILY_CHANGE_ALUNNO'}, '03_FAMILY_CHANGE_ALUNNO.json', {"alunnoId": self.alunni[Alunno]}, 'json', False ]
            self.__get_session(Alunno, [link], None)

    def elaborazione_json(self, compiti: dict, Alunno: str) -> str:
        """
        Costruisce il testo della notifica dal dizionario compiti

        :param compiti: Dizionario di compiti
        :type compiti: dict
        :param Alunno: Nome dell'alunno
        :type Alunno: str
        :return: corpo della notifica
        :rtype: str
        """
        new_compiti = []

        # FILTRO PER DATA
        for c in compiti["data"]:
            dt = datetime.strptime(c["giorno"], "%d/%m/%Y")
            if (dt > datetime.now()):
                new_compiti.append(c)

        linee_notifica = ["<html>", "<body>", "<h1>Compiti per {}</h1>".format(Alunno)]
        giorno_app = ""
        for c in range(len(new_compiti)-1, -1, -1):
            giorno = new_compiti[c]["giorno"]
            if(c == (len(new_compiti)-1)):
                linee_notifica.append("<h2>{}</h2>".format(giorno))
            else:
                if(giorno != giorno_app):
                    linee_notifica.append("<h2>{}</h2>".format(giorno))
            giorno_app = giorno

            testo_email = []
            if (new_compiti[c]["testo"] != ""):
                testo_email.append(new_compiti[c]["testo"])
            elif(new_compiti[c]["verifica"] != ""):
                testo_email.append("<b>Verifica</b>: "+new_compiti[c]["verifica"])
            linee_notifica.append("<h3>{}</h3><ul><li>{}</li></ul>".format(new_compiti[c]["materia"], "</li><li>".join(testo_email)))

        linee_notifica.append("</body>")
        linee_notifica.append("</html>")

        return "".join(linee_notifica)
