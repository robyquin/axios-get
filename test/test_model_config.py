"""
Test per la validazione dei dati in credenziali.yml (model_config.py)

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

Test unitari per la validazione della configurazione credenziali.
"""

import pytest
import sys
from pathlib import Path

# Aggiungi il percorso del progetto
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestModelConfig:
    """Test per validazione dati di configurazione."""

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="vuoto"),
            pytest.param({'tipo': 'html'}, False, id="tipo_obbligatorio"),
            pytest.param({'param': 'stringa'}, False, id="param_obbligatorio"),
            pytest.param({'tipo': 'qualsiasi', 'param': 'stringa'}, False, id="tipo-non-in-lista"),
            pytest.param({'tipo': 'html', 'param': 'stringa'}, True, id="tipo-html"),
            pytest.param({'tipo': 'screenshot', 'param': 'stringa'}, True, id="tipo-screenshot"),
            pytest.param({'tipo': 'telegram', 'param': 'stringa'}, True, id="tipo-telegram"),
            pytest.param({'tipo': 'smtp', 'param': 'nome@cognome'}, True, id="tipo-smtp-email"),
            pytest.param({'tipo': 'smtp', 'param': 'stringa'}, False, id="tipo-smtp-stringa"),
            pytest.param({'tipo': 'html', 'param': 'stringa', 'nome_alternativo': 'stringa'}, True, id="nome_alternativo"),
            pytest.param({'tipo': 'html', 'param': 12}, False, id="param-int"),
            pytest.param({'tipo': 'html', 'param': 1.2}, False, id="param-float"),
        ]
    )
    def test_ConfigurazioneAlunno(self, conf, status):
        from moduli.model_config import ConfigurazioneAlunno
        msg = ""
        try:
            ConfigurazioneAlunno(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="vuoto"),
            pytest.param({'customerid': 1.2}, False, id="customerid-float"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 1.2}, False, id="username-float"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 12}, False, id="password-int"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 1.2}, False, id="password-float"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': 'stringa'}, False, id="alunni-stringa"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': 12}, False, id="alunni-int"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': 1.5}, False, id="alunni-float"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': []}, False, id="alunni-list"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': {}}, False, id="alunni-dict-vuoto"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : 'stringa'}}, False, id="alunni-alunno-stringa"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : 12}}, False, id="alunni-alunno-int"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : 1.2}}, False, id="alunni-alunno-float"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : []}}, False, id="alunni-alunno-list"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : {}}}, True, id="alunni-alunno-dict"),
            # campi obbligatori
            pytest.param({'username': 'number', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : {}}}, False, id="customerid-obbligatorio"),
            pytest.param({'customerid': 'codice_fiscale', 'password': 'chiave-segreta', 'alunni': {'alunno_A' : {}}}, False, id="username-obbligatorio"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'alunni': {'alunno_A' : {}}}, False, id="password-obbligatorio"),
            pytest.param({'customerid': 'codice_fiscale', 'username': 'number', 'password': 'chiave-segreta'}, False, id="alunni-obbligatorio"),
        ]
    )
    def test_ConfigurazioneIstituto(self, conf, status):
        from moduli.model_config import ConfigurazioneIstituto
        msg = ""
        if (conf.get('alunni', None) is not None):
            if (isinstance(conf['alunni'], dict)):
                if (conf['alunni'].get('alunno_A', None) is not None):
                    if (isinstance(conf['alunni']['alunno_A'], dict)):
                        conf['alunni']['alunno_A'] = {'tipo': 'html', 'param': 'stringa', 'nome_alternativo': 'stringa'}
        try:
            ConfigurazioneIstituto(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="path-obbligatorio"),
            pytest.param({'path': 'stringa'}, True, id="path-stringa"),
            pytest.param({'path': 12}, False, id="path-not-stringa")
        ]
    )
    def test_ConfigNotificaLocale(self, conf, status):
        from moduli.model_config import ConfigNotificaLocale
        msg = ""
        try:
            ConfigNotificaLocale(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="vuoto"),
            pytest.param({'smtp_server': 12}, False, id="smtp_server-not-stringa"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 'stringa'}, False, id="smtp_port-not-int"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 12}, False, id="smtp_username-not-string"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 12}, False, id="smtp_password-not-string"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': 12}, False, id="destinatari-not-list"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': []}, False, id="destinatari-list"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': [], 'n_allegati': 'stringa'}, False, id="n_allegati-not-int"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': [], 'n_allegati': -10}, False, id="n_allegati-negative-int"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': [], 'n_allegati': 2}, True, id="n_allegati-positive-int"),
            # Campi obbligatori
            pytest.param({'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': [], 'n_allegati': 2}, False, id="smtp_server-obbligatorio"),
            pytest.param({'smtp_server': 'stringa', 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': [], 'n_allegati': 2}, False, id="smtp_port-obbligatorio"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_password': 'password', 'destinatari': [], 'n_allegati': 2}, False, id="smtp_username-obbligatorio"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'destinatari': [], 'n_allegati': 2}, False, id="smtp_password-obbligatorio"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'n_allegati': 2}, False, id="destinatari-obbligatorio"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': []}, False, id="n_allegati-obbligatorio"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': [12], 'n_allegati': 2}, False, id="destinatari-destinatario-not-string"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': ['destinatario'], 'n_allegati': 2}, False, id="destinatari-destinatario-not-email"),
            pytest.param({'smtp_server': 'stringa', 'smtp_port': 456, 'smtp_username': 'username', 'smtp_password': 'password', 'destinatari': ['nome@cognome'], 'n_allegati': 2}, True, id="destinatari-destinatario-email"),
        ]
    )
    def test_ConfigNotificaSmtp(self, conf, status):
        from moduli.model_config import ConfigNotificaSmtp
        msg = ""
        try:
            ConfigNotificaSmtp(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="vuoto"),
            pytest.param({'BOT_TOKEN': 12}, False, id="BOT_TOKEN-not-stringa"),
            pytest.param({'BOT_TOKEN': 'stringa', 'n_allegati': 'stringa'}, False, id="n_allegati-not-int"),
            pytest.param({'BOT_TOKEN': 'stringa', 'n_allegati': -10}, False, id="n_allegati-negative-int"),
            pytest.param({'BOT_TOKEN': 'stringa', 'n_allegati': 10}, True, id="n_allegati-positive-int"),
            pytest.param({'BOT_TOKEN': 'stringa', 'n_allegati': 10, 'CHAT_ID': 12}, False, id="CHAT_ID-not-string"),
            pytest.param({'BOT_TOKEN': 'stringa', 'n_allegati': 10, 'CHAT_ID': 'stringa'}, True, id="CHAT_ID-string"),
            # Campi obbligatori
            pytest.param({'n_allegati': 10}, False, id="BOT_TOKEN-obbligatorio"),
            pytest.param({'BOT_TOKEN': 'stringa'}, False, id="n_allegati-obbligatorio"),
        ]
    )
    def test_ConfigNotificaTelegram(self, conf, status):
        from moduli.model_config import ConfigNotificaTelegram
        msg = ""
        try:
            ConfigNotificaTelegram(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="vuoto"),
            pytest.param({'html': 'stringa'}, False, id="html-not-ConfigNotificaLocale"),
            pytest.param({'screenshot': 'stringa'}, False, id="screenshot-not-ConfigNotificaLocale"),
            pytest.param({'smtp': 'stringa'}, False, id="smtp-not-ConfigNotificaSmtp"),
            pytest.param({'telegram': 'stringa'}, False, id="telegram-not-ConfigNotificaTelegram"),
            pytest.param({'html': {}}, False, id="html-dict-not-ConfigNotificaLocale"),
            pytest.param({'screenshot': {}}, False, id="screenshot-dict-not-ConfigNotificaLocale"),
            pytest.param({'smtp': {}}, False, id="smtp-dict-not-ConfigNotificaSmtp"),
            pytest.param({'telegram': {}}, False, id="telegram-dict-not-ConfigNotificaTelegram"),
        ]
    )
    def test_ParamsNotifiche(self, conf, status):
        from moduli.model_config import ParamsNotifiche
        msg = ""
        try:
            ParamsNotifiche(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg

    @pytest.mark.parametrize(
        "conf, status",
        [
            pytest.param({}, False, id="vuoto"),
            pytest.param({'version': 12}, False, id="version-not-string"),
            pytest.param({'version': 'stringa'}, False, id="version-not-format"),
            pytest.param({'version': '1.1.1', 'credenziali': 'stringa'}, False, id="credenziali-not-list"),
            pytest.param({'version': '1.1.1', 'credenziali': [], 'params_notifiche': 'stringa'}, False, id="params_notifiche-not-dict"),
            pytest.param({'version': '1.1.1', 'credenziali': [], 'params_notifiche': {}}, False, id="params_notifiche-dict-not-ParamsNotifiche"),
            pytest.param({'version': '1.1.1', 'credenziali': [], 'params_notifiche': {'html': {'path': '.'}}}, True, id="params_notifiche-ParamsNotifiche"),
            # Parametri obbligatori
            pytest.param({'credenziali': [], 'params_notifiche': {'html': {'path': '.'}}}, False, id="version-obbligatorio"),
            pytest.param({'version': '1.1.1', 'params_notifiche': {'html': {'path': '.'}}}, False, id="credenziali-obbligatorio"),
            pytest.param({'version': '1.1.1', 'credenziali': []}, False, id="params_notifiche-obbligatorio"),
        ]
    )
    def test_ConfigCredenzialiYaml(self, conf, status):
        from moduli.model_config import ConfigCredenzialiYaml
        msg = ""
        try:
            ConfigCredenzialiYaml(**conf)
            esito = True
        except Exception as e:
            esito = False
            msg = e

        if (status):
            assert esito, msg
        else:
            assert not esito, msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
