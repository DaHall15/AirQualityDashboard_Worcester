# The following base code was taken based off the following website:
# https://medium.com/@mahyar.aboutalebi/real-time-air-quality-mapping-in-4-easy-steps-python-3e4b7a09e2d3

# Defining the Area of Interest
import requests
url = "https://api.purpleair.com/v1/sensors" # This is the basic url, it will be added to
# Coordinates of Worcester Area - area of interest
nwlng = -71.88621040103936
nwlat = 42.325335608467334
selng = -71.72691479594192
selat = 42.216515499221515

# Querying the fields of the locations of the sensors within the area
querystring = {"fields": "latitude,altitude,longitude",
               "location_type": "0","nwlng": f"{nwlng}", "nwlat": f"{nwlat}", "selng": f"{selng}", "selat": f"{selat}"}

# Setting the header of the request, this is the read API key
headers = { "X-API-Key": "8DF7161D-F2AE-11EE-B9F7-42010A80000D"}
# This uses the requests package to query the sensor requests, combining the url, header and parameters into a single request/query
response = requests.get(url, headers=headers, params=querystring)
# Printing the response to the query
print(response.text)

########################### CREATING A DB FOR SENSORS ##########################

# Importing the necessary packages
import json
import pandas as pd

# Defining 'response_dict' the responses as text into json
response_dict = json.loads(response.text)
response_dict['time_stamp']
# Creating a panda's dataframe
df_sensors = pd.DataFrame(response_dict['data'], columns=response_dict['fields']) # creates dataframe with all listed fields
# Adding time stamp to the data frame
response_dict['data']
df_sensors['time_stamp'] = response_dict['time_stamp']
# Printing the output of the dataframe
df_sensors # There are four total air quality sensors in Worcester from PurpleAir!
# Then add convert to csv...?
df_sensors.to_csv('sensors.csv', index=False)

####################### CREATING A DB FOR Air Quality Readings ##########################
# Downloading the Real-time air quality reaadings from sensors

import requests
from io import StringIO
# URL to pull the data
url = f"https://api.purpleair.com/v1/sensors"
# Coordinates of Worcester Area
nwlng = -71.88621040103936
nwlat = 42.325335608467334
selng = -71.72691479594192
selat = 42.216515499221515

# Setting the header of the request - again we have the READ API key
headers = { "X-API-Key": "8DF7161D-F2AE-11EE-B9F7-42010A80000D"}
#
# Setting the parameters to get
params = {
    "fields": "pm2.5_60minute", # The parameters queried are PM2.5 for 60 minute
    "location_type": "0",# changed to fields_aq to distinguish between params
    "nwlng": f"{nwlng}",
    "nwlat": f"{nwlat}",
    "selng": f"{selng}",
    "selat": f"{selat}"
}


response = requests.get(url, headers=headers, params=params) # combines the parts into one query
# Importing from JSON to dataframe
import json
import io

data =  json.load(io.BytesIO(response.content)) 
df_aq = pd.DataFrame(data['data'], columns=data['fields']) # puts the response into a dataframe
# Printing the dataframe
df_aq

# Normalization Steps
# - Add timestamp
# - Add sensor name

# Save the dataframe in a CSV                ### EXPORTING DATAFRAME OF ACTUAL AIRQUALITY READINGS ###
df_aq.to_csv('data.csv', index=False)
df_aq

################################# Joining the Dataframes ###########################################
import json
import io
data =  json.load(io.BytesIO(response.content))
df_all = pd.DataFrame(data['data'], columns=data['fields'])

import pandas as pd
df1 = pd.read_csv('sensors.csv')
df2 = pd.read_csv('data.csv')

merged_df = pd.merge(df1, df2, on='sensor_index')
merged_df.to_csv('sensors_data.csv', index=False)
merged_df

############################# Converting PurpleAir Raw PM2.5 to AQI Measurements

## Code Sourced from https://community.purpleair.com/t/how-to-calculate-the-us-epa-pm2-5-aqi/877/11

# Defining the "calcAQI" function that is the actual AQI conversion, considers 
    # Conci = Input concentration for a given pollutant
    # ConcLo = The concentration breakpoint that is less than or equal to Conci
    # ConcHi = The concentration breakpoint that is greater than or equal to Conci
    # AQILo = The AQI value/breakpoint corresponding to ConcLo
    # AQIHi = The AQI value/breakpoint corresponding to ConcHi
    # These variables are in the AQI lo and AQI hi values listed within the aqiFromPM function
def calcAQI(Cp, Ih, Il, BPh, BPl):
    a = (Ih - Il)
    b = (BPh - BPl)
    c = (Cp - BPl)
    return round((a / b) * c + Il)

# Defining the "aqiFromAPI" function which converts raw Pm2.5 observations
    # that are reported from the purple air API into AQI values. AQI values are needed because they are 
    # the reported values that website viewers see and understand on EPA and other interactive AQ dashboards.
    # Basically they are more intuitive.
