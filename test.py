#!/usr/bin/python3

import pySBB

entries = pySBB.get_stationboard("Zürich, Milchbuck")[:5]
for entry in entries:
    print(entry.category, entry.number, entry.to, entry.stop.departure)
