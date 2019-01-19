import requests
import datetime

from .utils import *
from .classes import *

name = "sbpy"
url = "http://transport.opendata.ch/v1/"


def get_connections(departure, arrival, via=None, date=None, time=None, isArrivalTime=False, transportations=None, limit=None, page=None, direct=None, sleeper=None, cauchette=None, bike=None, accessibility=None):

    params = {"from": parse_str(departure),
              "to": parse_str(arrival),
              "via": parse_list(via),
              "date": parse_date(date),
              "time": parse_time(time),
              "isArrivalTime": parse_bool(isArrivalTime),
              "transportations": parse_restricted_list(transportations, ["train", "tram", "ship", "bus", "cableway"]),
              "limit": parse_int(limit, lower_bound=1, upper_bound=16),
              "page": parse_int(page, lower_bound=0, upper_bound=3),
              "direct": parse_bool(direct),
              "sleeper": parse_bool(sleeper),
              "cauchette": parse_bool(cauchette),
              "bike": parse_bool(bike),
              "accessibility": parse_restricted_list(accessibility, ["independent_boarding", "assisted_boarding", "advanced_notice"])}

    # add "[]" to the keys which have lists as values
    array_entries = []
    for key, value in params.items():
        if type(value) == list and len(value) > 1:
            array_entries.append((key, value))
    for pair in array_entries:
        key = pair[0]
        value = pair[1]
        params.pop(key)
        params[key + "[]"] = value

    response = requests.get(url + "connections", params=params)
    json = response.json()
    out = []
    for conn in json["connections"]:
        out.append(Connection(conn))
    return out


def get_locations(query=None, x=None, y=None, type="all"):
    params = {"query": parse_str(query),
              "x": parse_float(x),
              "y": parse_float(y),
              "type": parse_restricted(type, ["all", "station", "poi", "address"])
              }

    response = requests.get(url + "locations", params=params)
    json = response.json()
    out = []
    for loc in json["stations"]:
        out.append(Location(loc))
    return out


def get_stationboard(station, id=None, limit=None, transportations=None, date=None, time=None, type="departure"):
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")  # 2012-03-25 17:30
    else:
        date = parse_date(date)
    if time is None:
        time = datetime.datetime.now().strftime("%H:%M")
    else:
        time = parse_time(time)

    params = {"station": parse_str(station),
              "id": parse_int(id),
              "limit": parse_int(limit),
              "transportations": parse_restricted_list(transportations, ["train", "tram", "ship", "bus", "cableway"]),
              "datetime": "{} {}".format(date, time),
              "type": parse_restricted(type, ["departure", "arrival"])}

    response = requests.get(url + "stationboard", params=params)
    json = response.json()
    out = []
    for stop in json["stationboard"]:
        out.append(StationBoardEntry(stop))
    return out
