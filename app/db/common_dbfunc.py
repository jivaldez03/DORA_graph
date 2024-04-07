# database's execution 

def execute_read_query(driver, query: str, **kwargs):
    with driver.session() as session:
        results = session.execute_read(
                lambda tx: tx.run(query, **kwargs.data())
            )
        return results
    
def execute_write_query(driver, query: str, **kwargs):
    #print(f"query_w: {query} -> params **kwargs: {kwargs} \n")
    with driver.session() as session:
        results = session.execute_write(
                lambda tx: tx.run(query, **kwargs).data()
            )
        return results

