from typing import List
from pydantic_settings import BaseSettings

# for all neo4j database
class DBSettings_any(BaseSettings):
    NEO4J_PROTOCOL: str = "neo4j"
    NEO4J_HOST: str = "localhost"
    NEO4J_PORT: str = "7687"
    NEO4J_USERNAME: str = ""
    NEO4J_PASSWORD: str = ""

    def get_database_uri(self) -> str:
        return f"{self.NEO4J_PROTOCOL}://{self.NEO4J_HOST}:{self.NEO4J_PORT}"


    def get_database_uri_port(self,port) -> str:
        return f"{self.NEO4J_PROTOCOL}://{self.NEO4J_HOST}:{port}"


class Settings_any(BaseSettings):
    APP_NAME: str = "json -> neo4j"
    API_V1_PATH: str = ""
    db: DBSettings_any = DBSettings_any()

settings_any = Settings_any()

print(f"settings_an: {settings_any}")