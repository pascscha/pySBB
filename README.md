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
This is a descripition of all objects used by this api.

## Connection
A connection represents a possible journey between two locations.
### Parameters:
| Name     | Type     | Description                       |
| ---------|:--------:|:--------------------------------- |
| start    | Stop     | The starting point of the journey |
| end      | Stop     | The end point of the journey      |
| duration | Duration | How long the journey takes        |
### Functions:
| Name     | Return Type  | Description                                        |
| ---------|:------------:|:---------------------------------------------------|
| __str__  | str          | Returns a string representation of the Connection. |

## Stop
A stop represents an arrival or a departure point (in time and space) of a connection.
### Parameters:
| Name      | Type     | Description                                                         |
| ----------|:--------:|:--------------------------------------------------------------------|
| station   | Location | A location object showing this line's stop at the requested station |
| arrival   | Time     | The arrival time to the checkpoint                                  |
| departure | Time     | The departure time from the checkpoint                              |
| delay     | int      | The delay of this connection                                        |
| platform  | str      | The arrival/departure platform                                      |
### Functions:
| Name     | Return Type  | Description                                  |
| ---------|:------------:|:---------------------------------------------|
| __str__  | str          | Returns a string representation of the Stop. |

## Location
Can be any location, station address or point of iterest.
### Parameters:
| Name        | Type        | Description                                                               |
| ------------|:-----------:|:--------------------------------------------------------------------------|
| id          | int         | The id of the location                                                    |
| name        | str         | The name of the location                                                  |
| score       | str         | The accuracy of the result                                                |
| distance    | int         | If search has been with coordinates, distance to original point in meters |
| coordinates | Coordinates | The location coordinates                                                  |
### Functions:
| Name     | Return Type  | Description                                      |
| ---------|:------------:|:-------------------------------------------------|
| __str__  | str          | Returns a string representation of the Location. |

## Duration
A duration object holds the duration it takes to complete a journey
### Parameters:
| Name        | Type        | Description            |
| ------------|:-----------:|:-----------------------|
| days        | int         | The number of days    |
| hours       | int         | The number of hours   |
| minutes     | int         | The number of minutes |
| seconds     | int         | The number of seconds |
### Functions:
| Name     | Return Type  | Description                                      |
| ---------|:------------:|:-------------------------------------------------|
| __str__  | str          | Returns a string representation of the Duration. |

## Time
A time object holds the time for some event such as arrival at a checkpoint. Notice that there is no 
### Parameters:
| Name        | Type        | Description              |
| ------------|:-----------:|:-------------------------|
| year        | int         | The year of this event   |
| month       | int         | The month of this event  |
| day         | int         | The day of this event    |
| hour        | int         | The hour of this event   |
| minute      | int         | The minute of this event |
### Functions:
| Name     | Return Type  | Description                                  |
| ---------|:------------:|:---------------------------------------------|
| __str__  | str          | Returns a string representation of the Time. |


## Coordinates
Coordinates describe the location of any geographical point used by this package.
### Parameters:
| Name        | Type        | Description    |
| ------------|:-----------:|:---------------|
| x           | int         | The latitude   |
| y           | int         | The longitude  |
### Functions:
| Name     | Return Type  | Description                                         |
| ---------|:------------:|:----------------------------------------------------|
| __str__  | str          | Returns a string representation of the Coordinates. |
