# File di configurazione

Questo è un promemoria per il file di configurazione di Axios-Get.

Contiene la maggior parte delle impostazioni configurabili, insieme ai relativi valori predefiniti.

Il file di configurazione si chiama `credenziali.yml` e deve essere collocato nella cartella principale di Axios-Get.

Il file è scritto in *YAML*: formato basato sull'indentazione e progettato per file di configurazione.

In breve, il linguaggio YAML può gestire tre tipi di dato: scalari (valori singoli), sequenze (liste) e dizionari (corrispondenza chiave-valore). Tutto il resto si può ottenere con l'indentazione e l'utilizzo di combinazioni di questi tre tipi.

Se `credenziali.yml` non esiste, al primo avvio di `AxiosGetCompiti` viene creato un file di configurazione di default `credenziali_default.yml`.

Per funzionare, `credenziali_default.yml` deve essere rinominato in `credenziali.yml` e editato, modificando opportunamente i valori delle impostazioni presenti.

> [!IMPORTANT]
> Con la versione `v1.1.0` il file di configurazione è stato migliorato e riorganizzato per estendere l'utilizzo a tutti i genitori/tutori con più studenti appartenenti anche a istituti differenti (con più credenziali).
>
> Da questa release viene implementata la migrazione automatica della configurazione da una versione precedente, tuttavia, prima dell'effettivo utilizzo del nuovo file, occorre verificare la correttezza di tutti dati.
>
> La procedura di migrazione è non distruttiva, al primo avvio della una nuova release verrà generato il file aggiornato con il nome `credenziali_{versione}.yml`. Dopo la verifica/controllo dell'esattezza dei dati il file dovrà essere rinominato in `credenziali.yml` per rendere le modifiche effettive.

## Convenzioni del documento

Si indicherà con **RF**: *Axios Registro Elettronico FAMIGLIA*

Inoltre si userà la seguente convenzione per descrivere la struttura adottata in `credenziali.yml`:

- `Sezione1.Sottosezione2.Chiave: Valore_0` dove il punto sta ad indicare una nuova linea e un'indentazione nel file,
- `Sezione1.NomeLista.[]` dove le parentesi quadre stanno a rappresentare il valore dell'elemento della lista (`- Valore_1`)

```yaml
Sezione1:
    Sottosezione1:
        Chiave: Valore_0
    NomeLista:
        - Valore_1
```

## Configurazione minima richiesta

