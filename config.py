import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not MONGO_URI:
    raise ValueError("⚠️ Manca la stringa MONGO_URI nel file .env!")
if not NEO4J_PASSWORD:
    raise ValueError("⚠️ Manca la stringa NEO4J_PASSWORD nel file .env!")

# Coordinate del Comune di Milano
MILANO_LAT = 45.4642
MILANO_LON = 9.1900
RADIUS_KM = 8



DB_NAME = "ev_analytics_milano"


HEADERS = {
    "User-Agent": "Milano_EV_University_Project/2.0 (junior_dev@mail.com)"
}