# 🚗 Milano EV Analytics - Digital Twin & Profitability

Questo progetto universitario di Data Engineering è incentrato sull'analisi dell'efficienza, dell'utilizzo e della redditività della rete di ricarica per veicoli elettrici (EV) all'interno del Comune di Milano. 

L'obiettivo principale è costruire una pipeline di dati solida in grado di monitorare lo stato delle colonnine e calcolare metriche utili a valutare l'ottimizzazione degli investimenti infrastrutturali.

## 🏗️ Architettura del Sistema

Il progetto è diviso in fasi logiche distinte per garantire la separazione delle competenze:

* 🗺️ **Censimento Geografico (Dati Statici):** Estrazione delle coordinate e delle specifiche tecniche reali di tutte le colonnine di Milano tramite OpenStreetMap (Overpass API).
* ⚡ **Gemello Digitale (Dati Dinamici):** Simulazione probabilistica basata sul comportamento umano e sulle fasce orarie per riprodurre flussi di traffico e cambi di stato realistici (*Available*, *Charging*, *Out of Service*).
* 💾 **Data Ingestion & Storage:** Memorizzazione persistente degli eventi all'interno di una collezione *Time Series* ottimizzata su MongoDB Atlas Cloud.
* 📊 **Data Analytics:** Hub di analisi per elaborare i tassi di occupazione medi, i consumi energetici stimati e i profitti generati dalla rete.

## 🛠️ Tecnologie Utilizzate

* 🐍 **Python 3** (Requests, Pandas, PyMongo, Python-dotenv)
* 🍃 **MongoDB Atlas** (Time Series Collections)
* 🗺️ **OpenStreetMap API** (Overpass QL)
* 🐙 **Git & GitHub** per il controllo di versione collaborativo
