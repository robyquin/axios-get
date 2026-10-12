# Server SMTP

## Provider di Posta Nazionali e Webmail Italiane

Se possiedi già una casella di posta elettronica con uno di questi gestori, i loro server SMTP utilizzano ancora l'autenticazione classica (indirizzo email + password standard della casella), a patto che non sia stata attivata manualmente la verifica in due passaggi.

| Provider      | Supporto   | Server SMTP        | Porta | Sicurezza | Credenziali richieste     | Note                      |
| ------------- | ---------- | ------------------ | ----- | --------- | ------------------------- | ------------------------- |
| Tim           | Verificato | smtp.tim.it        | 587   | STARTTLS  | email Tim + password      | Richiesta connessione Tim |
| Aruba         | Verificato | smtps.aruba.it     | 465   | SSL       | WebEmail Aruba + password |                           |
| Libero Mail   | ?          | smtp.libero.it     | 465   | SSL       | email Libero + password   |                           |
| Virgilio Mail | ?          | smtp.virgilio.it   | 465   | SSL       | email Virgilio + password |                           |
| Tiscali       | Verificato | smtp.tiscali.it    | 465   | SSL       | email Tiscali + password  |                           |
| Fastweb       | ?          | smtp.fastwebnet.it | 465   | SSL       | email Fastweb + password  |                           |
