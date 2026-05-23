import requests
import logging
from datetime import datetime, timezone
import config
import database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def scarica_anagrafica_osm():
    logging.info("🌍 Inizio download anagrafica colonnine da OpenStreetMap (Milano)...")
    
    overpass_url = "https://lz4.overpass-api.de/api/interpreter"
    
    overpass_query = """
    [out:json][timeout:90];
    area["name"="Milano"]["admin_level"="8"]->.searchArea;
    (
      node["amenity"="charging_station"](area.searchArea);
    );
    out body;
    """
    
    # LE CREDENZIALI DI ACCESSO: Diciamo al server chi siamo e cosa vogliamo
    headers = {
        "User-Agent": "Milano_EV_University_Project/1.0 (studente@unimib.it)",
        "Accept": "application/json"
    }
    
    try:
        # Inviamo la query direttamente nel body come testo puro (la modalità preferita da OSM)
        response = requests.post(
            overpass_url, 
            data=overpass_query.encode('utf-8'), 
            headers=headers
        )
        
        if response.status_code != 200:
            logging.error(f"❌ Errore Server OSM (Codice {response.status_code}): {response.text}")
            return
            
        dati_osm = response.json()
        colonnine = dati_osm.get('elements', [])
        
        if len(colonnine) == 0:
            logging.warning("⚠️ La query ha avuto successo, ma OSM ha restituito 0 colonnine. C'è un problema geometrico.")
            return
            
        logging.info(f"✅ Trovate {len(colonnine)} colonnine fisiche in OSM.")
        
        client = database.get_db_client()
        db = client[config.DB_NAME]
        collection = db['stations_osm_registry']
        
        # Svuotiamo i vecchi tentativi
        collection.delete_many({})
        
        documenti_da_salvare = []
        for nodo in colonnine:
            tags = nodo.get('tags', {})
            doc = {
                "osm_id": nodo.get('id'),
                "latitude": nodo.get('lat'),
                "longitude": nodo.get('lon'),
                "operator": tags.get('operator', 'Sconosciuto'),
                "capacity": tags.get('capacity', '1'),
                "max_power_kw": tags.get('charging_station:output', 'Sconosciuto'),
                "data_censimento": datetime.now(timezone.utc)
            }
            documenti_da_salvare.append(doc)
            
        if documenti_da_salvare:
            collection.insert_many(documenti_da_salvare)
            logging.info(f"💾 Salvate {len(documenti_da_salvare)} anagrafiche in MongoDB Atlas.")
            
        client.close()
        
    except Exception as e:
        logging.error(f"❌ Errore di sistema durante il censimento: {e}")

if __name__ == "__main__":
    scarica_anagrafica_osm()