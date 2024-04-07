from app.general_functions.common import _get_datetime, _get_sdatetime
from app.general_functions import pandas_fn as pd_fns
from app.db import common_dbfunc as dbexec

#from app.db.crud.NIST_file import control, control_enhancement
from app.db.crud.DORA_load import record_file
from app.db.database import driver_forneo4j

from json import loads, dumps 

print(_get_datetime())
print(_get_sdatetime())

port = input (f"port to connect Neo4j (7687): ")
if not port:
    port = '7687'

targetdb = driver_forneo4j(port)

print(f"Driver to db: {targetdb}")


def sendingDB_recordFile(df):
    global targetdb

    print("Loading records: ")
    #
    properties = ', '.join('{0}: ${0}'.format(n.lower()) for n in list(df.columns))    
    # properties: Supported_on: $Supported_on, Domain: $Domain, Article_Heading: $Article_Heading 

    for index_df, row in df.iterrows():
        query = record_file.create_dora_record_file.format(properties=properties) 

        datarecord = record_file.DataRecord.from_row(row)   # convert a row to a class
        #dict_rec = loads(dumps(datarecord.__dict__))       
        dict_rec = datarecord.__dict__     # convert the class in a json structure # convert the class in a json structure
        
        print(f"{index_df}: {datarecord.supported_on} -> {datarecord.domain}")        
        dbexec.execute_write_query(targetdb, query, **dict_rec)

    return

# MAIN SECTION
pdxls = pd_fns._read_file('files/DORA_Requirements.xlsx') 
print("sheets: ", pdxls.keys())
for gia, sheet in enumerate(list(pdxls.keys())[0:1]):    
    df = pdxls[sheet]
    cols = df.columns
    print(f"\nsheet: {sheet}\ncols: {cols}")
    df = pd_fns._df_renamecolumns(df
                                , { 'People, Process, Technology' : 'Supported_on'
                                    , 'Chapter Heading': 'Domain'
                                    , 'Article Heading' : 'Article_Heading'   
                                    , 'Section Heading' : 'Section_Heading'    
                                    , 'Sub-Point' : 'Sub_Point'
                                    , 'Related to' : 'Related_to'
                                    , 'Full Text' : 'Full_Text'
                                }
    )
    df = pd_fns._df_NaNbyAny(df, changeto=None)
    df = pd_fns._df_changetype(df, 'Chapter', 'int')
    #df = pd_fns._df_changetype(df, 'Section', 'int')
    df = pd_fns._df_changetype(df, 'Article', 'int')
    #df = pd_fns._df_changetype(df, 'Paragraph', 'int')
    #df = pd_fns._df_changetype(df, 'Sub_Point', 'int')

    sendingDB_recordFile(df)



#adding_relatedcontrols()
#adding_rootnodes()

targetdb.close()