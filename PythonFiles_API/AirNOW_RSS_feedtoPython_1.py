# R SCript to read in RSS feed to python
# April 04 2024

#https://practicaldatascience.co.uk/data-science/how-to-read-an-rss-feed-in-python
# Importing the packages
import requests # type: ignore # package is used to make HTTP request to server to get data
|import pandas as pd # type: ignore # package used for data storage and manipulation

## Importing XML reader
#import xml.etree.ElementTree as ET #lxml library already installed with packages

from requests_html import HTML # type: ignore # web-scraping library that combines beautiful soup (parsing) and requests
from requests_html import HTMLSession # type: ignore
# installed in command prompt

# Importing os, then setting the directory
import os
os.chdir("C:/Users/danie/OneDrive/Desktop/WorcesterAQ_WebMap")

# Parse the RSS feed contents
    ## Since we already have the URL provided from the AirNOW xml, we'll use that
    ## There is only one AirNOW sensor in Worcester, so we only need one URL
    ## https://feeds.enviroflash.info/rss/realtime/165.xml?id=1C0A8EED-07D2-9932-57E6890437E8E13B

    # First, need to build RSS parser in Python, done through the creation of
        # function called get_feed()
    # get_feed : takes URL of RSS and passes to the get_source() function
        # this will return the original AirNOW RSS XML code of the feed 
        # as an element called 'response'
    # Second, need to create Panda's dataframe in  which to store the parsed data
        # find() function is used to look for the element names within the XML
        # each element found is placed in a dictionary, called 'row'
        # .append is them used to append the 'row' elements to a dataframe 
        # 'df' that comtains all necessary fields


## Example used now https://github.com/NutraSmart/python_aqi/blob/main/python_airnow.ipynb

# API Key from my Clark email: 4a65bec8-f805-4394-89f8-e70e2d64c3b9
import requests
api_key = 'E45E0A74-20C7-4470-B4FD-22046580734E'

# Creating a function -obseravtion- to get the current conditions read from the sensor in Worcester (1)
def observation(zip_code,api_key,file_format='text/csv',dist='25'):
    params={'format':file_format,'zipCode':zip_code,'distance':dist,'API_KEY':api_key}
    url_airnow='https://www.airnowapi.org/aq/observation/zipcode/current/'

    response = requests.get(url_airnow,params)
    return(response.content)

## Importing the necessary packages to create pandas df
import pandas as pd
from io import BytesIO, StringIO

# Creating a dataframe from current conditions
#using the read_csv function from pandas to read the observation csv
    #observation is in format defined above
observation('01608','E45E0A74-20C7-4470-B4FD-22046580734E') # printing the output of the function
column_names  = ['O3','PM2.5','PM10']
current_df=pd.read_csv(BytesIO(observation('01603',api_key='E45E0A74-20C7-4470-B4FD-22046580734E')))

type(current_df)
current_df.T# printing the dataframe

### Data Frame Normalization 
# Dropping rows not reporting PM2.5
pm25_df_1 = current_df.T.iloc[:,:-1]
pm25_df = pm25_df_1.iloc[:,1:]
pm25_df

# Dropping unnecessary columns using drop function
pm25_norm= pm25_df.T.drop(['LocalTimeZone', 'ReportingArea','StateCode', 'CategoryNumber', 'CategoryName', 'ParameterName', 'Latitude', 'Longitude'], axis =1)
pm25_norm

# Adding the coordinates manually because the API feed is wrong
lat = ["42.263877"]
pm25_norm.loc[:,"Latitude"]=lat
pm25_norm

long = ["-71.794781"]
pm25_norm.loc[:,"Longitude"]=long
pm25_norm

# Adding sensor name as column
sensor_id = ["Mass. DEP Summer Street"]
pm25_norm.loc[:,"SensorName"]=sensor_id
pm25_norm

# Adding sensor index as a column
sensor_index = ['250270023']
pm25_norm.loc[:,"Sensor_Index"]=sensor_index
pm25_norm

# Changing the order of the columns
airnow_order = pm25_norm.iloc[:,[5,4,0,1,2,3,6]] # Need to save structure permanentley 
airnow_order


# Renaming the AQI column to be more descriptive
airnow_order.rename(columns={"AQI":"PM2.5_1hourAve", "HourObserved":"TimeObserved"},inplace = True)
airnow_order


## Exporting the CSV
filepath_airnow = "Data_CSVs/AirNOW_data_1.csv"
airnow_order.to_csv(filepath_airnow)










