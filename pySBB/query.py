#!/usr/bin/python3

# Author: Pascal Schärli
import requests
import datetime

from .utils import *
from .classes import *
from .parameter_parser import *


class Query:
    def __init__(self, url, return_class, *args, **kwargs):
        self.url = url
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        params = {}
        if len(args) != len(self.args):
            raise ValueError("Expected {} arguments but got {}".format(len(self.args), len(args)))

        for parser, value in zip(self.args, args):
            if value is not None:
                params[parser.name] = parser.parse(value)

        for kw, value in kwargs.items():
            if kw not in self.kwargs:
                raise ValueError("Unexpected Keyword argument {}.".format(kw))
            if value is not None:
                parser = self.kwargs[kw]
                params[parser.name] = parser.parse(value)

        response = requests.get(self.url, params=params)

        return return_class(response)


base_url = "http://transport.opendata.ch/v1/"

get_connections = Query(base_url + "connections", Connections,
                        Parameter("from", optional=False, valid_types=[str]),
                        Parameter("to", optional=False, valid_types=[str]),
                        via=ListParameter("via", Parameter("via", valid_types=[str])),
                        date=DateParameter("date", in_format="%Y-%m-%d", out_format="%Y-%m-%d"),
                        time=DateParameter("time", in_format="%H:%M", out_format="%H:%M"),
                        isArrivalTime=BoolParameter("isArrivalTime"),
                        transportations=ListParameter("transportations", Parameter("transportation", valid_values=["train", "tram", "ship", "bus", "cableway"])),
                        limit=BoundedParameter("limit", lower_bound=1, upper_bound=15, valid_types=[int]),
                        page=BoundedParameter("page", lower_bound=0, upper_bound=3, valid_types=[int]),
                        direct=BoolParameter("direct"),
                        sleeper=BoolParameter("sleeper"),
                        cauchette=BoolParameter("cauchette"),
                        bike=BoolParameter("bike"),
                        accessibility=ListParameter("accessibility", Parameter("accessibility", valid_values=["independent_boarding", "assisted_boarding", "advanced_notice"]))
                        )

get_locations = Query(base_url + "locations", Locations,
                      query=Parameter("query", valid_types=[str]),
                      x=Parameter("x", valid_types=[float]),
                      y=Parameter("y", valid_types=[float]),
                      type=Parameter("type", valid_values=["all", "station", "poi", "address"])
                      )

get_stationboard = Query(base_url + "stationboard", StationBoards,
                         Parameter("station", valid_types=[str]),
                         id=Parameter("id", valid_types=[int]),
                         limit=BoundedParameter("limit", lower_bound=0),
                         transportations=ListParameter("transportations", Parameter("transportation", valid_values=["train", "tram", "ship", "bus", "cableway"])),
                         datetime=DateParameter("datetime", in_format="%Y-%m-%d %H:%M", out_format="%Y-%m-%d %H:%M"),
                         type=Parameter("type", valid_values=["departure", "arrival"])
                         )
