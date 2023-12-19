import pandas as pd

try:
# read in csv and create df with pandas
    pollution_df = pd.read_csv('air-quality-data-2003-2022.csv', sep=';', dtype={'DateEnd': str})
    # drop rows with no date time
    pollution_df = pollution_df.dropna(subset=['Date Time'])
    # drop rows before 2010
    pollution_df = pollution_df.drop(pollution_df[pollution_df['Date Time'] < '2010-00-00T00:00:00+00:00'].index)
    
    # write to crop.csv 
    pollution_df.to_csv(path_or_buf='crop.csv', sep=';', index=False)

    print('crop successful')
except:
    print('error')




 