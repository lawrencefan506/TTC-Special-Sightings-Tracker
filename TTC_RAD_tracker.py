import pandas as pd
import requests
import xml.etree.ElementTree as ET
import numpy as np 
from datetime import datetime 

#Current bus route to garage allocations (Last update: 2022-11-21)
route_df = pd.read_excel('Route Allocations.xlsx')
routeAllocations = route_df.to_dict('records')[0]

#Current bus to garage allocations (Last update: 2022-12-23)
bus_df = pd.read_excel('Bus Allocations.xlsx')
busAllocations = bus_df.to_dict('records')[0]

#Get the data from the API
data = requests.get('https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc')
root = ET.fromstring(data.content)

#List of found special sightings will be added here
RADs = np.array([])

#Read the API data
for child in root.iter('*'): #Iterate through all the XML tags 
    if(child.tag == 'vehicle'):
        vehicle = child.get('id')
        route = child.get('routeTag')
        secsSinceReport = child.get('secsSinceReport')
        if(vehicle.isnumeric() == True and int(secsSinceReport) < 60):
            if(int(vehicle) in busAllocations and busAllocations[int(vehicle)] not in routeAllocations[int(route)]): #Conditions for a special sighting
                RADs = np.append(RADs, vehicle + ": " + route)

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
