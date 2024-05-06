from neo4j import GraphDatabase
from app.db.config import settings_any

def driver_forneo4j(port):
    print(f"Connecting: {settings_any.db.get_database_uri_port(port)}")
    driver_neo4j = GraphDatabase.driver(
        settings_any.db.get_database_uri_port(port)
        #, auth=(settings_any.db.NEO4J_USERNAME, settings_any.db.NEO4J_PASSWORD)        
    )
    return driver_neo4j

def driver_open():
    port = input (f"port to connect Neo4j (7687): ")
    if not port:
        port = '7687'
    return driver_forneo4j(port)

def driver_close():
    targetdb.close()

targetdb = driver_open()
