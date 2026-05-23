import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

API_KEY = os.getenv("API_KEY_OPEN_CHARGE_MAP")
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("⚠️ Manca la stringa MONGO_URI nel file .env!")

# Coordinate del Comune di Milano
MILANO_LAT = 45.4642
MILANO_LON = 9.1900
RADIUS_KM = 8

POLLING_INTERVAL = 900  # 15 minuti in secondi

DB_NAME = "ev_analytics_milano"
COLLECTION_NAME = "charging_events"

HEADERS = {
    "User-Agent": "Milano_EV_University_Project/2.0 (junior_dev@mail.com)"
}