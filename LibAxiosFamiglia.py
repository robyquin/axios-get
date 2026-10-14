#!python
"""
Gestore di acquisizione dati da Axios.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import sys
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

DOW_Tr = { 
    'Mon': 'Lun',
    'Tue': 'Mar',
    'Wed': 'Mer',
    'Thu': 'Gio',
    'Fri': 'Ven',
    'Sat': 'Sab',
    'Sun': 'Dom'
}

if getattr(sys, 'frozen', False):
    # Se l'applicazione è compilata con PyInstaller
    DIR=str(os.path.dirname(sys.executable))+os.path.sep
else:
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
        self.COMPITI = {}
        self.MATERIALE_CONDIVISO_ALUNNO = ""
        self.MATERIALE_DIDATTICO_FOLDERS_SHARED_PROF = ""
        self.MATERIALE_DIDATTICO_FOLDERS_SHARED = {}
        self.MATERIALE_DIDATTICO_CONDIVISO_CONTENT = []
        self.notifica = class_notifica
        self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES = []
        self.idx_folder = 0
        self.idx_file = 0
        self.sha1_REGISTRO = ""
        self.sha1_REGISTRO_old = ""
        self.sha1_MD = ""
        self.sha1_MD_old = ""

        if(self.customerid != '' and self.username != '' and self.password != '' ):
            self.session = requests.session()
        else:
            raise Exception("Controlla il file di configurazione: una delle credenziali di Axios è vuota")

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
            ['POST', 'https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'FAMILY_CHANGE_ALUNNO'}, '03_FAMILY_CHANGE_ALUNNO.json', 'set_in_session', 'json', False ],
            ['POST', 'https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'FAMILY_REGISTRO_CLASSE_COMPITI_LISTA'}, '04_action.json', {"draw":1,"columns":{},"order":[],"start":0,"length":50,"search":{"value":"","regex":False},"iMatId":""}, 'json', True],
            ['GET','https://registrofamiglie.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'FAMILY_REGISTRO_CLASSE_NOTE', 'Others': 2}, '05_annotazioni.json'],
            ['GET', 'https://registrofamiglie.axioscloud.it/Pages/SD/SD_Logout.aspx', {}, '06_logout.html']
        ]

        self.__get_session(Alunno, link_registrofamiglie, "registrofamiglie_")
        # Notifica qui
        if (self.sha1_REGISTRO != self.sha1_REGISTRO_old or self.sha1_MD != self.sha1_MD_old and self.COMPITI != {}):
            self.notifica.send_notifica(self.elaborazione_json(self.COMPITI, Alunno), Alunno)
            print("Registro", self.sha1_REGISTRO, self.sha1_REGISTRO_old)
            print("Materiale-Dit", self.sha1_MD, self.sha1_MD_old)
            print("---")
        else:
            print("Nessuna notifica: non ci sono modifiche!\n---")

    def get_session_collabora(self, Alunno: str) -> None:
        """
        Gestisce una sessione di Collabora per l'alunno specificato

        :param Alunno: Nome dell'alunno
        :type Alunno: str
        """
        self.session.headers['User-Agent'] = self.DefaultUserAgent
        self.session.headers['Referer'] = "https://collabora.axioscloud.it/"
        link_collabora = [
            ['GET','https://collabora.axioscloud.it/', {}, '00_home.html'],
            ['POST', 'https://collabora.axioscloud.it/Pages/SD/SD_Login.aspx', {}, '01_login.html', {'customerid': self.customerid, 'username': self.username, 'password': self.password, 'customeridSpid': '' }, '', False],
            ['GET','https://collabora.axioscloud.it/Pages/SD/SD_Dashboard.aspx', {}, '02_dashboard.html'],
            ['GET','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'DashboardLoad'}, '03_load_dashboard.html'],
            ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_CONDIVISO_ALUNNO'}, '04_MATERIALE_CONDIVISO_ALUNNO.json', 'set_in_session', '', False],
            ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_DIDATTICO_FOLDERS_SHARED'}, '05_MATERIALE_DIDATTICO_FOLDERS_SHARED.json', 'set_in_session', '', False],
            ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_CONDIVISO_CON_ME_DETAIL'}, '06_MATERIALE_CONDIVISO_CON_ME_DETAIL.json', 'set_in_session', 'json', False],
            ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_DIDATTICO_CONDIVISO_CONTENT'}, '07_MATERIALE_DIDATTICO_CONDIVISO_CONTENT.json', 'set_in_session', 'json', False],
            ['GET', 'https://collabora.axioscloud.it/Pages/SD/SD_Logout.aspx', {}, '08_logout.html']
        ]

        self.__get_session(Alunno, link_collabora, "collabora_")
        if (len(self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES) > 0):
            matdit_compiti_alunno = os.path.join(DIR, "collabora_"+Alunno, 'materiale-didattico.html')
            text_MD = "\n".join(self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES)
            self.sha1_MD = hashlib.sha1(text_MD.encode('utf-8')).hexdigest()
            if(os.path.exists(matdit_compiti_alunno)):
                with open(matdit_compiti_alunno, 'r', encoding='utf-8', newline='') as f:
                    self.sha1_MD_old = hashlib.sha1(f.read().encode('utf-8')).hexdigest()
            with open(matdit_compiti_alunno, 'w', encoding='utf-8', newline="\n") as fp:
                fp.write(text_MD)
                fp.close()

    def __get_session(self, Alunno, link_sequence, prefix):
        for link in link_sequence:
            registo_compiti_alunno = os.path.join(DIR, prefix+Alunno, link[UrlIdType.filename])
            if (link[UrlIdType.method] == 'GET'):
                res = self.session.get(link[UrlIdType.url], params=link[UrlIdType.params], allow_redirects=True)
                if ('Action' in link[UrlIdType.params].keys()):
                    if (link[UrlIdType.params]['Action'] == 'DashboardLoad'):
                        text = res.text
                        if (prefix == "registrofamiglie_"):
                            m = re.search(r"<a.*data-action='FAMILY_CHANGE_ALUNNO'.*?data-others='(.*?)'.*?<b>(.*?)</b>.*?</a>", text)
                            if (m is not None):
                                self.alunni[m.group(2)] = m.group(1)
                        elif (prefix == "collabora_"):
                            m = re.search(r"<button.*?utId = '(.*?)'>.*?<div class='details'><div class='desc'>(.*?)</div></div></button>", text)
                            if (m is not None):
                                if (Alunno in m.group(2)):
                                    self.alunni[Alunno] = m.group(1)
                        if (not Alunno in self.alunni.keys()):
                            print(f"Warning! Il nome dell'alunno, {Alunno}, non trovato! Verifica e controlla la corrispondenza nel file di configurazione.", file=sys.stderr)
            else:
                if ('Action' in link[UrlIdType.params].keys()):
                    if (link[UrlIdType.params]['Action'] == 'MATERIALE_CONDIVISO_ALUNNO'):
                        link[UrlIdType.data] = {"fiAlunno": self.alunni[Alunno], "fuiAlunno":""}
                    elif (link[UrlIdType.params]['Action'] == 'FAMILY_CHANGE_ALUNNO'):
                        link[UrlIdType.data] = {"alunnoId": self.alunni[Alunno]}
                    elif (link[UrlIdType.params]['Action'] == 'MATERIALE_DIDATTICO_FOLDERS_SHARED'):
                        link[UrlIdType.data] = self. MATERIALE_CONDIVISO_ALUNNO
                    elif (link[UrlIdType.params]['Action'] == 'MATERIALE_CONDIVISO_CON_ME_DETAIL'):
                        link[UrlIdType.data] = self.MATERIALE_DIDATTICO_FOLDERS_SHARED[self.idx_folder]['MATERIALE_CONDIVISO_CON_ME_DETAIL'] # richiede iterazione
                    elif (link[UrlIdType.params]['Action'] == 'MATERIALE_DIDATTICO_CONDIVISO_CONTENT'):
                        link[UrlIdType.data] = self.MATERIALE_DIDATTICO_CONDIVISO_CONTENT[self.idx_file] # richiede iterazione

                if (link[UrlIdType.type_data]=='json'):
                    res = self.session.post(link[UrlIdType.url], json=link[UrlIdType.data], params=link[UrlIdType.params], allow_redirects=link[UrlIdType.redirect], headers={'Content-Type': 'application/x-www-form-urlencoded'})
                else:
                    res = self.session.post(link[UrlIdType.url], data=link[UrlIdType.data], params=link[UrlIdType.params], allow_redirects=link[UrlIdType.redirect], headers={'Content-Type': 'application/x-www-form-urlencoded'})

                get_error = re.search(r"SweetMessage.error\('(.*)'\);", res.text)
                if (get_error == None):
                    if ('Action' in link[UrlIdType.params].keys()):
                        if (link[UrlIdType.params]['Action'] == 'FAMILY_REGISTRO_CLASSE_COMPITI_LISTA'):
                            self.COMPITI = json.loads(res.text)
                            self.sha1_REGISTRO = hashlib.sha1(res.text.encode('utf-8')).hexdigest()
                            self.sha1_REGISTRO_old = ""
                            if(os.path.exists(registo_compiti_alunno)):
                                with open(registo_compiti_alunno, "rb") as f:
                                    self.sha1_REGISTRO_old = hashlib.file_digest(f, "sha1").hexdigest()
                        elif (link[UrlIdType.params]['Action'] == 'MATERIALE_CONDIVISO_ALUNNO'):
                            jj = json.loads(res.text)
                            text = jj['html']
                            m = re.search(r"'userList' value = '(.*?)'", text)
                            self. MATERIALE_CONDIVISO_ALUNNO = m.group(1)
                            m = re.search(r"<legend.*?>(.*?)</legend>", text)
                            self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES.append(f"<h2>{m.group(1)}</h2>")
                        elif (link[UrlIdType.params]['Action'] == 'MATERIALE_DIDATTICO_FOLDERS_SHARED'):
                            self.MATERIALE_DIDATTICO_FOLDERS_SHARED = json.loads(json.loads(res.text)['json'])
                            for folder, _ in enumerate(self.MATERIALE_DIDATTICO_FOLDERS_SHARED):
                                FOLDERS_SHARED = str(self.MATERIALE_DIDATTICO_FOLDERS_SHARED[folder]['id']).split("|")
                                self.MATERIALE_DIDATTICO_FOLDERS_SHARED[folder]['MATERIALE_CONDIVISO_CON_ME_DETAIL'] = {}
                                self.MATERIALE_DIDATTICO_FOLDERS_SHARED[folder]['MATERIALE_CONDIVISO_CON_ME_DETAIL']['fiDocId'] = FOLDERS_SHARED[0]
                                self.MATERIALE_DIDATTICO_FOLDERS_SHARED[folder]['MATERIALE_CONDIVISO_CON_ME_DETAIL']['fnId'] = FOLDERS_SHARED[1]
                        elif (link[UrlIdType.params]['Action'] == 'MATERIALE_CONDIVISO_CON_ME_DETAIL'):
                            jj = json.loads(res.text)
                            text = jj['html']
                            m = re.findall(r"data-nrow='(.*?)' data-others='(.*?)'", text)
                            for ll in m:
                                self.MATERIALE_DIDATTICO_CONDIVISO_CONTENT.append({"folderId": str(ll[1]),"nRow":str(ll[0]),"uteCanWrite":""})
                            m = re.findall('<a.*?>(.*?)</a>', text)
                            if (self.MATERIALE_DIDATTICO_FOLDERS_SHARED_PROF != self.MATERIALE_DIDATTICO_FOLDERS_SHARED[self.idx_folder]['text']):
                                m1 = re.findall('(.*?)<div.*?<span.*?>(.*?)</span>', self.MATERIALE_DIDATTICO_FOLDERS_SHARED[self.idx_folder]['text'])
                                self.MATERIALE_DIDATTICO_FOLDERS_SHARED_PROF = f"{m1[0][0]} ({str(m1[0][1])})"
                                self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES.append(f"<h3>{self.MATERIALE_DIDATTICO_FOLDERS_SHARED_PROF}</h3>")
                            for ll in m:
                                self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES.append(f"<h4>{ll}</h4>")
                        elif (link[UrlIdType.params]['Action'] == 'MATERIALE_DIDATTICO_CONDIVISO_CONTENT'):
                            jj = json.loads(res.text)
                            text = jj['html']
                            m = re.findall('<td.*?>(.*?)<div.*?<button.*?data-source-filename=\'(.*?)\'.*?</button>.*?<small>(.*?)</small>.*?</td>', text)
                            self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES.append("<ul>")
                            for ll in m:
                                self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES.append(f"<li><b>{ll[0]}</b><div>{ll[1]} - {ll[2]}</div></li>")
                            self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES.append("</ul>")
                            if(len(self.MATERIALE_DIDATTICO_CONDIVISO_CONTENT)-1 > self.idx_file):
                                new_link_collabora = [
                                        ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_DIDATTICO_CONDIVISO_CONTENT'}, '07_MATERIALE_DIDATTICO_CONDIVISO_CONTENT.json', 'set_in_session', 'json', False]
                                    ]
                                self.idx_file +=1
                                self.__get_session(Alunno, new_link_collabora, prefix)
                            if(len(self.MATERIALE_DIDATTICO_FOLDERS_SHARED)-1 > self.idx_folder):
                                new_link_collabora = [
                                        ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_CONDIVISO_CON_ME_DETAIL'}, '06_MATERIALE_CONDIVISO_CON_ME_DETAIL.json', 'set_in_session', 'json', False],
                                        ['POST','https://collabora.axioscloud.it/Pages/APP/APP_Ajax_Get.aspx', {'Action': 'MATERIALE_DIDATTICO_CONDIVISO_CONTENT'}, '07_MATERIALE_DIDATTICO_CONDIVISO_CONTENT.json', 'set_in_session', 'json', False]
                                    ]
                                self.idx_folder +=1
                                self.idx_file = 0
                                self.MATERIALE_DIDATTICO_CONDIVISO_CONTENT = []
                                self.__get_session(Alunno, new_link_collabora, prefix)

                else:
                    raise Exception("{}".format(get_error.group(1)))

            # DEBUG
            print(res.request.method, res.request.url)     # L'URL finale
            if (res.request.method == 'POST'):
                print(res.request.body)    # I dati inviati (es: test=123)
            print(res.request.headers) # Gli header di quella specifica chiamata
            print("---")
            if (prefix is not None and link[UrlIdType.filename] is not None):
                dir_registro_alunno = os.path.join(DIR, prefix+Alunno)
                if (not os.path.exists(dir_registro_alunno)):
                    os.makedirs(dir_registro_alunno)
                with open(registo_compiti_alunno, 'w', encoding='utf-8') as fp:
                    fp.write(res.text)
                    fp.close()

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
        oggi_long = datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")

        # FILTRO PER DATA
        for c in compiti["data"]:
            dt = datetime.strptime(c["giorno"], "%d/%m/%Y")
            if (dt > datetime.now()):
                new_compiti.append(c)

        linee_notifica = ["<html>", "<body>", f"<h1>Compiti per {Alunno}</h1>", f"<p>Ciao <i>{Alunno}</i>,<br>\nricorda sempre di verificare e integrare questi compiti con quelli scritti in classe sul tuo diario cartaceo.</p>", "<p>Buon lavoro</p>"]
        giorno_app = ""
        for c in range(len(new_compiti)-1, -1, -1):
            giorno = new_compiti[c]["giorno"]
            DayOfWeek = datetime.strptime(giorno, "%d/%m/%Y").strftime("%a")
            if(c == (len(new_compiti)-1)):
                linee_notifica.append(f"\n<hr>\n<h2>{DOW_Tr[DayOfWeek]}, {giorno}</h2>")
            else:
                if(giorno != giorno_app):
                    linee_notifica.append(f"\n<hr>\n<h2>{DOW_Tr[DayOfWeek]}, {giorno}</h2>")
            giorno_app = giorno

            testo_email = []
            if (new_compiti[c]["testo"] != ""):
                testo_email.append(new_compiti[c]["testo"])
            elif(new_compiti[c]["verifica"] != ""):
                testo_email.append("<b>Verifica</b>: "+new_compiti[c]["verifica"])
            linee_notifica.append(f"<h3>{new_compiti[c]["materia"]}</h3><ul><li>{"</li><li>".join(testo_email)}</li></ul>")

        if (len(self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES) > 0):
            linee_notifica.append("<hr>")
            linee_notifica.extend(self.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES)

        linee_notifica.append(f"\n<hr>\n<p>Questo è un aggiornamento del {oggi_long}</p>")
        if (self.sha1_REGISTRO != self.sha1_REGISTRO_old):
            linee_notifica.append(f"<p>Modifiche/aggiornamenti apportati sui <i>Compiti</i></p>")
        if (self.sha1_MD != self.sha1_MD_old):
            linee_notifica.append(f"<p>Modifiche/aggiornamenti apportati sul <i>Materiale Didattico</i></p>")
        linee_notifica.append("</body>")
        linee_notifica.append("</html>")

        return "\n".join(linee_notifica)
