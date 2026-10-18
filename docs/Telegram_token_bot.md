# Telegram

## Come ottenere il *BOT_TOKEN*

Per ottenere un token per un bot Telegram devi utilizzare BotFather, il bot ufficiale di Telegram creato per gestire e configurare tutti i bot sulla piattaforma. Il processo richiede pochissimi minuti ed è completamente gratuito.
Ecco i passaggi sequenziali per crearlo:

1. **Cerca BotFather**: Apri Telegram e digita `@BotFather` nella barra di ricerca. Assicurati che abbia la spunta blu di verifica per evitare bot contraffatti.
2. **Avvia la chat**: Clicca sul bot e premi il pulsante Avvia (o digita /start).
3. **Crea il nuovo bot**: Invia il comando /newbot. BotFather ti risponderà chiedendoti di impostare un nome per il tuo bot.
4. **Scegli il nome**: Digita il nome visibile del bot (ad esempio: Il Mio Assistente). Questo nome può essere modificato anche in seguito.
5. **Scegli lo username**: Invia lo username univoco del bot. Deve essere scritto in caratteri latini e deve terminare obbligatoriamente con la parola "bot" (ad esempio: MioAssistente_bot oppure MioAssistenteBot).

Una volta completato l'ultimo passaggio, BotFather ti invierà un messaggio di congratulazioni contenente il tuo token d'accesso (una stringa alfanumerica simile a questa: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ).

## Come ottenere la *CHAT_ID*

Per ottenere la chat_id di Telegram (l'identificativo univoco di una chat privata, di un gruppo o del tuo stesso profilo utente), esistono due metodi principali: il più rapido tramite un bot Telegram già pronto oppure quello classico tramite le API di Telegram usando il token del tuo bot.

Ecco come procedere in base alla soluzione che preferisci.

### Metodo 1: Il più veloce (Utilizzando un Bot Telegram)

Se hai bisogno di trovare al volo la tua chat_id personale o quella di un gruppo, puoi usare un bot adibito a questo scopo:

1. Cerca il bot `@userinfobot` (o in alternativa `@RawDataBot`) nella barra di ricerca di Telegram.
2. Avvia la chat cliccando su Avvia (o inviando /start).
3. Il bot ti risponderà immediatamente mostrando i tuoi dati. Il numero contrassegnato come Id: corrisponde esattamente alla tua chat_id.

Se cerchi la chat_id di un gruppo: Aggiungi temporaneamente uno di questi bot all'interno del gruppo. Non appena entrerà o riceverà un comando, il bot scriverà nel gruppo l'ID della chat (i codici dei gruppi iniziano sempre con un meno, ad esempio -100123456789).

### Metodo 2: Tramite API (Se stai sviluppando un Bot)

Se hai appena creato un bot con BotFather e hai bisogno della chat_id per inviare messaggi via codice, usa il browser:

1. Cerca il tuo bot su Telegram e avvia la conversazione cliccando su Avvia o inviando un messaggio qualsiasi (passaggio fondamentale, altrimenti la cronologia risulterà vuota).
2. Apri il browser e incolla questo URL, sostituendo {token} con il token HTTP API che ti ha fornito BotFather:
<https://api.telegram.org/bot{token}/getUpdates>
(Nota: Ricordati di mantenere la parola bot prima del codice del token).
3. Premi Invio. Ti apparirà una pagina di testo in formato JSON.

```
Suggerimento: Se la pagina del browser mostra il risultato {"ok":true,"result":[]}, significa che il bot non ha ricevuto messaggi recenti. Torna su Telegram, invia un nuovo messaggio al bot e aggiorna la pagina del browser.
```
