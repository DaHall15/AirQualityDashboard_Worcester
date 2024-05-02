# Worcester Air Quality Project

Danielle Hall
Spatial Databases

## Project Objectives
- Develop a web-based dashboard that displays live air quality (Particulate Matter 2.5) readings from all public air quality sensors in the town of Worcester.  

- Utilize all current air quality monitors and their live data readings.  

- Create a readable and easily accessible web-based dashboard, it is hoped that residents will have a better understanding of their local air quality.  

- APIs will be used to query live data from PurpleAir and AirNOW 

- A python script will be developed to read the data into pandas data frames 

- The mapping platform chosen for this will be ArcGIS Online.

## Background
- PurpleAir, AirNOW and MassDEP are the three providers of air quality sensors that provide live air quality readings to the public. 
- Particulate Matter 2.5 (PM2.5) are harmful particulates in the air, not visible to the naked eye. 
- With increasing surface air temperatures and the urban heat island effect, it is vital residents of Worcester have a user-friendly web-based dashboard to view live readings of air quality (measured by PM2.5) in their neighborhood.
### Purple Air Interactive Map
<img width="600px" src="Images\purpleair_interactivemap.png" alt="workflow"></img>

### AirNOW Interactive Map 
<img width="600px" src="Images\airnow_interactivemap.png" alt="workflow"></img>
## Proposed Workflow
Follow the proposed workflow in the diagram below. 
<img width="600px" src="Images\workflow_part1.png" alt="workflow"></img>

<img width="600px" src="Images\workflow_part2.png" alt="workflow"></img>

## PurpleAir Script to Read in Data Feed - Step 3
Purple Air live data feed will be read into a dataframe (and eventually a csv) using the example code provided in a 'Medium' article: https://medium.com/@mahyar.aboutalebi/real-time-air-quality-mapping-in-4-easy-steps-python-3e4b7a09e2d3 

The example code was used and adapted for this project in the file named _"PurpleAir_Python_to_Dataframe.py"_ witihn this repo. 

## AirNOW Script to Read in Data Feed - Step 3
AirNOW data live data feed will be read into a dataframe and csv, using the example code from Practical Data Science page: https://practicaldatascience.co.uk/data-science/how-to-read-an-rss-feed-in-python 

Example code was adapted to the use of this project and is called _"AirNOW_RSS_feedtoPython.py"_ in this repo.

## Required packages
Make sure to download the packages required to run this code. Use the "required_packages" text file within this repo for required packages
Run: 
```
pip install -r required packages.txt
```

## CalEnviroScreen Example
The final dashboard devleoped is aimed to emulate the basic structure of the CalEnviroScreen dashboard hosted on ArcGIS online. See the website here: https://experience.arcgis.com/experience/11d2f52282a54ceebcac7428e6184203/page/CalEnviroScreen-4_0/ 

## Data Frame Normalization 
Based on the example code that was adapted for the purposes of extracting PurpleAir and AirNOW sensor readings for Worcester, MA, live AQ sensor readings were output as pandas dataframes. 

# PurpleAir data frame
- The initial PurpleAir pandas data frame output looked like the following:
<img width="600px" src="Images\Purple_airInitial_DF.png" alt="workflow"></img>
- The data frame needs to be normalized and processed in order to have the same schema as the AirNOW data frame. 

Steps to normalization: 
1. Drop altitude column since it is not included in the AirNOW sensor information. 

2. Add sensor names based on PurpleAir interactive map sensor names.

- The resulting data frame looks like the following:
<img width="600px" src="Images\PurpleAir_current_df.png" alt="workflow"></img>


It is important to note the data frame is not yet in its final schema. Although, the data frame is within 1NF. This is because all the cells contain indivisible values. Each column has a unique name. The order of the columns does not impact the data's integrity and each column contains values of a single type. It has not yet been decided of whether keeping the sensor_index column is necessary.


