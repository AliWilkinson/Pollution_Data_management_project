import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np


# connect to local host and create database
def connect_localhost(host, user, password):
    try:
        mySQL_connection = mysql.connector.connect(
             host=host,
             user=user,
             passwd=password,
        ) 
        cursor = mySQL_connection.cursor()
        cursor.execute("""CREATE SCHEMA IF NOT EXISTS `pollution-db2` DEFAULT CHARACTER SET utf8 ;
    USE `pollution-db2` ;""")
        
        cursor.close()
        mySQL_connection.close()

        print('Connection successful, database created.')
    except Error as e:
        print(f"The error '{e}' occurred")
    
    
    # connect to pollution-db2 and create tables


def connect_database(host, user, password, db):
     try:
         connection = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=db
        )
         print('Connection successful')
         return connection
     except Error as e:
         print(f"The error '{e}' occurred")




def connect_pollution_db2(connection):
        
    try:
    # create site table    
        cursor = connection.cursor()
        create_site_table = """CREATE TABLE IF NOT EXISTS `pollution-db2`.`Site` (
    `Site_ID` INT NOT NULL,
    `Location` VARCHAR(50) NULL,
    `Geo_Point_2d` VARCHAR(50) NULL,
    PRIMARY KEY (`Site_ID`),
    UNIQUE INDEX `Site_ID_UNIQUE` (`Site_ID` ASC))
  ENGINE = InnoDB;"""
        cursor.execute(create_site_table)
        connection.commit()

    # create readings table 

        create_readings_table = """CREATE TABLE IF NOT EXISTS `pollution-db2`.`Readings` (
  `Reading_ID` INT NOT NULL AUTO_INCREMENT,
  `Site_ID` INT NOT NULL,
  `Date_Time` DATETIME NULL,
  `NOx` FLOAT NULL,
  `NO2` FLOAT NULL,
  `NO` FLOAT NULL,
  `PM10` FLOAT NULL,
  `NVPM10` FLOAT NULL,
  `VPM10` FLOAT NULL,
  `NVPM2.5` FLOAT NULL,
  `PM2.5` FLOAT NULL,
  `VPM2.5` FLOAT NULL,
  `CO` FLOAT NULL,
  `O3` FLOAT NULL,
  `SO2` FLOAT NULL,
  `Temperature` REAL NULL,
  `Relative_Humidity` FLOAT NULL,
  `Air_Pressure` FLOAT NULL,
  `Date_Start` DATETIME NULL,
  `Date_End` DATETIME NULL,
  `Current` TINYINT NULL,
  `Instrument_Type` VARCHAR(45) NULL,
  PRIMARY KEY (`Reading_ID`),
  UNIQUE INDEX `Reading_ID_UNIQUE` (`Reading_ID` ASC),
  INDEX `fk_Readings_Site_idx` (`Site_ID` ASC))
ENGINE = InnoDB;"""
        cursor.execute(create_readings_table)
        connection.commit()
 
    # create schema table 

        create_schema_table = """CREATE TABLE IF NOT EXISTS `pollution-db2`.`Schema` (
  `Measure` VARCHAR(20) NOT NULL,
  `Description` VARCHAR(35) NULL,
  `Unit` VARCHAR(10) NULL,
  PRIMARY KEY (`Measure`))
ENGINE = InnoDB;"""
        cursor.execute(create_schema_table)
        connection.commit()

        cursor.close()
        

        print('Connection successful, tables created.')
    except Error as e:
        print(f"The error '{e}' occurred")



# populate db with data from csv
# function to populate site and schema tables

