# database's execution 
from app.db.database import settings_any

def execute_read_query(query: str, **kwargs):
    driver = settings_any.connection
    with driver.session() as session:
        results = session.execute_read(
                lambda tx: tx.run(query, **kwargs.data())
            )
        return results
    
def execute_write_query(query: str, **kwargs):
    driver = settings_any.connection
    #print(f"query_w: {query} -> params **kwargs: {kwargs} \n")
    with driver.session() as session:
        results = session.execute_write(
                lambda tx: tx.run(query, **kwargs).data()
            )
        return results
