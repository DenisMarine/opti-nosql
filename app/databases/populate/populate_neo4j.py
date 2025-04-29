from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Suppression de la base
try:
    driver.flushdb()
    print("Base Redis vidée avec succès.")
except Exception as e:
    print(f"Erreur lors du vidage de la base Redis : {e}")

# Fonction pour créer des nœuds 'City'
def create_city(tx, code, name, country):
    query = "CREATE (c:City {code: $code, name: $name, country: $country})"
    tx.run(query, code=code, name=name, country=country)

# Fonction pour créer une relation 'NEAR' entre deux villes
def create_near_relation(tx, city_code1, city_code2, weight):
    query = """
        MATCH (c1:City {code: $city_code1}), (c2:City {code: $city_code2})
        CREATE (c1)-[:NEAR {weight: $weight}]->(c2)
        """
    tx.run(query, city_code1=city_code1, city_code2=city_code2, weight=weight)

def populate_graph():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            create_city(tx, "PAR", "Paris", "FR")
            create_city(tx, "LON", "London", "GB")
            create_city(tx, "BER", "Berlin", "DE")
            create_city(tx, "NYC", "New York", "US")
        
        with session.begin_transaction() as tx:
            create_near_relation(tx, "PAR", "LON", 0.8)
            create_near_relation(tx, "LON", "BER", 0.7)
            create_near_relation(tx, "BER", "NYC", 0.6)
            create_near_relation(tx, "PAR", "NYC", 0.9)

populate_graph()
driver.close()

print("Base de données peuplée avec succès!")