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
<img width="600px" src="AirQualityDashboard_Worcester\WebMap_setup\Images\purpleair_interactivemap.png" alt="workflow"></img>

### AirNOW Interactive Map 
<img width="600px" src="WebMap_setup\Images\airnow_interactivemap.png" alt="workflow"></img>
## Proposed Workflow
Follow the proposed workflow in the diagram below. 
<img width="600px" src="WebMap_setup\Images\workflow_part1.png" alt="workflow"></img>

<img width="600px" src="WebMap_setup\Images\workflow_part2.png" alt="workflow"></img>

## PurpleAir Script to Read in Data Feed - Step 3
Purple Air live data feed will be read into a dataframe (and eventually a csv) using the example code provided in a 'Medium' article: https://medium.com/@mahyar.aboutalebi/real-time-air-quality-mapping-in-4-easy-steps-python-3e4b7a09e2d3 

The example code was used and adapted for this project in the file named _"PurpleAir_Python_to_Dataframe.py"_ witihn this repo. 

## AirNOW Script to Read in Data Feed - Step 3
AirNOW data live data feed will be read into a dataframe and csv, using the example code from Practical Data Science page: https://practicaldatascience.co.uk/data-science/how-to-read-an-rss-feed-in-python 

Example code was adapted to the use of this project and is called _"AirNOW_RSS_feedtoPython.py"_ in this repo.

## Required packages
Make sure to download the packages required to run this code. Use the "all_required_packages" text file within this repo for required packages
Run: 
```
pip install -r all_required_packages.txt
```
Packages used in this project include: folium, pandas, requests, padas-geojson, and requests-html


## CalEnviroScreen Example
The final dashboard devleoped is aimed to emulate the basic structure of the CalEnviroScreen dashboard hosted on ArcGIS online. See the website here: https://experience.arcgis.com/experience/11d2f52282a54ceebcac7428e6184203/page/CalEnviroScreen-4_0/ 

## Data Frame Normalization 
Based on the example code that was adapted for the purposes of extracting PurpleAir and AirNOW sensor readings for Worcester, MA, live AQ sensor readings were output as pandas dataframes. 

# PurpleAir data frame
- The initial PurpleAir pandas data frame output looked like the following:
<img width="600px" src="WebMap_setup\Images\Purple_airInitial_DF.png" alt="workflow"></img>
- The data frame only needs to be changed in order for it to have the same schema as the AirNOW data frame. The data is only needed to be in first normal form, which is already in, so there is no need to normalize it. This is because all the cells contain indivisible values. Each column has a unique name. The order of the columns does not impact the data's integrity and each column contains values of a single type.

**Steps to making schemas the same:**
1. Manually add time stamp field 
```
# Defining 'response_dict' the responses as text into json
response_dict = json.loads(response.text)
response_dict['time_stamp']
# Creating a panda's dataframe
df_sensors = pd.DataFrame(response_dict['data'], columns=response_dict['fields']) # creates dataframe with all listed fields
# Adding time stamp to the data frame
response_dict['data']
df_sensors['time_stamp'] = response_dict['time_stamp']
```
2. Convert raw PM 2.5 to Air Quality Index (AQI Value)
- Current PM2.5 readings directly from the API are raw PM2.5 values. Need to convert them to AQI values because they are used widely to communicate air quality levels to the public. 
- This was done by following example code here: https://community.purpleair.com/t/how-to-calculate-the-us-epa-pm2-5-aqi/877/11
- Two functions were defined that converted raw PM2.5 values to AQI values

3. Convert timestamp field value to separate Date of Observation and Time of Observation fields.
4. Drop altitude column since it is not included in the AirNOW sensor information as well as timestamp field. 
5. Add sensor name based on PurpleAir Sensor information:
```
sensor_id_purpleair = ['Mass. DEP PurpleAir', 'Forest Grove', 'Batters Eye Polar Park', 'Batters Eye 2']
merged_df_norm.loc[:,"SensorName"]= sensor_id_purpleair
merged_df_norm
print(merged_df_norm)
```
6. Rename and re-order the columns in the dataframe to desired order


