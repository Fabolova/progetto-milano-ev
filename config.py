import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("⚠️ Manca la stringa MONGO_URI nel file .env!")

# Coordinate del Comune di Milano
MILANO_LAT = 45.4642
MILANO_LON = 9.1900
RADIUS_KM = 8



DB_NAME = "ev_analytics_milano"


HEADERS = {
    "User-Agent": "Milano_EV_University_Project/2.0 (junior_dev@mail.com)"
}