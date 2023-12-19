import mysql.connector
from mysql.connector import Error
import json

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


def read_query(connection):
    cursor = connection.cursor()
    query = """SELECT * FROM `readings` WHERE Site_ID = '501';"""
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def write_json(result):

    instance = {
        "site_id": 501,
        "name": "Colston Avenue",
        "geo_point": "51.455269382758324, -2.596648828557916"
    }

    readings = []

    for i in result:
        readings.append({"reading_id": i[0], "date_time": str(i[2]), "NOx": i[3], "NO2": i[4], "NO": i[5],
                               "PM10": i[6], "NVPM10": i[7], "VPM10": i[8], "NVPM2.5": i[9], "PM2.5": i[10],
                               "VPM2.5": i[11], "CO": i[12], "O3": i[13], "SO2": i[14], "temperature": i[15], "Relative_Humidity": i[16],
                                 "Air_Pressure": i[17], "date_start": str(i[18]), "date_end": i[19], "Current": i[20], "Instrument_Type": i[21]})
    
    instance["readings"] = readings 

    json_instance = json.dumps(instance, indent=2)
   
    with open('501.json', 'w') as file:
        file.write(json_instance)
    
          

db_connection = connect_database('localhost', 'root', None, 'pollution-db2')
result = read_query(db_connection)
write_json(result)
