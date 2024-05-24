from app.db.config import settings_any

def driver_open_session():
    port = input (f"port to connect Neo4j (7687): ")
    if not port:
        port = '7687'
    target_db = settings_any.open_driver(port)
    return target_db

def driver_close():
    settings_any.connection.close()
