<img width="1343" height="428" alt="Schermata del 2025-07-25 11-28-44" src="https://github.com/user-attachments/assets/7736c433-d2b3-4f85-898c-99d018016f67" />



Questo programma è un sistema client-server sviluppato in Python progettato per l'invio in tempo reale di segnali di trading XAU/USD (oro/dollaro) attraverso connessioni WebSocket. Il server esegue un'analisi continua dei dati di mercato e invia i segnali ai client connessi. Per garantire la sicurezza e l'accesso controllato, l'intero sistema utilizza un meccanismo di autenticazione basato su key.

Caratteristiche principali:
🔐 Accesso con Key Unica: Ogni utente può accedere solo inserendo una chiave autorizzata, validata tramite hash MD5. Le key possono avere una scadenza temporale (lifetime) configurabile.

📡 Server WebSocket: Il server è sempre attivo e invia segnali ai client connessi in tempo reale, non appena vengono generati.

🧠 Analisi Continua: Il server esegue costantemente analisi tecniche (es. trend, breakout, ecc.) sull'asset XAU/USD per generare segnali operativi (es. BUY o SELL).

🧩 Client Python Interattivo: Il client, dopo aver inserito la propria key, si connette al server e visualizza in modo chiaro i segnali ricevuti.

📆 Gestione della durata della key: Ogni key ha una durata limitata nel tempo. Alla scadenza, l’accesso viene revocato automaticamente.




## Requisiti

* Python ≥ 3.9 
* Windows, Linux o macOS

Dipendenze Python (automatizzate in `requirements.txt`):
```
websockets
rich
pyfiglet
```

Segui il menu, inserisci una KEY valida.

Per la KEY puoi mandarmi un messaggio sul mio sito https://dimitricotilli.it appena visualizzero' il messaggio ti inviero' la KEY.

Se vuoi visionare anche il lato server.py contattami e ti invierò il progetto completo!
