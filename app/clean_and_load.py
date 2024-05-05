from app.db import common_dbfunc as dbexec
from app.db.database import targetdb
from app.db.crud import doras_load_file
from app.model import record_file as model_dora
import re

def initializing_database():
    query = doras_load_file.initializing_database
    dbexec.execute_write_query(targetdb, query)

def cleaning_false_sub_point():
    query = doras_load_file.false_spt_fulltext
    dbexec.execute_write_query(targetdb, query)

def cleaning_false_point():    
    query = doras_load_file.false_pt_fulltext
    dbexec.execute_write_query(targetdb, query)

def cleaning_false_paragraph():
    query = doras_load_file.false_par_fulltext
    dbexec.execute_write_query(targetdb, query)

def cleaning_database():
    query = doras_load_file.record_file_delete
    dbexec.execute_write_query(targetdb, query)

    cleaning_false_sub_point()
    cleaning_false_point()
    cleaning_false_paragraph()

def cleaning_column_related_to(l:list):
    # converting: "Article 6(8)]" -> ['6;8;'] -> ' Article 6, Paragraph 8
    # converting: "Article 11(1); Article 11(3)" -> ['11;1;', '11;3;']
    # converting: "Article 30(2) point (i)" -> ['30;2;i;']
    newlist = []
    for element in l:
        if element:
            element2 = re.sub(r"[;]", "/", element) 
            element2 = re.sub(r"[()]", ";", element2) 
            element2 = re.sub(r"[, ]", "", element2) 
            element2 = element2.replace('Article','').replace('point','').replace(';;',';')
            element2 = element2.split('/')
            for pos,el in enumerate(element2):
                #if el.__contains__('Chapter'):
                #    continue
                if el.count(';') == 0: # or el.__contains__('Chapter'):
                    el += ';;'
                elif el.count(';') == 1:
                    el += ';'
                element2[pos] = el            
            newlist.append(element2)
        else:
            newlist.append(None)
    return newlist

def sendingDB_recordFile(df):
    global targetdb

    print("Loading records...")
    properties = ', '.join('{0}: ${0}'.format(n.lower()) for n in list(df.columns))
    # properties: Supported_on: $Supported_on, Domain: $Domain, Article_Heading: $Article_Heading 

    for index_df, row in df.iterrows():
        query = doras_load_file.create_dora_record_file.format(properties=properties) 

        datarecord = model_dora.DataRecord.from_row(row) # convert a row to a class

        dict_rec = datarecord.__dict__     # convert the class in a json structure         
        dbexec.execute_write_query(targetdb, query, **dict_rec)
    return

def adding_domain_cat_others():
    print('Adding Domains, categories and other data master...')
    query = doras_load_file.domain_cat_other
    dbexec.execute_write_query(targetdb, query)

def adding_articles():
    print('Adding Articles...')
    query = doras_load_file.articles
    dbexec.execute_write_query(targetdb, query)

def adding_paragraph():
    print('Adding Paragraph...')
    query = doras_load_file.paragraph
    dbexec.execute_write_query(targetdb, query)

def adding_point():
    print('Adding Point...')
    query = doras_load_file.point
    dbexec.execute_write_query(targetdb, query)

def adding_subpoint():
    print('Adding Subpoint...')
    query = doras_load_file.sub_point
    dbexec.execute_write_query(targetdb, query)

def adding_fulltext():
    print('Adding Fulltext...')
    query = doras_load_file.fulltext
    dbexec.execute_write_query(targetdb, query)

def adding_fulltext_paragraph():
    print('Adding Paragraph_Fulltext...')
    query = doras_load_file.paragraph_fulltext
    dbexec.execute_write_query(targetdb, query)

def adding_fulltext_point():
    print('Adding Point_Fulltext...')
    query = doras_load_file.point_fulltext
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Chapter():
    print('Adding Related to...', end="")
    query = doras_load_file.related_to_Chapter
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Art():
    print('......', end="")
    query = doras_load_file.related_to_Article
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Paragraph():
    print('......', end="")
    query = doras_load_file.related_to_Paragraph
    dbexec.execute_write_query(targetdb, query)

def adding_related_to_Point():
    print('......')
    query = doras_load_file.related_to_Point
    dbexec.execute_write_query(targetdb, query)
