#!python
"""
Modulo di configurazione di **logging** utilizzato per assicurare un unico stile di output.

:Author: Roberto Quintiliani
:Copyright: Copyright (c) Roberto Quintiliani
:License: MIT

"""

import logging

# --- Configurazione logger ---

log = logging.getLogger()

# Handler console con colori
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(console_formatter)
log.addHandler(console_handler)
log.setLevel(logging.INFO)
