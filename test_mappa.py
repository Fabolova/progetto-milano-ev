from pathlib import Path
import geopandas as gpd

# 1. Ricaviamo la cartella in cui si trova questo script
BASE_DIR = Path(__file__).parent

# 2. Puntiamo alla sottocartella 'data'
DATA_DIR = BASE_DIR / "data"

file_quartieri = DATA_DIR / "quartieri_nil.geojson"
file_colonnine = DATA_DIR / "ricarica_colonnine.geojson"

# Caricamento dei dataset geografici
print("⏳ Caricamento dati in corso...")
quartieri_gdf = gpd.read_file(file_quartieri)
colonnine_gdf = gpd.read_file(file_colonnine)

print("🗺️ CRS Quartieri:", quartieri_gdf.crs)
print("📍 CRS Colonnine:", colonnine_gdf.crs)