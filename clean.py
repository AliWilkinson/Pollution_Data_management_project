import pandas as pd

try:
    pollution_df = pd.read_csv('crop.csv', sep=';')

    # drop missing data in siteID column from dataframe
    pollution_df = pollution_df.dropna(subset=['SiteID'])


    monitors = {
    188: 'AURN Bristol Centre',
    203: 'Brislington Depot',
    206: 'Rupert Street',
    209: 'IKEA M32',
    213: 'Old Market',
    215: 'Parson Street School',
    228: 'Temple Meads Station',
    270: 'Wells Road',
    271: 'Trailer Portway P&R',
    375: 'Newfoundland Road Police Station',
    395: "Shiner's Garage",
    452: 'AURN St Pauls',
    447: 'Bath Road',
    459: 'Cheltenham Road \ Station Road',
    463: 'Fishponds Road',
    481: 'CREATE Centre Roof',
    500: 'Temple Way',
    501: 'Colston Avenue',
    672: 'Marlborough Street'
    }


    # put columns into lists
    site_ID_list = list(pollution_df.SiteID)
    site_location = list(pollution_df.Location)

    # create list of tuples of siteID and location from the data
    ID_location = zip(site_ID_list, site_location)
    ID_location_list = list(ID_location)
    # print(ID_location_list)

    # access keys and values from the monitors dict
    keys = list(monitors.keys())
    vals = list(monitors.values())

    # find missmatching tuples that dont match the key:value pairs in the monitors dictionary
    indices_to_drop = []
    for location in ID_location_list:
        ind = keys.index(location[0])
        if location[1] != vals[ind]:
            indices_to_drop.append(ID_location_list.index(location))
            print('The mismatching site ID and location are: ' + str(location[0]) + ' and ' + str(location[1]) + ' at index ' + str(ID_location_list.index(location)))

    # for the first val in the tuple - find the key in monitors and if the second value != to the equivalent value - add to the list to be dropped

    pollution_df_cropped = pollution_df.drop(labels=indices_to_drop, axis=0, inplace=False)

    pollution_df_cropped.to_csv(path_or_buf='clean.csv', sep=';', index=False)
    print('clean.csv created')
except:
    print('Error')