def aqiFromPM(pm):
    if not float(pm):
        return "0"
    if pm == 'undefined':
        return "-"
    if pm < 0:
        return pm
    if pm > 1000:
        return "-"
    
    # Edited by D.Hall - Updated to updated AQI Equation (valid beginning may 6 2024)
        #https://forum.airnowtech.org/t/the-aqi-equation-2024-valid-beginning-may-6th-2024/453
    
            # PM2.5 24-Hour 
    ##                            AQI lo - AQI hi| RAW PM2.5    
    ## Good                               0 - 50 | 0.0 – 9.0    
    ## Moderate                         51 - 100 | 9.1 – 35.4
    ## Unhealthy for Sensitive Groups  101 – 150 | 35.5 – 55.4
    ## Unhealthy                       151 – 200 | 55.5 – 125.4
    ## Very Unhealthy                  201 – 300 | 125.5 – 225.4
    ## Hazardous                       301 – 500 | 225.5 – 325.4
    if pm > 225.5:
        return calcAQI(pm, 400, 301, 325.4, 225.5)  # Hazardous
    elif pm > 125.5:
        return calcAQI(pm, 300, 201, 225.4, 125.5)  # Very Unhealthy
    elif pm > 55.5:
        return calcAQI(pm, 200, 151, 125.4, 55.5)  # Unhealthy
    elif pm > 35.5:
        return calcAQI(pm, 150, 101, 55.4, 35.5)  # Unhealthy for Sensitive Groups
    elif pm > 9.1:
        return calcAQI(pm, 100, 51, 35.4, 9.1)  # Moderate
    elif pm >= 0:
        return calcAQI(pm, 50, 0, 9, 0)  # Good
    else:
        return 'undefined'

# Convert US AQI from raw pm2.5 data (in the pm2.5_60minute column of the df_aq dataframe)
## Aplying this function to the pm2.5_60minute column in the df_aq dataframe
merged_df["pm2.5_60minute"] = merged_df["pm2.5_60minute"].apply(aqiFromPM)
merged_df["pm2.5_60minute"]

###### Converting the TimeStamp to Date and Time 
    # Supporting code: https://www.influxdata.com/blog/how-convert-timestamp-to-datetime-in-python/#:~:text=Converting%20Timestamp%20to%20Datetime%20in%20Python%201%20Import,manipulate%20the%20converted%20datetime%20object%20as%20needed.%20
import time
from datetime import datetime
import pytz

# Defining the time zone to convert to as well
merged_df['daytime'] = pd.to_datetime(merged_df["time_stamp"], unit = 's').dt.tz_localize('UTC').dt.tz_convert('America/New_York') # This is in UTC time zone 
merged_df['DateTime'] = merged_df['daytime'].dt.strftime("%Y-%m-%d %I:%M%p") # converting to date as year-month-date hour/AM/PM
 
#merged_df['DateTime']
#merged_df['DateOb'] = [d.date() for d in merged_df ['DateTime']]
#merged_df['TimeOb'] = [d.time() for d in merged_df ['DateTime']]

# Need to split the daytime column into two
# Creating a 'Day'column from the 'daytime' column and the same called 'Time'
#merged_df['DateObserved'] = [d.date() for d in merged_df ['daytime']]
#merged_df['TimeObserved'] = [d.time() for d in merged_df ['daytime']]

merged_df[['Date','Time']] = merged_df['DateTime'].str.split(" ", expand = True) # Splitting DayTime into two columns; Day and Time
merged_df

# Convert time UTC to hours 


###################### Normalizing the Data Frame ###############################33

# Dropping Unnecessary columns
merged_df_norm = merged_df.drop(['altitude', 'daytime', 'DateTime', 'time_stamp'], axis =1)
merged_df_norm

# Add sensor name based on PurpleAir Sensor info
sensor_id_purpleair = ['Mass. DEP PurpleAir', 'Forest Grove', 'Batters Eye Polar Park', 'Batters Eye 2']
merged_df_norm.loc[:,"SensorName"]= sensor_id_purpleair
merged_df_norm
print(merged_df_norm)

# Changing the order of the columns
purpleair_order = merged_df_norm.iloc[:,[6,3,4,5,1,2,0]] ## Need to reorder based on new column
purpleair_order

# Changing the name of the columns to be the same as AirNOW
purpleair_order.rename(columns={'latitude':'Latitude', 'longitude':'Longitude', 'sensor_index':'Sensor_Index', 'pm2.5_60minute':'PM2.5_1hourAve', 'Date':'DateObserved', 'Time':'TimeObserved'}, inplace = True)
purpleair_order


## Exporting the CSV
filepath_purpleair = "/Data_CSVs/PurpleAir_data_1.csv"
purpleair_order.to_csv(filepath_purpleair)


