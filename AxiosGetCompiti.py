#!python
"""
AxiosGetCompiti.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

__version__ = "1.1.1"

import sys
import os
from pathlib import Path
import re

import yaml

from moduli.lib_axios_famiglia import LibAxiosFamiglia
from moduli.logging_config import log

def file_config_default() -> str:
    """
    Crea il contenuto yaml di default

    :return: contenuto yaml di default
    :rtype: str
    """
    config_default = {
        'version': __version__,
        'credenziali': [
                {
                'customerid': 'customerid',
                'username': 'username',
                'password': 'password',
                'alunni': {
                    'NOME_ALUNNO_A' : {
                        'tipo': 'smtp',
                        'param': 'EMAIL_STUDENTE'
                    },
                    'NOME_ALUNNO_B' : {
                        'tipo': 'html',
                        'param': '.'
                    },
                    'NOME_ALUNNO_C' : {
                        'tipo': 'screenshot',
                        'param': '.'
                    },
                    'NOME_ALUNNO_D' : {
                        'tipo': 'telegram',
                        'param': 'CHAT_ID'
                    }
                }
            }
        ],
        'params_notifiche':{
            'html': {
                'path': '.'
            },
            'smtp': {
                'smtp_server': 'smtp.example.it',
                'smtp_port': 465,
                'smtp_username': 'Username',
                'smtp_password': 'PaSsWoRd',
                'destinatari': [
                    'EMAIL_GENITORE-TUTORE',
                    'EMAIL_ALTRI'
                    ],
                'n_allegati': 0
            },
            'telegram': {
                'BOT_TOKEN': 'TOKEN',
                'CHAT_ID': 'ID',
                'n_allegati': 0
            },
            'screenshot': {
                'path': '.'
            }
        }
    }
    
    content_yaml = yaml.dump(config_default, sort_keys=False)
    content_yaml = f"""# GUIDA ALLA CONFIGURAZIONE
# https://github.com/robyquin/axios-get/blob/master/docs/Configurazione.md
# Questo file è scritto in YAML, se lo modifichi manualmente presta attenzione all'indentazione e alla sintassi specifica.
# Il testo che segue il carattere # è un commento e quindi nell'esecuzione verrà ignorato\n\n{content_yaml}"""

    content_yaml = re.sub(r'(version:.*)', '\\1 # Versione della release', content_yaml)
    content_yaml = re.sub(r'(credenziali:.*)', '\\1 # Gruppo credenziali: raccoglie informazioni per l\'accesso al portale, la definizione degli studenti e per ciascuno la propria configurazione di notifica', content_yaml)
    content_yaml = re.sub(r'(- customerid:.*)', '\\1 # CF Istituto/Cliente', content_yaml)
    content_yaml = re.sub(r'(\s+username:.*)', '\\1 # Codice Utente o mail personale', content_yaml)
    content_yaml = re.sub(r'(\s+alunni:.*)', '\\1 # Gruppo alunni: definisce nome studente, tipologia di notifica e relativi parametri', content_yaml)
    content_yaml = re.sub(r'(\s+NOME_ALUNNO_A:.*)', '\\1 # Inserisci qui il nome dello studente che trovi nel menu a tendina sul portale AxiosFamiglia', content_yaml)
    content_yaml = re.sub(r'(\s+tipo:.*)', "\\1 # Tipi di notifiche disponibili: html, screenshot, smtp, telegram", content_yaml)
    content_yaml = re.sub(r'(\s+param:.*)', "\\1 # Parametro caratteristico della notifica scelta [default: eredita il parametro dalla configurazione generale]", content_yaml)

    content_yaml = re.sub(r'(params_notifiche:.*)', '\\1 # Gruppo parametri globali di notifica: raccoglie informazioni generali per rendere possibile la tipologia di notifica', content_yaml)
    content_yaml = re.sub(r'(\s+(html|screenshot):.*)', '\\1 # Gruppo di configurazione globale per la notifica \\2', content_yaml)
    content_yaml = re.sub(r'(\s+(telegram):.*)', '\\1 # Gruppo di configurazione globale per la notifica \\2 (https://github.com/robyquin/axios-get/blob/master/docs/Telegram_token_bot.md)', content_yaml)
    content_yaml = re.sub(r'(\s+(smtp):.*)', '\\1 # Gruppo di configurazione globale per la notifica \\2 (https://github.com/robyquin/axios-get/blob/master/docs/SMTP_server.md)', content_yaml)
    content_yaml = re.sub(r'(\s+path:.*)', '\\1 # Specifica qui il percorso relativo o assoluto della cartella di destinazione', content_yaml)
    content_yaml = re.sub(r'(\s+n_allegati:.*)', '\\1 # Specifica il numero di screenshot da allegare alla notifica [>=0]', content_yaml)

    content_yaml = re.sub(r'(NOME_ALUNNO_[B-D]:.*)', '# \\1 # Inserisci qui il nome dello studente successivo che trovi nel menu', content_yaml)
    content_yaml = re.sub(r'(tipo: (html|screenshot|telegram))', '# \\1', content_yaml)
    content_yaml = re.sub(r'(param: (\.|CHAT_ID))', '# \\1', content_yaml)
    content_yaml = re.sub(r'(- EMAIL_ALTRI.*)', '# \\1 # Specifica, come un elenco, altri destinatari della email', content_yaml)

    return content_yaml

