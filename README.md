# Axios-Get

Notifica ai tuoi figli/e i compiti loro assegnati sul registro elettronico.

**AxiosGetCompiti.py** è pensata per quegli studenti/studentesse a cui non è permesso, per legge o per burocrazia, di avere un account *Axios Registro Elettronico ALUNNI*.

![Axios-Get](./icon/Axios-Get.svg)

## Requirements

- Python 3.13 or later
- Moduli:
  - `yaml`
  - `requests`
  - `pillow`

## Installation

### Installation from source

```bash
git clone https://github.com/robyquin/axios-get.git
cd axios-get
```

- Passa alla *configurazione*

### Installation from binary

**Windows Users**:

- Fai il [download dell'ultima release](https://github.com/robyquin/axios-get/releases/latest)
- Estrai l'archivio in una cartella
- Passa alla *configurazione*

## Configuration

Per la prima configurazione occorre creare un file, se non esiste, con il nome `credenziali.yml` nella stessa cartella di **AxiosGetCompiti**.

- Se al primo avvio, il file non esiste, riceverete un messaggio di errore con la conseguente creazione di `credenziali_default.yml`, rinominatelo in `credenziali.yml`, sarà un ottimo punto di partenza per la compilazione.

- Per la compilazione dei campi del file e per conoscere tutte le tipologie di notifiche disponibili, segui le indicazioni nel documento [CONFIGURAZIONE](./docs/Configurazione.md)

## Usage

### Unix Like

```bash
python /__absolute_path__/AxiosGetCompiti.py
```

**NOTA**: L'utente che lancia lo script deve avere permessi di scrittura su `__absolute_path__`

### Windows Like

Semplicemente doppio click su `AxiosGetCompiti.exe`

## Integrazione con schedulatori

### Unix Like (Systemd)

Crea i file di servizio `axios-compiti.service` e `axios-compiti.timer`

#### axios-compiti.service

```bash
# /etc/systemd/system/axios-compiti.service
[Unit]
Description=Servizio per Axios-Compiti

[Service]
Type=oneshot
ExecStart=python /__absolute_path__/AxiosGetCompiti.py
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

#### axios-compiti.timer

```bash
# /etc/systemd/system/axios-compiti.timer
[Unit]
Description=Timer per Axios-Compiti

[Timer]
OnCalendar=*-*-* 14..18:30
Unit=axios-compiti.service

[Install]
WantedBy=timers.target
```

#### Settings

```bash
systemctl daemon-reload
systemctl enable axios-compiti.timer
systemctl start axios-compiti.timer
```

### Windows Like

- Premi i tasti `Win + R`, scrivi `taskschd.msc run` e premi Invio.

oppure

- Clicca sul pulsante **Start**, digita **Utilità di pianificazione** e seleziona il risultato.

Per la configurazione di questo schedulatore, ti chiedo gentilmente di seguire le informazioni che trovi in rete.

## Licenza

Questo progetto è concesso in licenza nei termini della licenza **MIT** (vedi il file `LICENSE` per i dettagli).

### Componenti di terze parti

Il font incluso nella cartella `assets/fonts/` è distribuito sotto licenza **Apache License 2.0**.

- **OpenSansEmoji.ttf** - Copyright (c) [2013] [Merten Peetz].
- Il testo della licenza del font è disponibile in `assets/fonts/LICENSE-FONT.txt`.
