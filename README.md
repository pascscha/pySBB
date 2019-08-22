# pySBB

This is an unofficial python wrapper for the SBB [API](https://transport.opendata.ch/docs.html). [SBB](https://www.sbb.ch) stands for the "Schweizerische Bundes Bahnen" (Swiss Federal Transport).

# Installation
`pip3 install pySBB`

# Usage
This package lets you access the SBB api easily. Here is how to use it:

## Get Connections
It is very simple to get connections between two stations:
```
import pySBB

connections = pySBB.get_connections("Zürich", "Bern")
for c in connections:
	print(c)
```
Example Output:
```
Zürich HB (18:32, Plat. 32) -> Bern (19:28, Plat. 32) | 56min
Zürich HB (19:02, Plat. 31) -> Bern (19:58, Plat. 31) | 56min
Zürich HB (19:32, Plat. 32) -> Bern (20:28, Plat. 32) | 56min
Zürich HB (20:02, Plat. 31) -> Bern (20:58, Plat. 31) | 56min
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
import pySBB

locations = pySBB.get_locations(query="Lidostrasse 5 Luzern")
for l in locations:
    print(l)
```
Example Output:
```
Luzern, Lidostr. 5
Verkehrshaus der Schweiz, Luzern, Lidostr. 5
Restaurant Piccard im Verkehrshaus der Schweiz, Luzern, Lidostr. 5
...
```
Further parameters (see [locations](https://transport.opendata.ch/docs.html#locations) for more info:
- query: Specifies the location name to search for
- x: Latitude
- y: Longitude
- type: Only with query parameter. Specifies the location type, possible types are:
	* all (default): Looks up for all types of locations
	* station: Looks up for stations (eg. train station, bus station)
	* poi: Looks up for points of interest (eg. Clock tower, China garden)
	* address: Looks up for an address (eg. Zurich Bahnhofstrasse 33)

## Get Stationboards
Stationboards are the big blue boards that can be seen at trainstations. These are also available via the api.
```
import pySBB

entries = pySBB.get_stationboard("Lugano")
for e in entries:
    print(e)
```
Example Output:
```
Lugano (18:51, Plat. 2) -> Chiasso
Lugano (18:55, Plat. 4) -> Bellinzona
Lugano (19:05, Plat. 2) -> Chiasso
Lugano (19:22, Plat. 2) -> Monza
Lugano (19:25, Plat. 4) -> Bellinzona
...
```
Further parameters (see [stationboard](https://transport.opendata.ch/docs.html#stationboard)) for more info:
- id: The id of the station whose stationboard should be returned. Overwrites to the station parameter.
- limit: Number of departing connections to return.
- transportations: Transportation means; one or more of train, tram, ship, bus, cableway
- date: Date of departing connections, in the format YYYY-MM-DD
- time: Time of departing connections, in the format hh:mm
- type: departure (default) or arrival

# Objects
The objects are the same as the ones used by the API, which are documented [here](https://transport.opendata.ch/docs.html#api-objects)

The only difference is that any strings containing times or durations have been converted to [datetime](https://docs.python.org/3/library/datetime.html) objects.

# Further Examples
## Get all transfer stations
The following code lets you see all transfer stations for a given connection
```
import pySBB

connection = pySBB.get_connections("Mauraz", "Amriswil", limit=1)[0]

print(connection)
for section in connection.sections:
    print("   {}".format(section))
```
```
Mauraz (11:48) -> Amriswil (16:05, Plat. 33) | 4h 17min
   Mauraz (11:48) -> Pampigny-Sévery (12:04)
   Pampigny-Sévery (12:04) -> L'Isle (12:13)
   L'Isle (12:13) -> L'Isle, gare (12:15)
   L'Isle, gare (12:15) -> Cossonay-Penthalaz, gare (12:35)
   Cossonay-Penthalaz, gare (12:35) -> Cossonay-Penthalaz (12:37)
   Cossonay-Penthalaz (12:37, Plat. 1) -> Yverdon-les-Bains (13:00, Plat. 1)
   Yverdon-les-Bains (13:00, Plat. 1) -> Zürich HB (14:56, Plat. 13)
   Zürich HB (14:56, Plat. 33) -> Amriswil (16:05, Plat. 2)
```

## Get passed stations with coordinates
The following code prints all station names that are passed, together with its coordinates.
```
import pySBB

connection = pySBB.get_connections("Brugg", "Basel", limit=1)[0]

print(connection)
for section in connection.sections:
    for passList in section.journey.passList:
        station = passList.station
        print("   {} {}".format(station.name, station.coordinate))
```

```
Brugg AG (11:41, Plat. 2) -> Basel SBB (12:24, Plat. 2) | 43min
   Brugg AG (47.48085, 8.208829)
   Frick (47.507341, 8.01309)
   Rheinfelden (47.551208, 7.792162)
   Basel SBB (47.547403, 7.589577)
```

## Get all follwing station for first stationboard entry
The following code prints all stations of the first ship departing from "Luzern Bahnhofquai" at a given date:
```
import pySBB

entry = pySBB.get_stationboard("Luzern Bahnhofquai", transportations="ship", datetime="2019-10-10 12:00", limit=1)[0]

print(entry)
for passList in entry.passList:
    print("   {}".format(passList))
```

```
Luzern Bahnhofquai (12:00, Plat. 1) -> Vitznau
   Verkehrshaus-Lido (12:10)
   Hertenstein (See) (12:30)
   Weggis (12:40)
   Vitznau (12:54)
```