def populate_site_schema(connection):
    try:
        cursor = connection.cursor()

        # read in csv and save to pandas df
        pollution_df = pd.read_csv('clean.csv', sep=';')
        pollution_df.replace(to_replace=np.nan, value=None, inplace=True)

        # itterate over pollution_df and insert specific data from each row into Site table
        insert_site = """
        INSERT INTO Site (Site_ID, Location, Geo_Point_2d)
        VALUES (%s, %s, %s)"""

        unique_sites = pollution_df.drop_duplicates(subset='SiteID', inplace=False)
    
        # DONT WANT TO PUT ALL DATA FROM SITE ID ETC. - ONLY ONE SITE ID = 1 LOCATION = 1 GP

        siteID = unique_sites.SiteID
        location = unique_sites.Location
        geo_point = unique_sites.geo_point_2d
        site_data = list(zip(siteID, location, geo_point))
    

        cursor.executemany(insert_site, site_data)


        insert_schema = """
        INSERT INTO `Schema` (Measure, Description, Unit) 
        VALUES (%s, %s, %s)"""

        measure = ['Date Time', 'NOx', 'NO2', 'NO', 'SiteID', 'PM10', 'NVPM10', 'VPM10', 'NVPM2.5', 'PM2.5', 'VPM2.5', 'CO', 'O3', 'SO2', 'Temperature', 'RH', 'Air Pressure', 'Location', 'geo_point_2d', 'DateStart', 'DateEnd', 'Current', 'Instrument Type']
        desc = ['Date and time of measurement', 'Concentration of oxides of nitrogen', 'Concentration of nitrogen dioxide', 'Concentration of nitric oxide', 'Site ID for the station', 'Concentration of particulate matter <10 micron diameter', 'Concentration of non - volatile particulate matter <10 micron diameter', 'Concentration of volatile particulate matter <10 micron diameter', 'Concentration of non volatile particulate matter <2.5 micron diameter', 'Concentration of particulate matter <2.5 micron diameter', 
                'Concentration of volatile particulate matter <2.5 micron diameter', 'Concentration of carbon monoxide', 'Concentration of ozone', 'Concentration of sulphur dioxide', 'Air temperature', 'Relative Humidity', 'Air Pressure', 'Text description of location', 'Latitude and longitude', 'The date monitoring started', 'The date monitoring ended', 'Is the monitor currently operating', 'Classification of the instrument']
        unit = ['datetime', '㎍/m3', '㎍/m3', '㎍/m3', 'integer', '㎍/m3', '㎍/m3', '㎍/m3','㎍/m3', '㎍/m3', '㎍/m3', '㎎/m3', '㎍/m3', '㎍/m3', '°C', '%', 'mbar', 'text', 'geo point', 'datetime', 'datetime', 'text', 'text']

        schema_data = list(zip(measure, desc, unit))

        cursor.executemany(insert_schema, schema_data)
        cursor.fetchall()  
        connection.commit()
        cursor.close()
        

        print('Site and Schema populated')
    except Error as e:
        print(f"The error '{e}' occurred")


# function to populate readings table and close the connection

def populate_readings(connection):

    try:
        cursor = connection.cursor()

        insert_readings = """
        INSERT INTO Readings (`Site_ID`, `Date_Time`, `NOx`, `NO2`, `NO`, `PM10`,
        `NVPM10`, `VPM10`, `NVPM2.5`, `PM2.5`, `VPM2.5`, `CO`, `O3`, `SO2`, `Temperature`,
        `Relative_Humidity`, `Air_Pressure`, `Date_Start`, `Date_End`, `Current`, `Instrument_Type`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""   

# chunk the readings data
        chunk_size = 3457
        

        for chunk in pd.read_csv('clean.csv', sep=';', chunksize=chunk_size, iterator=True):

            chunk.replace(to_replace=np.nan, value=None, inplace=True)


            site_id = chunk.SiteID
            dat_tim = chunk['Date Time']
            nox = chunk.NOx
            no2 = chunk.NO2
            no = chunk.NO
            pm10 = chunk.PM10
            nvpm10 = chunk.NVPM10
            vpm10 = chunk.VPM10
            nvpm25 = chunk['NVPM2.5']
            pm25 = chunk['PM2.5']
            vpm25 = chunk['VPM2.5'] 
            co = chunk.CO
            o3 = chunk.O3
            so2 = chunk.SO2
            temp = chunk.Temperature
            rh = chunk.RH
            ap = chunk['Air Pressure']
            ds = chunk.DateStart 
            de = chunk.DateEnd 
            current = chunk.Current
            it = chunk['Instrument Type']

            readings_data = list(zip(site_id, dat_tim, nox, no2, no, pm10, nvpm10, vpm10, nvpm25, pm25, vpm25, co, o3, so2, temp, rh, ap, ds, de, current, it))    
            cursor.executemany(insert_readings, readings_data)
            connection.commit()
               
            
        cursor.close()
        connection.close()

        print('Readings populated')
    except Error as e:
        print(f"The error '{e}' occurred")


connect_localhost('localhost', 'root', None)  

db_connection = connect_database('localhost', 'root', None, 'pollution-db2')
 
connect_pollution_db2(db_connection) 
populate_site_schema(db_connection) 
populate_readings(db_connection)




   

        

    





    

