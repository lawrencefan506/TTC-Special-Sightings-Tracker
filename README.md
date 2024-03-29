# TTC-Special-Sightings-Tracker

Welcome to the TTC Special Sightings Tracker. This program uses the TTC's [NextBus API](https://webservices.umoiq.com/service/publicXMLFeed?command=vehicleLocations&a=ttc) to output all current special sightings, which are buses on routes which are run by other garages. An example output is: 

Updated at: 2022-05-17 15:27:19.935000

1350: 46   

1550: 24

3552: 104

1350 is a Mount Dennis bus on the 46, a Queensway route. 1550 is a Malvern bus on the 24, a Birchmount route. 3552 is an Arrow Rd bus on the 104, a Wilson route. Up-to-date information on bus and route allocations can be found on the CPTDB Wiki (link for each garage below): 

* [Arrow Rd (ARW)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Arrow_Rd._Division)
* [Birchmount (BIR)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Birchmount_Division)
* [Eglinton (EGL)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Eglinton_Division)
* [Malvern (MAL)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Malvern_Division)
* [McNicoll (MCN)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_McNicoll_Division)
* [Mount Dennis (MTD)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Mount_Dennis_Division)
* [Queensway (QSY)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Queensway_Division)
* [Wilson (WIL)](https://cptdb.ca/wiki/index.php/Toronto_Transit_Commission_Wilson_Division)

### Limitations

Sometimes, school specials or certain departures on routes are operated by another garage other than the one that runs said route. For example, in the May 2022 board period, the 32 is a Mount Dennis route and has three school specials in the afternoon: two from Arrow Rd and one from Wilson. The buses on these school specials will show up on the Special Sightings Tracker's output, even though they happen on a daily basis and are thus not considered special. Currently, the tracker has no method of distinguishing these school specials from true special sightings. 

### To use on a mobile Android device for use on the go 

1. Install the [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) app from the Google Play Store, which allows you to run Python on your Android device. 
2. Open Pydroid 3 and install the following Python libraries from the Pip menu: datetime, numpy, pandas, requests, openpyxl, and et-xmlfile. 
3. Download the included TTC_RAD_tracker.py file along with the spreadsheets Bus Allocations.xslx and Route Allocations.xslx onto your mobile device, ensuring that they are in the same folder / directory. 
4. Open TTC_RAD_tracker.py in Pydroid 3 and press the yellow play button on the bottom right to run. 

### Updates to Bus Allocations

* 2022-04-30: 8958 -> EGL
* 2022-05-06: 3474-3488 -> MAL
* 2022-09-07: 3489-3493, 9078-9079 -> MAL; 9139, 9225-9234 -> ARW
* 2022-09-26: 9220-9224 -> ARW
* 2022-10-09: 8877-8880 -> EGL; 8949, 8953-8954, 8958, 8960-8964 -> ARW
* 2022-11-01: 3105, 3109, 3111, 3115, 3119 -> ARW 
* 2022-11-14: 3100, 3103, 3122, 3125 -> ARW; 3105, 3109, 3111, 3115, 3119 -> MCN
* 2022-11-18: 1360, 1361, 1379 -> WIL; 3103 -> MCN
* 2022-11-19: 1393 -> WIL; 3320-3321, 3323-3325, 3327-3329 -> QSY; 8460-8468 -> BIR; 9210-9219 -> ARW; 9220-9234 -> MCN 
* 2022-11-23: 1392 -> WIL; 3322, 3326 -> QSY
* 2022-11-30: 3100, 3122, 3125 -> MCN
* 2022-12-23: 1356-1358, 1394, 1396-1398, 1401 -> WIL; 3302-3303, 3305, 3309 -> QSY; 9213-9215 -> BIR
* 2022-12-28: 3301, 3304, 3306-3308 -> QSY; 9210-9212, 9216 -> BIR
* 2023-01-06: 1359, 1362, 1369, 1378, 1385, 1386 -> WIL; 3313, 3316, 3318-3319 -> QSY; 3494-3509 -> MAL; 8868-8869; 8871-8880, 9212-9216 -> ARW
* 2023-01-12: 3310-3312, 3314-3315, 3317 -> QSY

### Updates to Route Allocations
* 2022-05-08: 172 -> EGL; 174 -> MTD; 306 -> BIR
* 2022-07-31: 506 Shuttle (Spadina Stn - Distillery) -> ARW, MAL, MCN
* 2022-09-07: 301/501 Shuttle -> WIL; 304/504 Shuttle -> BIR, QSY; 506 Shuttle -> EGL
* 2022-11-21: 301/501 Shuttle -> QSY, WIL; 503 shuttle -> BIR; 304/504 Shuttle -> WIL
* 2023-01-12: 301/501 Shuttle -> MTD, QSY, WIL

### Contact
Email: lawrencefan195@gmail.com

### Roadmap
1. Setup server endpoint
2. Create tracker module
3. Setup client
4. Deploy on Netify (test on sruge)

#### Later
4. Setup databse to presist user data

# Server setup guide
1. Run `source env/bin/activate` to activate the virtual environment
2. Run `python3 App.py` to launch the server