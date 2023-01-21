# Progetto prenotazione cup marche
Script python che controlla a intervalli regolari la disponibilità di visite mediche dal cup online delle marche, dato il numero di ricetta e il codice fiscale. Se viene trovata una disponibilità, invia una notifica tramite email.

Il sito di riferimento è il seguente:

https://mycupmarche.it/prenotazionecittadino/

In cui viene utilizzata la modalità "senza credenziali", ovvero inserendo a mano il codice fiscale anzichè fare il login con spid.
## Utilizzo
Con il comando ``` python prenotazione.py --help ``` verrà fuori il messaggio di help:
```
usage: prenotazione.py [-h] --cf CF --ricetta RICETTA --sender SENDER --password PASSWORD --receiver RECEIVER [--timespan TIMESPAN] [--port PORT] [--smtp SMTP] [--headless [HEADLESS]]

Script che invia una notifica mail quando si libera un posto per il cup marche

options:
  -h, --help            show this help message and exit
  --cf CF               Codice fiscale
  --ricetta RICETTA     Ricetta
  --sender SENDER       Email mittente
  --password PASSWORD   Password email mittente
  --receiver RECEIVER   Email destinatario
  --timespan TIMESPAN   Intervallo controllo (minuti)
  --port PORT           Porta smtp
  --smtp SMTP           Smtp server
  --headless [HEADLESS] Chrome headless
``` 

I parametri obbligatori sono codice fiscale, ricetta, email sender, password email sender, receiver email.

Esempio:
```
python prenotazione.py --cf NCLDNLXXXXXXXXXX --ricetta 41XXXXXX60 --sender xxxxx@gmail.com --password xxxxx --receiver xxxxx@gmail.com --timespan 1
```

