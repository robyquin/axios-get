# Funzionamento

Axios-Get è un progetto open source (sviluppato in Python) pensato per scaricare automaticamente i compiti assegnati sul registro elettronico Axios Famiglia e notificarli direttamente ai figli, superando le barriere burocratiche o legali che spesso impediscono agli studenti di avere un proprio account sul registro elettronico alunni.

Lo script è totalmente cross-platform (compatibile con Linux, MacOS e Windows) e può essere eseguito principalmente in due modi:

⚙️ OneShot (Esecuzione Manuale)

Permette di verificare e scaricare i compiti al momento.

* Su Windows: Basta un doppio clic sul file eseguibile (AxiosGetCompiti.exe) scaricato dalle release.

* Su Linux / MacOS: Si lancia direttamente da terminale con il comando python AxiosGetCompiti.py.

⚙️ Service (Integrazione in uno Schedulatore)

Per evitare di dover cliccare ogni giorno, il tool è progettato per integrarsi perfettamente con i sistemi di automazione per controllare il registro a orari prestabiliti:

* Linux (Systemd): Il repository fornisce già i file di configurazione pronti (.service di tipo oneshot e relativo .timer) per controllare il registro, ad esempio, nella fascia oraria pomeridiana dalle 14:00 alle 18:30.

* Windows: È possibile configurare l'esecuzione automatica programmata tramite l'Utilità di pianificazione (taskschd.msc) di sistema.

## OneShot

```mermaid
stateDiagram
    MR: Main
    C: Legge <b>configurazione</b>
    AGC: <b>AxiosGetCompiti</b>
    SAlunno: Seleziona<br><b>Alunno/a</b>
    GMD: Preleva dati<br>dal <b>Materiale Didattico</b>
    GRF: Preleva dati<br>dai <b>Compiti</b>
    Nfile: <i>Salvataggio</i>
    Nemail: <i>Invio</i>
    Ntelegram: <i>Invio</i>
    BNotifica: Costruisce<br><b>Notifica</b>
    Notificato: <b>Notificato</b><br>all'Alunno/a
    NessunaNotifica: Nessuna <b>Notifica</b><br>all'Alunno/a
    News: Ci sono novità?
    TypeNotify: <b>Tipo di notifica</b>
    state if_state_notifica <<choice>>
    state if_news <<choice>>

    [*] --> AGC
    AGC --> C : Esecuzione
    C --> MR
    state MR {
        SAlunno --> GMD
        GMD --> GRF
        GRF --> BNotifica
        BNotifica --> News
        News --> if_news
        if_news --> TypeNotify : Sì
        if_news --> NessunaNotifica : No
        TypeNotify --> if_state_notifica
        if_state_notifica --> Nfile : <b>File</b>
        if_state_notifica --> Nemail : <b>Email</b>
        if_state_notifica --> Ntelegram : <b>Telegram</b>

        Nfile --> Notificato
        Nemail --> Notificato
        Ntelegram --> Notificato

        Notificato --> SAlunno : Ciclo per ogni<br>alunno/a
        NessunaNotifica --> SAlunno : Ciclo per ogni<br>alunno/a
    }
    MR --> [*]
    
```

## Service

```mermaid
stateDiagram
    Start: <b>Servizio</b>
    Sleep: <b>Attende</b><br>fino al nuovo lancio
    MR: <b>Main</b>

    [*] --> Start
    Start --> MR : Esecuzione
    MR --> Sleep
    Sleep --> MR : ciclo
```
