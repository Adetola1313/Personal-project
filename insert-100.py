import pandas as pd

import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def generate_sql_file(filename,df):
    with open(f"{filename}",'w') as file:
        for row in df[:100].iterrows():

            row = row[1]
            reading_insert = f"""INSERT INTO reading (dateTime, stationId, NOx, NO2, NO, PM10, NVPM10, VPM10, NVPM2_5, PM2_5, VPM2_5, CO, O3, SO2, temperature, RH, airPressure, instrumentType,dateStart,dateEnd)
            VALUES ('{row['Date Time']}', {row['SiteID']}, {row['NOx']}, {row['NO2']}, {row['NO']}, {row['PM10']}, {row['NVPM10']}, {row['VPM10']}, {row['NVPM2.5']}, {row['PM2.5']}, {row['VPM2.5']}, {row['CO']}, {row['O3']}, {row['SO2']}, {row['Temperature']}, {row['RH']}, {row['Air Pressure']}, '{row['Instrument Type']}','{row['DateStart']}','{row['DateEnd']}')""".replace('nan','NULL')
            file.write(f"{reading_insert};\n")


logging.info('reading the data in')
df = pd.read_csv('clean.csv',low_memory=False)

logging.info('generating sql file')
generate_sql_file('insert-100.sql',df)
logging.info('Done')