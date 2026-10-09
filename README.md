# Axios-Get

Notifica ai tuoi figli/e i compiti loro assegnati sul registro elettronico.

**AxiosGetCompiti.py** è pensata per quegli studenti/studentesse a cui non è permesso, per legge o per burocrazia, di avere un account *Axios Registro Elettronico ALUNNI*.

## Requirements

- Python 3.13 or later
- Moduli:
  - `yaml`
  - `requests`

## Installation

```bash
git clone https://github.com/robyquin/axios-get.git
cd axios-get
```

## Configuration

Compila i campi nel file di configurazione *YAML*

```yaml
axios:
    credenziali: 
        customerid: STRING_REDACTED # Inserire CF Istituto/Cliente
        username: STRING_REDACTED   # Codice Utente o mail personale
        password: STRING_REDACTED   # password di accesso ad `Axios Registro Elettronico FAMIGLIA`
    alunni:
        - Nome_Alunno_1             # Lista di nomi come indicato nella Home di `Axios Registro Elettronico FAMIGLIA`
        - Nome_Alunno_2
tipo_notifica: file_html # tipo di notifica da utilizzare
file_html:
    path: ./pathfile # percorso relativo o assoluto della cartella di destinazione
smtp:
    smtp_server: STRING_REDACTED           # indirizzo server SMTP
    smtp_port: 465                         # porta SMTP
    smtp_username: STRING_REDACTED         # username per il login SMTP
    smtp_password: STRING_REDACTED         # password per il login SMTP
    mittente: Genitore <@EMAIL_REDACTED>   # Utilizzato solo per il campo `From:` della mail
    destinatari:
        - @EMAIL_REDACTED1                  # Lista dei destinatari (genitori + studenti)
        - @EMAIL_REDACTED2
```

Tipologie di notifiche:

- **file**: salva un file HTML per Studente/Studentessa in un percorso **path** specifico (`NotificaFileHTML`)
- **smtp**: invia una mail per Studente/Studentessa agli indirizzi **destinatari** specificati (`NotificaMail`)

## Usage

```bash
python /__absolute_path__/AxiosGetCompiti.py
```

**NOTA**: L'utente che lancia lo script deve avere permessi di scrittura su `__absolute_path__`

## Integrazione con Systemd

### axios-compiti.service

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

### axios-compiti.timer

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

### Settings

```bash
systemctl daemon-reload
systemctl enable axios-compiti.timer
systemctl start axios-compiti.timer
```
