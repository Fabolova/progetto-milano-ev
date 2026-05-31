from neo4j import GraphDatabase
import database
import config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class TransactionsImporter:
    def __init__(self):
        self.driver = GraphDatabase.driver(config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD))
        self.mongo_client = database.get_db_client()
        self.mongo_db = self.mongo_client[config.DB_NAME]

    def close(self):
        self.driver.close()
        self.mongo_client.close()

    def importa_eventi_simulazione(self):
        eventi_mongo = list(self.mongo_db['charging_sessions2.0'].find({}))
        
        if not eventi_mongo:
            logging.error("❌ Nessun evento trovato in MongoDB.")
            return

        logging.info(f"💸 Trovati {len(eventi_mongo)} eventi di simulazione. Avvio iniezione...")

        # Query Cypher con gestione intelligente del Modello Auto
        cypher_query = """
        // 1. Trova la colonnina
        MATCH (c:Colonnina {id_colonnina: $id_colonnina})
        
        // 2. Crea l'Evento
        CREATE (e:Evento {
            id_mongo: $id_mongo,
            tipo: $tipo_evento,
            inizio: $inizio,
            fine: $fine,
            energia_kwh: $kwh,
            ricavo_euro: $euro
        })
        CREATE (c)-[:HA_REGISTRATO]->(e)
        
        // 3. SE esiste il modello auto, crea il nodo ModelloAuto e collegalo
        FOREACH (ignoreMe IN CASE WHEN $modello_auto IS NOT NULL THEN [1] ELSE [] END |
            MERGE (m:ModelloAuto {nome: $modello_auto})
            CREATE (m)-[:COINVOLTO_IN]->(e)
        )
        """

        with self.driver.session() as session:
            for log in eventi_mongo:
                # Estrazione sicura date
                ts_inizio = log.get('timestamp_inizio', {})
                inizio_str = ts_inizio.get('$date') if isinstance(ts_inizio, dict) else str(ts_inizio)
                
                ts_fine = log.get('timestamp_fine', {})
                fine_str = ts_fine.get('$date') if isinstance(ts_fine, dict) else str(ts_fine)

                session.run(cypher_query,
                    id_colonnina=log.get('id_colonnina', ''),
                    id_mongo=str(log.get('_id')),
                    tipo_evento=log.get('tipo_evento', 'SCONOSCIUTO'),
                    inizio=inizio_str,
                    fine=fine_str,
                    kwh=float(log.get('energia_kwh', 0.0)),
                    euro=float(log.get('ricavo_euro', 0.0)),
                    # Passiamo il modello se c'è, altrimenti None
                    modello_auto=log.get('modello_auto') 
                )
                
        logging.info("✅ EVENTI E VEICOLI IMPORTATI CON SUCCESSO!")

if __name__ == "__main__":
    importer = TransactionsImporter()
    try:
        importer.importa_eventi_simulazione()
    finally:
        importer.close()