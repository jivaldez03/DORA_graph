from app.general_functions.common import _get_datetime, _get_sdatetime
from app.general_functions import pandas_fn as pd_fns
from app.db import common_dbfunc as dbexec

from app.db.crud.DORA_load import doras_file
from app.model import record_file as model_dora
from app.db.database import driver_forneo4j

#import typing
import re

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
        query = doras_file.create_dora_record_file.format(properties=properties) 

        datarecord = model_dora.DataRecord.from_row(row) # convert a row to a class

        dict_rec = datarecord.__dict__     # convert the class in a json structure 
        
        print(f"{index_df}: {datarecord.supported_on} -> {datarecord.domain}")        
        dbexec.execute_write_query(targetdb, query, **dict_rec)

    return

def clean_related_to(l:list):
    newlist = []
    for element in l:
        if element:
            element2 = re.sub(r"[;]", "/", element) 
            element2 = re.sub(r"[()]", ";", element2) 
            element2 = re.sub(r"[, ]", "", element2) 
            element2 = element2.replace('Article','').replace('point','').replace(';;',';').replace('Chapter','')
            element2 = element2.split('/')
            for pos,el in enumerate(element2):       
                if el.count(';') == 0:
                    el += ';;'
                elif el.count(';') == 1:
                    el += ';'

                element2[pos] = el

            print(f"element: {element} - {element2}")
            newlist.append(element2)
        else:
            newlist.append(None)
    return newlist


def adding_domain_cat_others():
    print('Adding Domains, categories and other data master:')
    query = doras_file.domain_cat_other
    dbexec.execute_write_query(targetdb, query)

def adding_articles():
    print('Adding Articles')
    query = doras_file.articles
    dbexec.execute_write_query(targetdb, query)

def adding_paragraph():
    print('Adding Paragraph')
    query = doras_file.paragraph
    dbexec.execute_write_query(targetdb, query)

def adding_point():
    print('Adding Point')
    query = doras_file.point
    dbexec.execute_write_query(targetdb, query)

def adding_subpoint():
    print('Adding Subpoint')
    query = doras_file.sub_point
    dbexec.execute_write_query(targetdb, query)

def adding_fulltext():
    print('Adding Fulltext')
    query = doras_file.fulltext
    dbexec.execute_write_query(targetdb, query)

def adding_fulltext_paragraph():
    print('Adding Paragraph_Fulltext')
    query = doras_file.paragraph_fulltext
    dbexec.execute_write_query(targetdb, query)

def adding_fulltext_point():
    print('Adding Point_Fulltext')
    query = doras_file.point_fulltext
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Art():
    print('Adding Related to...', end="")
    query = doras_file.related_to_Article
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Paragraph():
    print('Adding Related to...', end="")
    query = doras_file.related_to_Paragraph
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Point():
    print('......')
    query = doras_file.related_to_Point
    dbexec.execute_write_query(targetdb, query)

def cleaning_false_point():    
    query = doras_file.false_pt_fulltext
    dbexec.execute_write_query(targetdb, query)

def cleaning_false_sub_point():
    query = doras_file.false_spt_fulltext
    dbexec.execute_write_query(targetdb, query)


def cleaning_database():
    print("cleaning....")
    query = doras_file.record_file_delete
    dbexec.execute_write_query(targetdb, query)

    cleaning_false_point()
    cleaning_false_sub_point()
    

# MAIN SECTION
pdxls = pd_fns._read_file('files/DORA_Requirements_v2.xlsx') 
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
    df = pd_fns._df_changetype(df, 'Article', 'int')

    df["Related_to"] = clean_related_to(list(df["Related_to"]))
    
    sendingDB_recordFile(df)

    adding_domain_cat_others()
    adding_articles()
    adding_paragraph()
    adding_point()
    adding_subpoint()
    adding_fulltext()
    adding_fulltext_paragraph()
    adding_fulltext_point()
    adding_related_to_Art()
    adding_related_to_Paragraph()
    adding_related_to_Point()
    cleaning_database()

#adding_relatedcontrols()
#adding_rootnodes()

targetdb.close()