The final PurpleAir data frame looks like the following:
<img width="600px" src="WebMap_setup\Images\Final_PurpleAir.png" alt="workflow"></img>



# AirNOW data frame
- The initial AirNOW pandas data frame output looked like the following:
<img width="600px" src="WebMap_setup\Images\AirNOW_initial_DF.png" alt="workflow"></img>
- The data frame needs to be processed in order to have the same schema as the PurpleAir dataframe.
- The initial resulting dataframe is already in 1NF because some of the columns rely on each other (reporting area and state code). Although, these dependent columns will be dropped since they are not needed and they are not contained within the PurpleAir dataframe.
- Besides those columns, the table only needs to be in 1NF, and no further normalization is needed.

**Steps to making the data frame similar to PurpleAir:**

1. Drop columns that report airquality parameters that are not PM2.5. (parameters that are O3 and PM10)
- Transpose data frame
- Drop first and last column in dataframe

2. Drop columns of Local Time Zone, Reporting Area, State, Parameter Name, CategoryName, Category Number. These columns did not provide any necessary information about the AQ reading and were not columns in the PurpleAir data frame, so they were dropped.

3. Adding the coordinates manually because the API feed coordinates are wrong
```
lat = ["42.263877"]
pm25_norm.loc[:,"Latitude"]=lat
pm25_norm

long = ["-71.794781"]
pm25_norm.loc[:,"Longitude"]=long
pm25_norm
```

3. Add sensor name and sensor ID as columns and fill in their values manually

4. Rename and re-order the columns in the dataframe to have the same schema as PurpleAir. 

- Resulting data frame looks like the following:

<img width="600px" src="WebMap_setup\Images\Final_AirNOW.png" alt="workflow"></img>


##  Web Map Creation using Leaflet in Python
### Writing Output CSVs
 After finalizing the PurpleAir and AirNOW pandas data frame schemas in the python files _AirNOW_RSS_feedtoPuython_1.py_ and _PurpleAir_Python_to_Dataframe_1.py_ the output data frames were saved as CSVs - called _AirNOW_data_1.csv_ and _PurpleAir_data_1.csv_ files in the Data_CSVs folder.

### Creating a Leaflet map and Adding Air Quality Data
The python script _AirQuality_visualize_1_, was adapted from the following code:
- https://ui-libraries.github.io/Web-Mapping-Intro/#using-the-web-console-to-develop-and-debug-maps-with-live-server
- Using colormaps — Folium 0.16.1.dev54+g570f2933 documentation (python-visualization.github.io)

Within this python script, the following packages are used:
- folium: helps develop Leaflet in python
- pandas
- requests 

First, the CSVs were read into script as variables, then concetenated into a single data frame. Using the folium package, a leaflet map was created and a linear color scale was developed and added to the map. 

```
# Create a continuous color ramp
colormap = LinearColormap(colors=['green', 'Yellow','red', '#8F3F97', '#7E001F'], vmin= 0, vmax= 300, index = [50, 100, 150, 200,300])
colormap.caption = "Air Quality Index Value"
# Create a map centered around sensors
worcesteraq_map = folium.Map(location=[42.269769, -71.799490], zoom_start=12)

# Add markers for each sensor with continuous color based on values
for index, row in aqsensors_df.iterrows():
    folium.CircleMarker(location=[row["Latitude"], row["Longitude"]],
                        radius=10,
                        popup=f"{row['PM2.5_1hourAve']}: {row['SensorName']}: {row['TimeObserved']}: {row['DateObserved']}",
                        color=colormap(row['PM2.5_1hourAve']),
                        fill=True,
                        fill_color=colormap(row['PM2.5_1hourAve']),
                        fill_opacity=0.7).add_to(worcesteraq_map)
# Add the colormap to the map
worcesteraq_map.add_child(colormap)
worcesteraq_map.add_child(folium.GeoJson("WorcesterBoundary_JS/woobounds_1_json.json"))

```

