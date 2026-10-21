# File di configurazione

Questo è un promemoria per il file di configurazione di Axios-Get.

Contiene la maggior parte delle impostazioni configurabili, insieme ai relativi valori predefiniti.

Il file di configurazione si chiama `credenziali.yml` e deve essere collocato nella cartella principale di Axios-Get.

Il file è scritto in *YAML*: formato basato sull'indentazione e progettato per file di configurazione.

In breve, il linguaggio YAML può gestire tre tipi di dato: scalari (valori singoli), sequenze (liste) e dizionari (corrispondenza chiave-valore). Tutto il resto si può ottenere con l'indentazione e l'utilizzo di combinazioni di questi tre tipi.

Al primo avvio di `AxiosGetCompiti` un file di configurazione di default `credenziali_default.yml` viene creato se `credenziali.yml` non esiste.

Per funzionare, `credenziali_default.yml` deve essere rinominato in `credenziali.yml` e editato, modificando opportunamente i valori delle impostazioni presenti.

## Convezioni del documento

Si indicherà con **RF**: *Axios Registro Elettronico FAMIGLIA*

Inoltre si userà questa convenzione per descrivere la struttura del file di configurazione:

- `Sezione1.Sottosezione2.Chiave: Valore_0` dove il punto sta ad indicare una nuova linea e un'indentazione nel file di configurazione,
- `Sezione1.NomeLista.[]` dove le parentesi quadre stanno a rappresentare il valore dell'elemento della lista, rappresentato nel file con `- Valore_1`

```yaml
Sezione1:
    Sottosezione1:
        Chiave: Valore_0
    NomeLista:
        - Valore_1
```

## Configurazione minima richiesta

La configurazione minima richiesta per il corretto funzionamento riguarda la compilazione di tre blocchi:

- Axios,
- Selezione del tipo di notifica,
- Configurazione di notifica.

## Axios

| Path                           | Tipo dato      | Valore                    | Descrizione                                                      |
| ------------------------------ | -------------- | ------------------------- | ---------------------------------------------------------------- |
| `axios`                        | gruppo         |                           | Gruppo principale della configurazione del sistema               |
| `axios.credenziali`            | gruppo         |                           | Gruppo di definizione delle credenziali di accesso ad **RF**.    |
| `axios.credenziali.customerid` | testo          | Richiesto                 | CF Istituto/Cliente                                              |
| `axios.credenziali.username`   | testo          | Richiesto                 | Codice Utente o mail personale                                   |
| `axios.credenziali.password`   | testo          | Richiesto                 | Password                                                         |
| `axios.alunni`                 | lista          |                           | Lista degli studenti/studentesse (prelevati da **RF**)           |
| `axios.alunni.[0]`             | elemento lista | Il primo Nome in **RF**   | Nome dello studente/studentessa soggetto a notifica              |
| `axios.alunni.[1]`             | elemento lista | Nomi successivi in **RF** | Nomi degli studenti/studentesse soggetto a notifica, se presenti |

## Selezione del tipo di notifica

| Path            | Tipo dato | Valore                          | Descrizione                                              |
| --------------- | --------- | ------------------------------- | -------------------------------------------------------- |
| `tipo_notifica` | testo     | **Nome** del gruppo di notifica | Definisce quale notifica adottare tra quelle configurate |

**NOTA**: i nomi dei gruppo di notifica vengono indicati nelle sezioni successive

## Configurazione di notifica

Scegli la tipologia di notifica che preferisci tra quelle descritte di seguito e inseriscila nel file di configurazione.

### Notifica File

**Obiettivo del tipo di notifica**: salvare in locale la lista dei compiti del registro in un file HTML.

| Path             | Tipo dato | Valore | Descrizione                                                 |
| ---------------- | --------- | ------ | ----------------------------------------------------------- |
| `file_html`      | gruppo    |        | Definizione **nome** del gruppo di notifica                 |
| `file_html.path` | testo     | .      | Percorso relativo o assoluto della cartella di destinazione |

### Notifica Screenshot

**Obiettivo del tipo di notifica**: salvare in locale la lista dei compiti del registro in immagini organizzati per giorno.

| Path              | Tipo dato | Valore | Descrizione                                                 |
| ----------------- | --------- | ------ | ----------------------------------------------------------- |
| `screenshot`      | gruppo    |        | Definizione **nome** del gruppo di notifica                 |
| `screenshot.path` | testo     | .      | Percorso relativo o assoluto della cartella di destinazione |

### Notifica Email

**Obiettivo del tipo di notifica**: inviare in una email la lista dei compiti del registro, e se richiesto allegare screenshot delle pagine diario.

| Path                   | Tipo dato      | Valore | Descrizione                                                        |
| ---------------------- | -------------- | ------ | ------------------------------------------------------------------ |
| `smtp`                 | gruppo         |        | Definizione **nome** del gruppo di notifica                        |
| `smtp.smtp_server`     | testo          |        | indirizzo server SMTP                                              |
| `smtp.smtp_port`       | intero         | 465    | porta SMTP                                                         |
| `smtp.smtp_username`   | testo          |        | username per il login SMTP                                         |
| `smtp.smtp_password`   | testo          |        | password per il login SMTP                                         |
| `smtp.destinatari`     | lista          |        | Lista di email dei destinatari della notifica                      |
| `smtp.destinatari.[0]` | elemento lista | email  | Email di un genitore                                               |
| `smtp.destinatari.[1]` | elemento lista | email  | Email dello studente/studentessa                                   |
| `smtp.destinatari.[2]` | elemento lista | email  | Altra email di un'altro studente/studentessa, se esiste            |
| `smtp.n_allegati`      | intero         | $>=0$  | Numero desiderati di allegati per invio (screenshot pagina diario) |

Consulta il documento [SMTP server](./SMTP_server.md) per verificare i parametri dei provider supportati.

### Notifica Telegram

**Obiettivo del tipo di notifica**: inviare messaggio in chat con la lista dei compiti del registro, e se richiesto allegare screenshot delle pagine diario.

| Path                  | Tipo dato | Valore | Descrizione                                                        |
| --------------------- | --------- | ------ | ------------------------------------------------------------------ |
| `telegram`            | gruppo    |        | Definizione **nome** del gruppo di notifica                        |
| `telegram.BOT_TOKEN`  | testo     |        | TOKEN del bot gestore della notifica                               |
| `telegram.CHAT_ID`    | intero    |        | Numero identificativo della chat                                   |
| `telegram.n_allegati` | intero    |        | Numero desiderati di allegati per invio (screenshot pagina diario) |

Consulta il documento [Telegram_token_bot](./Telegram_token_bot.md) per ottenere il `BOT_TOKEN` e il `CHAT_ID`.

## Configurazione di default

Configurazione di default da compilare:

```yaml
axios:
    credenziali: 
        customerid: STRING_REDACTED
        username: STRING_REDACTED
        password: STRING_REDACTED
    alunni:
        - Nome_Alunno_1
        - Nome_Alunno_2
tipo_notifica: file_html
file_html:
    path: ./pathfile
smtp:
    smtp_server: STRING_REDACTED
    smtp_port: 465
    smtp_username: STRING_REDACTED
    smtp_password: STRING_REDACTED
    destinatari:
        - @EMAIL_REDACTED1
        - @EMAIL_REDACTED2
    n_allegati: 0
telegram:
    BOT_TOKEN: "TOKEN"
    CHAT_ID: "ID"
    n_allegati: 0
screenshot:
    path: ./pathfile
```
