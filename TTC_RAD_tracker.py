import pandas as pd
import requests
import xml.etree.ElementTree as ET
import numpy as np 
from datetime import datetime 
import random

#Current bus route to garage allocations (Last update: 2023-01-12)
route_df = pd.read_excel('Route Allocations.xlsx')
routeAllocations = route_df.to_dict('records')[0]

#Current bus to garage allocations (Last update: 2023-01-12)
bus_df = pd.read_excel('Bus Allocations.xlsx')
busAllocations = bus_df.to_dict('records')[0]

#High level overview of the program:
#1. Use command=vehicleLocations in the XML feed to get all currently active vehicles.
#2. If a special sightings hit occurs, record its route and dirTag.
#3. Use command=routeConfig with r=route to search for the stop tags of the dirTag the vehicle is on.
#4. Use command=predictions and start with s=<the last stop tag>. If vehicle is not found, go to the previous stop tag and continue until vehicle is found. 
#5. Record the block of the vehicle and use command=schedule to find the next departures in the block. 

#Function to create parseable XML file from URL
def create_XML_file(url):
    #Create HTTP response object from given URL
    resp = requests.get(url)
    #Save the XML file
    with open('data.xml', 'wb') as f:
        f.write(resp.content)

#Get the data from the vehicleLocations API
vehicleLocations = requests.get('https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc')
vehicleLocationsTree = ET.fromstring(vehicleLocations.content)

#List of found special sightings will be added here
RADs = np.array([])
nextDeparturesDict = {} 

###STEP 1###
#Read the API data
for child in vehicleLocationsTree.iter('*'): #Iterate through all the XML tags 
    if(child.tag == 'vehicle'):
        vehicle = child.get('id')
        route = child.get('routeTag')
        secsSinceReport = child.get('secsSinceReport')
        if(vehicle.isnumeric() == True and int(secsSinceReport) < 60):
            ###STEP 2###
            if(int(vehicle) not in busAllocations): #Disregard streetcars
                continue
            vehicleGarage = busAllocations[int(vehicle)]
            routeGarage = routeAllocations[int(route)]
            if(vehicleGarage not in routeGarage): #Conditions for a special sighting
                dirTag = child.get('dirTag')

                ###STEP 3###
                create_XML_file('https://retro.umoiq.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=' + route)
                routeConfigTree = ET.parse('data.xml')
                routeConfigRoot = routeConfigTree.getroot()

                #Get the stoptags of the route. Shuffle them randomly to help find the bus more efficiently in step 4. 
                stopTags = routeConfigRoot.findall('route/stop')
                random.shuffle(stopTags)
                # for stopTag in stopTags:
                #     print(stopTag.attrib['tag'])
                    
                ###STEP 4###
                #Look for the vehicle in the predictions API using the stoptags of the route.
                for stopTag in stopTags:
                    stop = stopTag.attrib['tag']
                    create_XML_file('https://retro.umoiq.com/service/publicXMLFeed?command=predictions&a=ttc&r=' + route + '&s=' + stop)
                    predictionsTree = ET.parse('data.xml')
                    predictionsRoot = predictionsTree.getroot()
                    vehicleFound = False #Flag to determine whether to keep looking in the stopTags list 

                    predictions = predictionsRoot.findall('predictions/direction/prediction')
                    for prediction in predictions:
                        if prediction.attrib['vehicle'] == vehicle:
                            vehicleFound = True
                            run = prediction.attrib['block'] #Once the vehicle is found, record the block 
                            break
                    
                    if vehicleFound: break
                                
                #At this point we can check if we have a true RAD or a school special / "intercentre"
                #If we do not have a true RAD, continue to the next vehicle in the vehicleLocations list 
                dominantRoute = run.split('_')[0]
                if vehicleGarage in routeAllocations[int(dominantRoute)]: 
                    continue 

                ###STEP 5###
                create_XML_file('https://retro.umoiq.com/service/publicXMLFeed?command=schedule&a=ttc&r=' + route)
                scheduleTree = ET.parse('data.xml')
                scheduleRoot = scheduleTree.getroot()

                #Create a dictionary of the stops listed under the header. Key stop tag: Value stop name
                stopLookup = {}
                stops = scheduleRoot.findall('route/header/stop')
                for stop in stops:
                    stopLookup[stop.attrib['tag']] = stop.text
                
                #Generate a list of next block departures for the next 3 hours 
                nextDepartures = []
                xpath = './/tr[@blockID="' + run + '"]'
                departures = scheduleRoot.findall(xpath)
                for departure in departures:
                    timepoints = departure.findall('stop')
                    #Search for the start point
                    for timepoint in timepoints:
                        unwantedDeparture = False
                        if timepoint.text != '--':
                            startpointTime = timepoint.text
                            startpointHour = int(startpointTime.split(':')[0])
                            startpointMinute = int(startpointTime.split(':')[1])
                            currentTime = str(datetime.now().strftime("%H:%M"))
                            currentHour = int(currentTime.split(':')[0])
                            currentMinute = int(currentTime.split(':')[1])
                            diffInMin = (startpointHour * 60 + startpointMinute - 
                                         currentHour * 60 - currentMinute)
                            if(diffInMin < 0 or (diffInMin > 180 and diffInMin < 1260)): #In the past or too far into the future
                                unwantedDeparture = True
                                break

                            startpoint = timepoint.text + " at " + stopLookup[timepoint.attrib['tag']]
                            break

                    if unwantedDeparture:
                        continue

                    #Get the end point
                    endpoint = stopLookup[timepoints[-1].attrib['tag']]
                    nextDepartures.append(startpoint + " towards " + endpoint)

                nextDepartures.sort()
                nextDeparturesDict[vehicle] = nextDepartures
                
                RADs = np.append(RADs, vehicle + ' (' + vehicleGarage + ') on run ' + run + ' (' + routeGarage + '). Next departures:'  )

    #Retrieve the time and date the API was updated at         
    if(child.tag == 'lastTime'):
        timestamp = child.get('time')
        dateTime = datetime.fromtimestamp(int(timestamp) / 1e3)
        dateTime = dateTime.strftime("%Y-%m-%d %H:%M:%S")
        print("Updated at:", dateTime)
        print("") #New line

#Print results 
if(len(RADs) == 0):
    print("No special sightings currently")
else:
    RADs = np.sort(RADs)
    for x in RADs:
        print(x)
        vehicle = x.split(' ')[0]
        for y in nextDeparturesDict[vehicle]:
            print(y)
        
        print("\n")
        
        
