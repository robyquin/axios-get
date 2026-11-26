"""
Test per la funzione prepara_notifica di lib_axios_famiglia.py

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

Test unitari per la funzione prepara_notifica senza accesso a rete.
"""

import pytest
import sys
import os
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
# from unittest.mock import patch, MagicMock

# Aggiungi il percorso del progetto
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestPreparaNotifica:
    """Test della funzione prepara_notifica."""

    @pytest.mark.parametrize("expected_pattern", [
                "<html>",
                "<head><style>",
                "</style></head>",
                "<body>",
                "<h1>Compiti per Mario</h1>",
                "</p>",
                "<!-- BEGIN COMPITI -->",
                "<!-- END COMPITI -->",
                "<!-- BEGIN SCREENSHOT -->",
                "<!-- END SCREENSHOT -->",
                "<h2 class='diario'>📰 ",
                "</h2>",
                "<h3>Matematica</h3>",
                "<h3>Italiano</h3>",
                "<h3>Storia</h3>",
                "<li class='compiti'>Esercizi capitolo 5</li>",
                "<li class='verifica'><b>Verifica</b>: Numeri romani</li>",
                "<li class='annotazione'><b>Annotazione</b>: portare libro</li>",
                "</body>",
                "</html>"
            ]
    )
    def test_prepara_notifica_creates_html_structure(self, expected_pattern):
        """Test che prepara_notifica crea la struttura HTML corretta."""
        from moduli.lib_axios_famiglia import LibAxiosFamiglia, AxiosView
        
        oggi = datetime.now()
        domani = (oggi + timedelta(days=1)).strftime("%d/%m/%Y")
        domani2 = (oggi + timedelta(days=2)).strftime("%d/%m/%Y")
        domani3 = (oggi + timedelta(days=3)).strftime("%d/%m/%Y")
        # Dati simulati
        compiti = {
            "data": [
                {
                    "giorno": domani,
                    "materia": "Matematica",
                    "testo": "Esercizi capitolo 5",
                    "verifica": ""
                },
                {
                    "giorno": domani2,
                    "materia": "Italiano",
                    "testo": "Compiti casa",
                    "verifica": "",
                    "note": "portare libro"
                },
                {
                    "giorno": domani3,
                    "materia": "Storia",
                    "testo": "Compiti casa",
                    "verifica": "Numeri romani"
                }
            ]
        }
        argomenti = {
            "data": []
        }
        Alunno = "Mario"

        LAF = LibAxiosFamiglia
        LAF.alunni = {}
        LAF.alunni[AxiosView.registro] = {}
        LAF.alunni[AxiosView.registro][Alunno] = Alunno
        LAF.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES = []
        LAF.sha1_REGISTRO = "test"
        LAF.sha1_REGISTRO_old = "test"
        LAF.sha1_MD = ""
        LAF.sha1_MD_old = ""

        LAF.dir_istituto = tempfile.TemporaryDirectory().name
        dir_alunno = f'{AxiosView.registro}_{Alunno}_{hashlib.md5(LAF.alunni[AxiosView.registro][Alunno].encode('utf-8')).hexdigest()}'
        if (not os.path.exists(os.path.join(LAF.dir_istituto, dir_alunno))):
            os.makedirs(os.path.join(LAF.dir_istituto, dir_alunno))
        html_output = LAF.prepara_notifica(LAF, compiti, argomenti, Alunno)
        os.remove(os.path.join(LAF.dir_istituto, dir_alunno, 'notifica.html'))
        os.removedirs(os.path.join(LAF.dir_istituto, dir_alunno))

        assert expected_pattern in html_output

    @pytest.mark.parametrize("expected_pattern", [
                "style='color:green'",
                "style='color:orange'"
            ]
    )
    def test_prepara_notifica_creates_html_structure_cambiamenti(self, expected_pattern):
        """Test che prepara_notifica crea la struttura HTML corretta."""
        from moduli.lib_axios_famiglia import LibAxiosFamiglia, AxiosView
        
        oggi = datetime.now()
        domani = (oggi + timedelta(days=1)).strftime("%d/%m/%Y")
        domani2 = (oggi + timedelta(days=2)).strftime("%d/%m/%Y")
        domani3 = (oggi + timedelta(days=3)).strftime("%d/%m/%Y")
        # Dati simulati
        compiti = {
            "data": [
                {
                    "giorno": domani,
                    "materia": "Matematica",
                    "testo": "Esercizi capitolo 5",
                    "verifica": ""
                },
                {
                    "giorno": domani2,
                    "materia": "Italiano",
                    "testo": "Compiti casa",
                    "verifica": "",
                    "note": "portare libro"
                }
            ]
        }
        argomenti = {
            "data": []
        }
        Alunno = "Mario"

        LAF = LibAxiosFamiglia
        LAF.alunni = {}
        LAF.alunni[AxiosView.registro] = {}
        LAF.alunni[AxiosView.registro][Alunno] = Alunno
        LAF.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES = []
        LAF.sha1_REGISTRO = "test"
        LAF.sha1_REGISTRO_old = "test"
        LAF.sha1_MD = ""
        LAF.sha1_MD_old = ""

        LAF.dir_istituto = tempfile.TemporaryDirectory().name
        dir_alunno = f'{AxiosView.registro}_{Alunno}_{hashlib.md5(LAF.alunni[AxiosView.registro][Alunno].encode('utf-8')).hexdigest()}'
        if (not os.path.exists(os.path.join(LAF.dir_istituto, dir_alunno))):
            os.makedirs(os.path.join(LAF.dir_istituto, dir_alunno))
        html_output_old = LAF.prepara_notifica(LAF, compiti, argomenti, Alunno)
        os.remove(os.path.join(LAF.dir_istituto, dir_alunno, 'notifica.html'))
        os.removedirs(os.path.join(LAF.dir_istituto, dir_alunno))
        compiti['data'].append(
                {
                    "giorno": domani3,
                    "materia": "Storia",
                    "testo": "Compiti casa",
                    "verifica": "Numeri romani"
                })
        compiti['data'][0]["testo"] = "Esercizi capitolo 4"
        LAF.dir_istituto = tempfile.TemporaryDirectory().name
        if (not os.path.exists(os.path.join(LAF.dir_istituto, dir_alunno))):
            os.makedirs(os.path.join(LAF.dir_istituto, dir_alunno))
        html_output_new = LAF.prepara_notifica(LAF, compiti, argomenti, Alunno)
        html_output_list = LAF.evidenzia_cambiamenti(LAF, html_output_old.split("\n"), html_output_new.split("\n"))
        os.remove(os.path.join(LAF.dir_istituto, dir_alunno, 'notifica.html'))
        os.removedirs(os.path.join(LAF.dir_istituto, dir_alunno))

        html_output = "\n".join(html_output_list)

        assert expected_pattern in html_output

    @pytest.mark.parametrize("expected_pattern", [
                "<!-- BEGIN SCREENSHOT -->",
                "<!-- END SCREENSHOT -->"
                "<h3>Matematica</h3>",
                "<h3>Italiano</h3>",
                "<h3>Storia</h3>"
            ]
    )
    def test_prepara_notifica_filter_future_dates(self, expected_pattern):
        """Test che i compiti passati non siano inclusi."""

        from moduli.lib_axios_famiglia import LibAxiosFamiglia, AxiosView
                
        now = datetime.now()
        oggi = now.strftime("%d/%m/%Y")
        ieri = (now - timedelta(days=1)).strftime("%d/%m/%Y")
        ieri1 = (now - timedelta(days=2)).strftime("%d/%m/%Y")
        # Dati simulati
        compiti = {
            "data": [
                {
                    "giorno": oggi,
                    "materia": "Matematica",
                    "testo": "Esercizi capitolo 5",
                    "verifica": ""
                },
                {
                    "giorno": ieri,
                    "materia": "Italiano",
                    "testo": "Compiti casa",
                    "verifica": "",
                    "note": "portare libro"
                },
                {
                    "giorno": ieri1,
                    "materia": "Storia",
                    "testo": "Compiti casa",
                    "verifica": "Numeri romani"
                }
            ]
        }
        argomenti = {
            "data": []
        }
        Alunno = "Mario"

        LAF = LibAxiosFamiglia
        LAF.alunni = {}
        LAF.alunni[AxiosView.registro] = {}
        LAF.alunni[AxiosView.registro][Alunno] = Alunno
        LAF.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES = []
        LAF.sha1_REGISTRO = "test"
        LAF.sha1_REGISTRO_old = "test"
        LAF.sha1_MD = ""
        LAF.sha1_MD_old = ""

        LAF.dir_istituto = tempfile.TemporaryDirectory().name
        dir_alunno = f'{AxiosView.registro}_{Alunno}_{hashlib.md5(LAF.alunni[AxiosView.registro][Alunno].encode('utf-8')).hexdigest()}'
        if (not os.path.exists(os.path.join(LAF.dir_istituto, dir_alunno))):
            os.makedirs(os.path.join(LAF.dir_istituto, dir_alunno))
        html_output = LAF.prepara_notifica(LAF, compiti, argomenti, Alunno)
        os.remove(os.path.join(LAF.dir_istituto, dir_alunno, 'notifica.html'))
        os.removedirs(os.path.join(LAF.dir_istituto, dir_alunno))

        assert expected_pattern not in html_output

    @pytest.mark.parametrize("expected_pattern, should_exist", [
                    ("<!-- BEGIN SCREENSHOT -->", False),
                    ("<!-- END SCREENSHOT -->", False),
                    ("<!-- BEGIN COMPITI -->", True),
                    ("<!-- END COMPITI -->", True),
                    ("<h3>Matematica</h3>", False),
                    ("<h3>Italiano</h3>", False),
                    ("<h3>Storia</h3>", False)
                ]
        )
    def test_prepara_notifica_empty_compiti(self, expected_pattern, should_exist):
        """Test con nessun compito."""
        from moduli.lib_axios_famiglia import LibAxiosFamiglia, AxiosView

        # Dati simulati
        compiti = {
            "data": []
        }
        argomenti = {
            "data": []
        }
        Alunno = "Mario"

        LAF = LibAxiosFamiglia
        LAF.alunni = {}
        LAF.alunni[AxiosView.registro] = {}
        LAF.alunni[AxiosView.registro][Alunno] = Alunno
        LAF.dir_istituto = './_tmp'
        LAF.MATERIALE_CONDIVISO_ALUNNO_TEXT_LINES = []
        LAF.sha1_REGISTRO = "test"
        LAF.sha1_REGISTRO_old = "test"
        LAF.sha1_MD = ""
        LAF.sha1_MD_old = ""

        dir_alunno = f'{AxiosView.registro}_{Alunno}_{hashlib.md5(LAF.alunni[AxiosView.registro][Alunno].encode('utf-8')).hexdigest()}'
        if (not os.path.exists(os.path.join(LAF.dir_istituto, dir_alunno))):
            os.makedirs(os.path.join(LAF.dir_istituto, dir_alunno))
        html_output = LAF.prepara_notifica(LAF, compiti, argomenti, Alunno)
        os.remove(os.path.join(LAF.dir_istituto, dir_alunno, 'notifica.html'))
        os.removedirs(os.path.join(LAF.dir_istituto, dir_alunno))

        if (should_exist):
            assert expected_pattern in html_output
        else:
            assert expected_pattern not in html_output

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
