# sbpy

This is an unofficial python wrapper for the SBB api. SBB are the "Schweizerische Bundes Bahnen" (Swiss Federal Transport)

# Installation
`pip3 install sbpy`

# Usage
This package lets you access the SBB api easily. Here is how to use it:

## Get Connections
It is very simple to get connections between two stations:
```
import sbpy

connections = sbpy.get_connections("Zürich", "Bern")
for c in connections:
	print(c)
```
Further parameters (see [connections](https://transport.opendata.ch/docs.html#connections)) for more info:
- via: Specifies up to five via locations.
- date: Date of the connection, in the format YYYY-MM-DD
- time: Time of the connection, in the format hh:mm
- isArrivalTime: Defaults to False, if set to True the passed date and time is the arrival time
- transportations: Transportation means; one or more of train, tram, ship, bus, cableway
- limit: 1 - 16. Specifies the number of connections to return. If several connections depart at the same time they are counted as 1.
- page: 0 - 3. Allows pagination of connections. Zero-based, so first page is 0, second is 1, third is 2 and so on.
- direct: defaults to False, if set to True only direct connections are allowed
- sleeper: defaults to False, if set to True only direct connections are allowed
- couchette: defaults to False, if set to True only night trains containing couchettes are allowed, implies direct=True
- bike: defaults to False, if set to True only trains allowing the transport of bicycles are allowed
- accessibility: Possible values are independent_boarding, assisted_boarding, and advanced_notice

## Get Locations
The api allows you to find locations such as train stations, addresses and other point of interests (eg. Clock Tower or China Garden)
```
import sbpy

locations = sbpy.get_locations(query="Lidostrasse 5 Luzern")
for l in locations:
    print(l)
```
Further parameters (see [locations](https://transport.opendata.ch/docs.html#locations) for more info:
- query: Specifies the location name to search for
- x: Latitude
- y: Longitude
- type: Only with query parameter. Specifies the location type, possible types are:
	* all (default): Looks up for all types of locations
	* station: Looks up for stations (train station, bus station)
	* poi: Looks up for points of interest (Clock tower, China garden)
	* address: Looks up for an address (Zurich Bahnhofstrasse 33)

## Get Stationboards
Stationboards are the big blue boards that can be seen at trainstations. These are also available via the api.
```
import sbpy

entries = sbpy.get_stationboard("Lugano")
for e in entries:
    print(e)
```
Further parameters (see [stationboard](https://transport.opendata.ch/docs.html#stationboard)) for more info:
- id: The id of the station whose stationboard should be returned. Overwrites to the station parameter.
- limit: Number of departing connections to return. 
- transportations: Transportation means; one or more of train, tram, ship, bus, cableway
- date: Date of departing connections, in the format YYYY-MM-DD
- time: Time of departing connections, in the format hh:mm
- type: departure (default) or arrival
