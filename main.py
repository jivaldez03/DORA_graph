from app.db.database import driver_close
from app.general_functions import pandas_fn as pd_fns
import app.clean_and_load as cl

# MAIN SECTION

cl.initializing_database()

pdxls = pd_fns._read_file('./files/DORA_Requirements.xlsx') 

for gia, sheet in enumerate(list(pdxls.keys())[0:1]):    
    df = pdxls[sheet]
    cols = df.columns
    df = pd_fns._df_renamecolumns(df
                                , { 'People, Process, Technology' : 'Category'
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

    df["Related_to"] = cl.cleaning_column_related_to(list(df["Related_to"]))
    df["Stipulation"] = df["Stipulation"].str.capitalize()
    
    cl.sendingDB_recordFile(df)
    cl.adding_domain_cat_others()
    cl.adding_articles()
    cl.adding_paragraph()
    cl.adding_point()
    cl.adding_subpoint()
    cl.adding_fulltext()
    cl.adding_fulltext_paragraph()
    cl.adding_fulltext_point()
    cl.adding_related_to_Chapter()
    cl.adding_related_to_Art()
    cl.adding_related_to_Paragraph()
    cl.adding_related_to_Point()
    cl.cleaning_database()

driver_close()
