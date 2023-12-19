import pandas as pd

#save first 100 lines of clean to a df
clean_df = pd.read_csv('clean.csv', sep=';', nrows=100)


#write the file
with open('insert-100.sql', 'w') as file:
           for index, row in clean_df.iterrows():
            insert_statement = """INSERT INTO Readings (`Site_ID`, `Date_Time`, `NOx`, `NO2`, `NO`, `PM10`,
        `NVPM10`, `VPM10`, `NVPM2.5`, `PM2.5`, `VPM2.5`, `CO`, `O3`, `SO2`, `Temperature`,
        `Relative_Humidity`, `Air_Pressure`, `Date_Start`, `Date_End`, `Current`, `Instrument_Type`)
        VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n""".format(row.SiteID, row['Date Time'], row.NOx, row.NO2, row.NO, row.PM10, row.NVPM10,
                                                                                                                  row.VPM10, row['NVPM2.5'], row['PM2.5'], row['VPM2.5'], row.CO, row.O3, row.SO2,
                                                                                                                  row.Temperature, row.RH, row['Air Pressure'], row.DateStart, row.DateEnd, row.Current, row['Instrument Type'])
            
            file.writelines(insert_statement) 

 


       

    

