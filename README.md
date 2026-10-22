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

- Premi i tasti `Win + R`, scrivi `taskschd.msc run` e premi Invio, oppure clicca sul pulsante **Start**, digita **Utilità di pianificazione** e seleziona il risultato.
- **Crea un'attività** inserendo tutti i parametri richiesti per la pianificazione dell'esecuzione automatica di AxiosGetCompiti.

**NOTA**: Per la configurazione di questo schedulatore, ti chiedo gentilmente di seguire le informazioni che trovi in rete.

Un alternativa alla creazione manuale della pianificazione, ti suggerisco i passi per l'**Importazione attività**:

- Copia il codice che trovi nella sezione `Configurazione attività`,
- Incollalo in un file chiamato `schedula_axios-get.xml`,
- Sostituisci `__absolute_path__` con il percorso reale di dove hai installato *AxiosGetCompiti.exe* (es. `C:\axios-get_v1.0.5`). Per le release più recenti (`>= v1.0.6`), nella cartella di prima installazione troverai già il template del file (`schedula_axios-get.xml_tmp`); al primo avvio verrà sostituito in automatico il valore corretto di `__absolute_path__`, e il file verrà rinominato in `schedula_axios-get.xml`.
- In **Utilità di pianificazione**, *Importa attività*, ti verrà richiesto di selezionare `schedula_axios-get.xml`

Il seguente file di configurazione imposta 5 attivazioni giornaliere di *AxiosGetCompiti.exe*:

- Ogni giorno alle 14:30
- Ogni giorno alle 15:30
- Ogni giorno alle 16:30
- Ogni giorno alle 17:30
- Ogni giorno alle 18:30

#### Configurazione attività

```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2026-10-21T18:00:00</Date>
    <Author>Axios-Get</Author>
    <Description>Schedulazione di Axios-Get</Description>
    <URI>\Axios-get</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-10-21T14:30:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
    <CalendarTrigger>
      <StartBoundary>2026-10-21T15:30:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
    <CalendarTrigger>
      <StartBoundary>2026-10-21T16:30:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
    <CalendarTrigger>
      <StartBoundary>2026-10-21T17:30:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
    <CalendarTrigger>
      <StartBoundary>2026-10-21T18:30:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>NT AUTHORITY\SYSTEM</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT72H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>__absolute_path__\AxiosGetCompiti.exe</Command>
      <WorkingDirectory>__absolute_path__</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
```

## Licenza

Questo progetto è concesso in licenza nei termini della licenza **MIT** (vedi il file `LICENSE` per i dettagli).

### Componenti di terze parti

Il font incluso nella cartella `assets/fonts/` è distribuito sotto licenza **Apache License 2.0**.

- **OpenSansEmoji.ttf** - Copyright (c) [2013] [Merten Peetz].
- Il testo della licenza del font è disponibile in `assets/fonts/LICENSE-FONT.txt`.
