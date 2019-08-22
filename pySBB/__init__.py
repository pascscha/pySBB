from .query import Query
from .parameter_parser import *
from .classes import Connection, Location, StationBoardEntry

name = "pySBB"


base_url = "http://transport.opendata.ch/v1/"


get_connections = Query(base_url + "connections", Connection, "connections",
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

get_locations = Query(base_url + "locations", Location, "stations",
                      query=Parameter("query", valid_types=[str]),
                      x=Parameter("x", valid_types=[float]),
                      y=Parameter("y", valid_types=[float]),
                      type=Parameter("type", valid_values=["all", "station", "poi", "address"])
                      )

get_stationboard = Query(base_url + "stationboard", StationBoardEntry, "stationboard",
                         Parameter("station", valid_types=[str]),
                         id=Parameter("id", valid_types=[int]),
                         limit=BoundedParameter("limit", lower_bound=0),
                         transportations=ListParameter("transportations", Parameter("transportation", valid_values=["train", "tram", "ship", "bus", "cableway"])),
                         datetime=DateParameter("datetime", in_format="%Y-%m-%d %H:%M", out_format="%Y-%m-%d %H:%M"),
                         type=Parameter("type", valid_values=["departure", "arrival"])
                         )
