import requests
import config

print("🔍 Avvio Micro-Test API OpenChargeMap...")

headers = {
    "User-Agent": "Milano_EV_University_Project/3.0",
    "X-API-Key": config.API_KEY
}

params = {
    "output": "json",
    "latitude": 45.4642,
    "longitude": 9.1900,
    "distance": 1,        # Solo 1 km
    "maxresults": 2       # Chiediamo SOLO 2 colonnine!
}

try:
    print("⏳ Contatto il server...")
    response = requests.get(
        "https://api.openchargemap.io/v3/poi/", 
        headers=headers, 
        params=params, 
        timeout=10
    )
    response.raise_for_status()
    data = response.json()
    print(f"✅ SUCCESSO! Il server è vivo. Ha restituito {len(data)} colonnine.")
    for idx, station in enumerate(data):
        print(f"   -> Colonnina {idx+1}: {station.get('AddressInfo', {}).get('Title')}")
        
except Exception as e:
    print(f"❌ FALLIMENTO TOTALE. Il server non risponde nemmeno a richieste piccolissime.")
    print(f"   Errore tecnico: {e}")