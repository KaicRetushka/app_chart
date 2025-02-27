import sqlite3
from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import os

def mysql_to_df(execute, host, port, user, password, database):
    try:
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
        try:
            df = pd.read_sql(execute, engine)
        except:
            return {'is_can': False, 'detail': 'Неверный sql запрос'}
        return {'is_can': True, 'df': df}
    except:
        return {'is_can': False, 'detail': 'Неверные данные для подключения'}

def postgres_to_df(execute, host, port, user, password, database):
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        try:
            df = pd.read_sql(execute, connection)
        except:
            return {'is_can': False, 'detail': 'Неверный sql запрос'}
        connection.close()
        return {'is_can': True, 'df': df}
    except:
        return {'is_can': False, 'detail': 'Неверные данные для подключения'}

def file_to_df(path):
    if os.path.splitext(path)[1] == '.csv':
        return pd.read_csv(path)
    return pd.read_excel(path)

def sqlite_to_df(path, execute):
    connection = sqlite3.connect(path)
    try:
        df = pd.read_sql(execute, connection)
        return {'is_can': True, 'df': df}
    except:
        return {'is_can': False, 'detail': 'Неверный sql запрос'}
    connection.close()
    return df