def run_axios_get_compiti(DIR):

    if (os.path.exists(os.path.join(DIR, "credenziali.yml"))):
        with open(os.path.join(DIR, "credenziali.yml"), "r", encoding="utf-8") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        if (config.get("version", None) == None):
            # La configurazione esiste ma ad una versione <= v1.0.8, è da aggiornare direttamente all'ultima
            log.info(f"Migrazione automatica alla versione {__version__}")
            log.warning(f"Il file di configurazione sarà convertito alla nuova versione {__version__}!")
            new_config = {}
            new_config['version'] = __version__
            new_config['credenziali'] = [config['axios']['credenziali']]
            new_config['credenziali'][0]['alunni'] = {}
            for alunno in config['axios']['alunni']:
                new_config['credenziali'][0]['alunni'][alunno] = { }
                tipo_notifica = config.get("tipo_notifica", 'html')
                if (tipo_notifica == 'file_html' or tipo_notifica == 'html'):
                    new_config['credenziali'][0]['alunni'][alunno]['tipo'] = 'html'
                    new_config['credenziali'][0]['alunni'][alunno]['param'] = config.get("file_html", {}).get("path", ".")
                elif (tipo_notifica == 'screenshot'):
                    new_config['credenziali'][0]['alunni'][alunno]['tipo'] = tipo_notifica
                    new_config['credenziali'][0]['alunni'][alunno]['param'] = config.get(tipo_notifica, {}).get("path", ".")
                elif (tipo_notifica == 'smtp'):
                    new_config['credenziali'][0]['alunni'][alunno]['tipo'] = tipo_notifica
                    new_config['credenziali'][0]['alunni'][alunno]['param'] = "EMAIL_STUDENTE"
                elif (tipo_notifica == 'telegram'):
                    new_config['credenziali'][0]['alunni'][alunno]['tipo'] = tipo_notifica
                    new_config['credenziali'][0]['alunni'][alunno]['param'] = config.get(tipo_notifica, {}).get("CHAT_ID", None)
            new_config['params_notifiche'] = {}
            for tipo_notifica in ['file_html', 'smtp', 'telegram', 'screenshot']:
                if (config.get(tipo_notifica, None) != None):
                    if (tipo_notifica == 'file_html'):
                        new_config['params_notifiche']['html'] = config.get(tipo_notifica)
                    elif (tipo_notifica == 'telegram'):
                        new_config['params_notifiche'][tipo_notifica] = config.get(tipo_notifica)
                    else:
                        new_config['params_notifiche'][tipo_notifica] = config.get(tipo_notifica)
            with open(os.path.join(DIR, f"credenziali_v{__version__}.yml"), "w", encoding="utf-8") as file_config:
                file_config.write(yaml.dump(new_config, sort_keys=False))
            log.info(f"Salvataggio file: {os.path.join(DIR, f"credenziali_v{__version__}.yml")}")
            log.warning(f"Verifica che i dati siano corretti, poi rinomina credenziali_v{__version__}.yml in credenziali.yml per renderlo effettivo!")
        else:
            v_maj_conf, v_min_conf, v_patch_conf = list(map(lambda x: int(x), config.get("version").split('.')))
            v_maj_app, v_min_app, v_patch_app = list(map(lambda x: int(x), __version__.split('.')))

            if (v_maj_app >= v_maj_conf and v_min_app > v_min_conf):
                # La configurazione esiste con una versione diversa da v1.1.0, ma è da aggiornata
                log.error("File di configurazione deve essere aggiornata!")
                log.error(f"Non è disponibile nessuna procedura di migrazione da v{config.get("version")} a v{__version__}")
            elif (v_maj_app == v_maj_conf and v_min_app == v_min_conf):
                # La configurazione esiste
                if (v_patch_app > v_patch_conf):
                    # La patch della versione è diversa e va aggiornata
                    log.info(f"Aggiornamento automatico di patch da {config['version']} a {__version__}")
                    config['version'] = __version__
                    with open(os.path.join(DIR, "credenziali.yml"), "w", encoding="utf-8") as file_config:
                        file_config.write(yaml.dump(config, sort_keys=False))
                log.info("INIZIO ELABORAZIONE")
                LibAxiosFamiglia(DIR, config)
                log.info("FINE ELABORAZIONE")
    else:
        try:
            with open(os.path.join(DIR, "credenziali_default.yml"), "w", encoding="utf-8") as file_config:
                file_config.write(file_config_default())
            raise FileNotFoundError(os.path.join(DIR, "credenziali_default.yml"))
        except FileNotFoundError as e:
            log.error(f"File di configurazione non trovato! Creazione del file di default: {e}")
        except PermissionError:
            log.error(f"Non hai i permessi necessari per scrivere nel file '{os.path.join(DIR, "credenziali_default.yml")}'.")
        except Exception as e:
            log.error(f"Si è verificato un errore imprevisto nel salvataggio di credenziali_default.yml: {e}")

if __name__ == "__main__":

    run_axios_get_compiti(str(Path(os.path.dirname(__file__)).absolute()))
    sys.exit(0)
