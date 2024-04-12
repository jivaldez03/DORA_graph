import pandas as pd
import numpy as np

def _read_file(path, sheetname = None):
    df = pd.read_excel(path, sheet_name=sheetname)
    return df


def _df_NaNbyAny(df, changeto=None):
    #df = df.fillna(None)
    df = df.replace(np.nan, changeto)
    return df

def _df_removerows_nulls(df, columns):
    df.dropna(subset=columns, inplace=True)
    return df

def _df_renamecolumn(df, oldcolum='oldcolum',newcolumn='newcolumn'):
    df.rename(columns = {oldcolum:newcolumn}, inplace = True)     
    return df


def _df_renamecolumns(df, colreplacename:dict):  # { oldcolumnname1: newcolname1, oldcolumnname2: newcolname2}    
    df.rename(columns = colreplacename, inplace = True)     
    return df

def _df_changeindex_name(df, oldindex='oldindex',newindex='Index'):
    df[newindex] = df[oldindex]
    df.set_index(newindex, inplace=True)
    df = df.drop(oldindex, axis='columns')
    return df

def _df_changeindex_renumber(df, newindex='Index'):
    df[newindex] = np.arange(df.shape[0])
    df.set_index(newindex, inplace=True)
    return df

def _df_changetype(df, column, new_dtype):    
    df[column] = df[column].astype(new_dtype)
    return df