# AirNOW data frame
- The initial AirNOW pandas data frame output looked like the following:
<img width="600px" src="Images\AirNOW_initial_DF.png" alt="workflow"></img>
- The data frame needs to be processed in order to have the same schema as the PurpleAir dataframe.
- The initial resulting dataframe is not in 1NF because some of the columns rely on each other (reporting area and state code). Although, these dependent columns will be dropped since they are not needed and they are not contained within the PurpleAir dataframe.
- Therefore, the following steps were taken to make the data frames for PurpleAir and AirNOW the same and to normalize both data frames. 

Steps to making the data frame similar to PurpleAir:

1. Drop columns that report airquality parameters that are not PM2.5. (parameters that are O3 and PM10)
- Transpose data frame
- Drop first and last column in dataframe

2. Drop columns of Local Time Zone, Reporting Area, State, Parameter Name, CategoryName, Category Number. These columns did not provide any necessary information about the AQ reading and were not columns in the PurpleAir data frame, so they were dropped.

3. Add sensor name as column and fill in value

- Resulting data frame looks like the following:

<img width="600px" src="Images\AirNOW_current_df.png" alt="workflow"></img>

Similar to the PurpleAir dataframe - it is important to note the data frame is not yet in its final schema. Although, the data frame is now almost within 1NF. This is because all the cells contain indivisible values. Each column has a unique name. The order of the columns does not impact the data's integrity and each column contains values of a single type. 
The data frame is not yet in 1NF. This is because the HourObserved is dependent on DateObserved. The columns of hour observed and date observed still need to be concatenated or merged somehow, but since PurpleAir time stamp is in a different format (its in time stamp form and AirNOW is in hour and date form), it hasn't been decided what the best option to do this is. 


## Next Steps in Data Normalization and Output File for Visualization
- The final steps of normalization above will depend on the file format that is required to visualize the air quality sensors while _still_ getting live sensor readings. 
- I am considering exporting the pandas data frames into CSV files, though this example https://github.com/bastienwirtz/aqi_watcher/blob/master/grafana-aqi-dashboard.json includes a json file that will symboloze and classifies the PM2.5 readings. 
- It is still desired to host this on ArcGIS Online, like CalEnviro Screen but I am still trying to figure out the connection between making sure the API is pulled from regualarly, making the code accessible, and making it so that the PM2.5 values are visualized properly on ArcGIS Online!


- The pandas dataframes created from reading in, processing and normalizing the AirNOW and PurpleAir API data feeds, were output as _.csv_ files. The .csv files called "AirNOW_data.csv" and "PurpleAir_data.csv" within the PurpleAir folder of the repo are the output files. 

- After setting an output filepath, the output csvs are then read into a Pthyon script _AirQualityMap_visualize.html_ which is ultimately used to merge the AirNOW and PurpleAir dataframes, and then create a leaflet map that will plot live airquality points. The output leaflet map is written as an html file. 

- The resulting html file that hosts the webmap locally is called _WorcesterAirQualityMap.html_. The initial result looks like the following: 


<img width="600px" src="Images\initial_webmaphtml.png" alt="workflow"></img>

## Package installation notes
The list of required_packages in the text file list all packages that need to be installed

Requests is a package that needs to be installed, so is pandas

The package of pandas we've been trying to install is 1.31, when i need 2.2.2..?

io is just a pandas module (io==4.7.5
)

html - need a version that imports the correct modules/package? that the script references but is also inline with the version of Pandas we use. (html5lib==1.1)

Do I even need the lxml since I didnt read in an lxml/rss doc for airnow? (lxml==5.2.1
lxml[html_clean]==0.1.1)

folium is a package definietely needed - it's not a module right?
(folium==v0.16.0)

pandas-geojson- is this a module or a package?

pip list command within project directory to get list of all versions of packages

---------------------
After going through, realized that some of the packages were just not in the correct versions
This is the updated list
requests==2.31.0
pandas==2.2.2
folium==0.16.0
pandas-geojson==2.1.0
requests-html==0.10.0

... is there a way to list the most updated versions within the required_packages without calling the specific versions?