The output leaflet map was then saved as an HTML file _WorcesterAirQualityMap_1.html_

**The output map looks like the following:**
<img width="600px" src="WebMap_setup\Images\HTML_outputfinal.png" alt="workflow"></img>


# Map Revisions (since presenting in class)
## Fixing AirNOW Sensor Coordinates
As mentioned in my presentation, the AirNOW sensor was being read in from the API with incorrect coordinates. The coordinates were fixed by dropping the original Latitude and Longitude fields read in by the API. Then, new Latitude and Longitude fields were created that contained the correct coordinates. 

See code below:
<img width="600px" src="WebMap_setup\Images\fixing_AirNOW_coordinates.png" alt="workflow"></img>

## Fixing an issue with City Boundary JSON
To get a json of the Worcester city boundary:
1. Downloaded shapefile of Massachusetts municipalities from the MassGIS website MassGIS Data: Municipalities | Mass.gov
2. Imported the shapefile into QGIS
3. Extracted Worcester shapefile using the attribute table
4. Exported the selected Worcester boundary feature as a JSON file

<img width="600px" src="WebMap_setup\Images\cityboundary_qgis.png" alt="workflow"></img>

Although when I presented my map in class, the json of the city of Worcester boundary rendered, once I re-ran my script, it no longer showed up.

I figured out this was due to the HTML file being re-written everytime I ran the _AirQuality_visualize_1.py_ script. 

To fix this issue, I imported the json using the folium package directly in the _AirQuality_visualize_1.py_ file and added it to the map. 

See the code below:
```
worcesteraq_map.add_child(folium.GeoJson("WorcesterBoundary_JS/woobounds_1_json.json"))
```

## Hosting the Web Map via GitHub Pages
I was inspired by Andre's web map in Narrrative Cartography and saw that, though his sight wasn't on a public domain yet, he was able to run it off of his GitHub repo. 

I looked into the process of developing a GitHub Page from my repo and thought it would be more efficient for me to create a new repo with only the files I actively used to create the web map. This is the repo called: **_WorcesterAQ_WebMap_** this is the GitHub repo that the final results of my project will be on (so please ignore the previous one you had access to!). 

... I was then able to succesfully create a GitHub Page by going into my repo settings and clicking on pages!!

See the screenshot below:

<img width="600px" src="WebMap_setup\Images\GitHub_pagesetup.png" alt="workflow"></img>

To view the web page follow the link here: https://dahall15.github.io/AirQualityDashboard_Worcester/WorcesterAirQualityMap_1.html


# Final Reflections and Future Steps
In regard to Spatial Databases, I am excited about the outcome of this project. Seeing my peers developing web maps and web apps as well was extremely helpful in seeing there are more ways than one to create a web map. It was especially helpful to create this web map under the lens of spatial database development. Having SQL, schemas, and PgAdmin fresh in my mind allowed me to better understand APIs and what it means to read them into a CSV. Coming into the course, I was very unfamiliar with more 'back end' development and data hosting, but after having took this course and bridging future applications of web map developemt with spatial databases, I feel I have a lot more of a better understanding of how all of this works!

I was unable to host the web map via server, though I tried using Node (and I would have had to keep the node open in my terminal the whole time), for now, I was only able to move the web map off from being hosted only locally. In the coming weeks, I would still like to see if I can have access to the Clark University ESRI ArcGIS Server and host the data there. It is desired to host this on ArcGIS Online, like CalEnviro Screen but I am still trying to figure out the connection between making sure the API is pulled from regualarly, making the code accessible, and making it so that the PM2.5 values are visualized properly on ArcGIS Online!

My reason for this is that it would allow me to develop the web map (with a lot more features might I add) and host the scripts and files in a place that John Rogan and others will have access to once I am no longer at Clark. Additionally, it would allow for the web map to be improved and for Clark as an instituion to host this tool for the city. 
 
## Future Steps
I would like to improve the aesthetics of the map, including a header, unique pop-ups and other tools so that the web map.