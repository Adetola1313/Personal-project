import logging
from typing import Optional

import pandas as pd
import pymysql
from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

host = 'localhost'
user= 'root'
password = ''
db = 'pollution-db2'


file_path = "clean.csv"

#query to create database
create_db_query = """CREATE DATABASE IF NOT EXISTS `pollution-db2`;"""

#query to create station table
create_station_table_query = """
CREATE TABLE IF NOT EXISTS station (
  stationId int NOT NULL,
  geoPoint2d VARCHAR(255),
  location VARCHAR(255),
  PRIMARY KEY (stationId)
);
"""

#query to create reading table
create_reading_table_query = """

CREATE TABLE IF NOT EXISTS reading (
  readingId INT NOT NULL AUTO_INCREMENT,
  dateTime DATETIME NOT NULL,
  stationId INT NOT NULL,
  NOx FLOAT,
  NO2 FLOAT,
  NO FLOAT,
  PM10 FLOAT,
  NVPM10 FLOAT,
  VPM10 FLOAT,
  NVPM2_5 FLOAT,
  PM2_5 FLOAT,
  VPM2_5 FLOAT,
  CO FLOAT,
  O3 FLOAT,
  SO2 FLOAT,
  temperature FLOAT,
  RH FLOAT,
  airPressure FLOAT,
  instrumentType VARCHAR(255),
  PRIMARY KEY (readingId),
  FOREIGN KEY (stationId) REFERENCES station(stationId)
);

""" 

#context manager that gives the option of using pymysql or sqlahemy
class MySQLConnection:
    def __init__(self, host: str, user: str, password: str, db: Optional[str] = None,
                 use_sqlalchemy: bool = False):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.use_sqlalchemy = use_sqlalchemy
        self.conn = None

    def __enter__(self):
        if self.use_sqlalchemy:
            # create a SQLAlchemy engine
            db_uri = f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db}'
            self.conn = create_engine(db_uri)
        else:
            # create a PyMySQL connection
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db
            )
        return self.conn

    def __exit__(self, *args):
        if self.conn is not None:
            if self.use_sqlalchemy:
                # close the SQLAlchemy engine
                self.conn.dispose()
            else:
                # close the PyMySQL connection
                self.conn.close()



def read_input_file(file_path: str) -> pd.DataFrame:
    """
    Read the cleaned CSV file into a Pandas DataFrame.

    Args:
        file_path (str): The path to the cleaned CSV file.

    Returns:
        pandas.DataFrame: The cleaned data.
    """
    return pd.read_csv(file_path,low_memory=False)



def run_sql_query(query: str, db: Optional[str] = None, multi: bool = False, value: list =None) -> None:
    """
    Executes a SQL query on a MySQL database using a context manager.

    Args:
        query (str): The SQL query to execute.
        db (str, optional): The name of the database to connect to. Defaults to None.

    Returns:
        None
    """

    with MySQLConnection(host,user,password,db) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            
def populate_station(df: pd.DataFrame) -> None:
    for row in df.iterrows():
        row = row[1]
        try:
            station_insert = f"""INSERT INTO station (stationId, geoPoint2d, location)
            VALUES ({row['SiteID']}, '{row['geo_point_2d']}', "{row['Location']}")"""
            run_sql_query(station_insert,'pollution-db2')
        except Exception as e:
            print(e)

def populate_data(df: pd.DataFrame) -> None:
    df_insert = data[['Date Time', 'SiteID', 'NOx', 'NO2', 'NO', 'PM10', 'NVPM10', 'VPM10', 'NVPM2.5', 'PM2.5', 'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature', 'RH', 'Air Pressure', 'Instrument Type']]
    df_insert.columns = ['dateTime', 'stationId', 'NOx', 'NO2', 'NO', 'PM10', 'NVPM10', 'VPM10', 'NVPM2_5', 'PM2_5', 'VPM2_5', 'CO', 'O3', 'SO2', 'temperature', 'RH', 'airPressure', 'instrumentType']

    with MySQLConnection(host,user,password,db,True) as conn:    
        
        df_insert.to_sql('reading', conn, if_exists='replace', index=False)

    
#run_sql_query(f'drop database `{db}`')

logging.info('Attempting Database Creation')
run_sql_query(create_db_query)

logging.info('Attempting Station Table Creation')
run_sql_query(create_station_table_query,db)

logging.info('Attempting Reading Table Creation')
run_sql_query(create_reading_table_query,db)

logging.info('Reading Input File')
data = read_input_file(file_path)

station = data[['SiteID','geo_point_2d','Location']].drop_duplicates(subset='SiteID')
logging.info(station.shape)

logging.info('Populating Station')
populate_station(station)

logging.info('Populating readings')
populate_data(data)

logging.info('Program Ended')