Per indicazioni per configurazione `<= v1.0.8` visiona il file [Configurazione v1.0.8](https://github.com/robyquin/axios-get/blob/v1.0.8/docs/Configurazione.md)

La configurazione minima richiesta per il corretto funzionamento riguarda la compilazione di due blocchi:

- version
- credenziali,
- params_notifiche.

## Version

Indica la versione del file di configurazione.

| Path      | Tipo dato | Valore | Descrizione |
| --------- | --------- | ------ | ----------- |
| `version` | testo     |        | Versione.   |

## Credenziali

| Path                                       | Tipo dato | Valore                                                    | Descrizione                                                      |
| ------------------------------------------ | --------- | --------------------------------------------------------- | ---------------------------------------------------------------- |
| `credenziali`                              | lista     |                                                           | Lista di definizione delle credenziali di accesso ad **RF**.     |
| `credenziali.[0].customerid`               | testo     | Richiesto                                                 | CF Istituto/Cliente                                              |
| `credenziali.[0].username`                 | testo     | Richiesto                                                 | Codice Utente o mail personale                                   |
| `credenziali.[0].password`                 | testo     | Richiesto                                                 | Password                                                         |
| `credenziali.[0].alunni`                   | gruppo    |                                                           | Gruppo degli studenti/studentesse (prelevati da **RF**)          |
| `credenziali.[0].alunni.NomeAlunnoA`       | gruppo    | Il primo Nome in **RF**                                   | Nome dello studente/studentessa soggetto a notifica              |
| `credenziali.[0].alunni.NomeAlunnoA.tipo`  | testo     | **Nome** del gruppo di notifica                           | Definisce quale notifica adottare tra quelle configurate         |
| `credenziali.[0].alunni.NomeAlunnoA.param` | testo     | **Parametro caratteristico** per la tipologia di notifica | Percorso, email studente, o CHAT_ID                              |
| `credenziali.[0].alunni.NomeAlunnoB`       | gruppo    | Nomi successivi in **RF**                                 | Nomi degli studenti/studentesse soggetto a notifica, se presenti |
| `credenziali.[0].alunni.NomeAlunnoB.tipo`  | testo     | **Nome** del gruppo di notifica                           | Definisce quale notifica adottare tra quelle configurate         |
| `credenziali.[0].alunni.NomeAlunnoB.param` | testo     | **Parametro caratteristico** per la tipologia di notifica | Percorso, email studente, o CHAT_ID                              |

**NOTA**: sia i nomi dei gruppo di notifica, che le indicazioni dei parametri caratteristici vengono indicati nelle sezioni successive

## Configurazione di notifica (`params_notifiche`)

Scegli la tipologia di notifica che preferisci tra quelle descritte di seguito e inseriscila nel file `credenziali.yml`.

### Notifica `html`

**Obiettivo del tipo di notifica**: salvare in locale la lista dei compiti del registro in un file HTML.

| Path                         | Tipo dato | Valore | Descrizione                                                                                                                   |
| ---------------------------- | --------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `params_notifiche.html`      | gruppo    |        | Definizione **nome** del gruppo di notifica                                                                                   |
| `params_notifiche.html.path` | testo     | .      | Percorso relativo o assoluto della cartella di destinazione (valore di default se non dovesse esistere quello dello studente) |

- **Parametro caratteristico** di questa notifica è il percorso relativo o assoluto della cartella di destinazione

### Notifica `screenshot`

**Obiettivo del tipo di notifica**: salvare in locale la lista dei compiti del registro in immagini organizzate per giorno.

| Path                               | Tipo dato | Valore | Descrizione                                                                                                                   |
| ---------------------------------- | --------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `params_notifiche.screenshot`      | gruppo    |        | Definizione **nome** del gruppo di notifica                                                                                   |
| `params_notifiche.screenshot.path` | testo     | .      | Percorso relativo o assoluto della cartella di destinazione (valore di default se non dovesse esistere quello dello studente) |

- **Parametro caratteristico** di questa notifica è il percorso relativo o assoluto della cartella di destinazione

### Notifica `smtp`

**Obiettivo del tipo di notifica**: inviare in una email la lista dei compiti del registro, e se richiesto, allegare screenshot delle pagine diario.

| Path                                    | Tipo dato      | Valore | Descrizione                                                        |
| --------------------------------------- | -------------- | ------ | ------------------------------------------------------------------ |
| `params_notifiche.smtp`                 | gruppo         |        | Definizione **nome** del gruppo di notifica                        |
| `params_notifiche.smtp.smtp_server`     | testo          |        | indirizzo server SMTP                                              |
| `params_notifiche.smtp.smtp_port`       | intero         | 465    | porta SMTP                                                         |
| `params_notifiche.smtp.smtp_username`   | testo          |        | username per il login SMTP                                         |
| `params_notifiche.smtp.smtp_password`   | testo          |        | password per il login SMTP                                         |
| `params_notifiche.smtp.destinatari`     | lista          |        | Lista di email dei destinatari della notifica                      |
| `params_notifiche.smtp.destinatari.[0]` | elemento lista | email  | Email di un genitore/tutore                                        |
| `params_notifiche.smtp.destinatari.[1]` | elemento lista | email  | Eventuale altra email di genitore/tutore                           |
| `params_notifiche.smtp.n_allegati`      | intero         | $>=0$  | Numero desiderati di allegati per invio (screenshot pagina diario) |

Consulta il documento [SMTP server](./SMTP_server.md) per verificare i parametri dei provider supportati.

- **Parametro caratteristico** di questa notifica è `EMAIL_STUDENTE`

### Notifica `telegram`

**Obiettivo del tipo di notifica**: inviare messaggio in chat con la lista dei compiti del registro, e se richiesto, allegare screenshot delle pagine diario.

| Path                                   | Tipo dato | Valore | Descrizione                                                        |
| -------------------------------------- | --------- | ------ | ------------------------------------------------------------------ |
| `params_notifiche.telegram`            | gruppo    |        | Definizione **nome** del gruppo di notifica                        |
| `params_notifiche.telegram.BOT_TOKEN`  | testo     |        | TOKEN del bot gestore della notifica                               |
| `params_notifiche.telegram.CHAT_ID`    | intero    |        | Numero identificativo della chat                                   |
| `params_notifiche.telegram.n_allegati` | intero    |        | Numero desiderati di allegati per invio (screenshot pagina diario) |

- **Parametro caratteristico** di questa notifica è `CHAT_ID`: Numero identificativo della chat.

Consulta il documento [Telegram_token_bot](./Telegram_token_bot.md) per ottenere il `BOT_TOKEN` e il `CHAT_ID`.

## Configurazione di default

Configurazione di default da compilare:

```yaml
axios:
version: 1.1.0
credenziali:
- customerid: customerid
  username: username
  password: password
  alunni:
    NOME_ALUNNO_A:
      tipo: smtp
      param: EMAIL_STUDENTE
    NOME_ALUNNO_B:
      tipo: html
      param: ./pathfile
    NOME_ALUNNO_C:
      tipo: screenshot
      param: ./pathfile
    NOME_ALUNNO_D:
      tipo: telegram
      param: CHAT_ID
params_notifiche:
  html:
    path: ./pathfile
  smtp:
    smtp_server: smtp.example.it
    smtp_port: 465
    smtp_username: Username
    smtp_password: PaSsWoRd
    destinatari:
    - tutore@example.it
    n_allegati: 0
  telegram:
    BOT_TOKEN: TOKEN
    CHAT_ID: ID
    n_allegati: 0
  screenshot:
    path: ./pathfile
```
