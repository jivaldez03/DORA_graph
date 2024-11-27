from pydantic_settings import BaseSettings
from neo4j import GraphDatabase

class DBSettings_any(BaseSettings):
    NEO4J_PROTOCOL: str = "neo4j"
    NEO4J_HOST: str = "localhost"
    NEO4J_PORT: str = "7689"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "sistemas"

    def get_database_uri(self) -> str:
        return f"{self.NEO4J_PROTOCOL}://{self.NEO4J_HOST}:{self.NEO4J_PORT}"


    def get_database_uri_port(self,port) -> str:
        return f"{self.NEO4J_PROTOCOL}://{self.NEO4J_HOST}:{port}"


class Settings_any():
    APP_NAME: str = "DORA -> neo4j"
    API_V1_PATH: str = ""
    db: DBSettings_any = DBSettings_any()

    def open_driver(self, port):
        driver_neo4j = GraphDatabase.driver(
            settings_any.db.get_database_uri_port(port)
            , auth=(settings_any.db.NEO4J_USERNAME, settings_any.db.NEO4J_PASSWORD)        
        )
        self.connection = driver_neo4j
        return driver_neo4j
    
    def close_driver(self):        
        self.connection.close()

settings_any = Settings_any()

print(f"settings_an: {settings_any}")
