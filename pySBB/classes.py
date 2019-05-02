import datetime

# Author: Pascal Schärli


class Connection:
    def __init__(self, json):
        if "from" in json and json["from"] is not None:
            self.start = Stop(json["from"])  # We can't use from as a name since its a taken python keyword :(
        else:
            self.start = None
        if "to" in json and json["to"] is not None:
            self.end = Stop(json["to"])
        else:
            self.end = None
        if "duration" in json and json["duration"] is not None:
            self.duration = Duration(json["duration"])
        else:
            self.duration = None

    def __str__(self):
        return "{} -> {} | {}".format(self.start, self.end, self.duration)


class Stop:
    def __init__(self, json):
        if "station" in json and json["station"] is not None:
            self.station = Location(json["station"])
        else:
            self.station = None
        if "arrival" in json and json["arrival"] is not None:
            self.arrival = Time(json["arrival"])
        else:
            self.arrival = None
        if "departure" in json and json["departure"] is not None:
            self.departure = Time(json["departure"])
        else:
            self.departure = None
        if "delay" in json:
            self.delay = json["delay"]
        else:
            self.delay = None
        if "platform" in json:
            self.platform = json["platform"]
        else:
            self.platform = None

    def __str__(self):
        out = "{}".format(self.station)

        info = []
        if self.arrival is not None:
            info.append("{}".format(self.arrival))
        if self.departure is not None:
            info.append("{}".format(self.departure))
        if self.platform is not None:
            info.append("Plat. {}".format(self.platform))
        if self.delay is not None and self.delay != 0:
            info.append("Delay {} min".format(self.delay))
        if len(info) > 0:
            out = out + " (" + ", ".join(info) + ")"
        return out


class StationBoardEntry:
    def __init__(self, json):
        if "stop" in json and json["stop"] is not None:
            self.stop = Stop(json["stop"])
        else:
            self.stop = None
        if "to" in json:
            self.to = json["to"]
        else:
            self.to = None
        if "category" in json:
            self.category = json["category"]
        else:
            self.category = None
        if "number" in json:
            self.number = json["number"]
        else:
            self.number = None
        if "name" in json:
            self.name = json["name"]
        else:
            self.name = None

    def __str__(self):
        return "{} -> {}".format(self.stop, self.to)


class Time:
    def __init__(self, time):
        self.year = int(time[0:4])
        self.month = int(time[5:7])
        self.day = int(time[8:10])
        self.hour = int(time[11:13])
        self.minute = int(time[14:16])

    def __str__(self):
        date = datetime.datetime.now()
        if self.year == date.year:
            if self.month == date.month and self.day == date.day:
                return "{:02d}:{:02d}".format(self.hour, self.minute)
            else:
                return "{:02d}.{:02d} {:02d}:{:02d}".format(self.day, self.month, self.hour, self.minute)
        return "{:02d}.{:02d}.{} {:02d}:{:02d}".format(self.year, self.day, self.month, self.hour, self.minute)


class Duration:
    def __init__(self, duration):
        if duration is not None:
            self.days = int(duration[0:2])
            self.hours = int(duration[3:5])
            self.minutes = int(duration[6:8])
            self.seconds = int(duration[9:11])

    def __str__(self):
        out = []
        added = False
        if self.days != 0:
            out.append("{}d".format(self.days))
            added = True
        if self.hours != 0 or added:
            out.append("{}h".format(self.hours))
            added = True
        if self.minutes != 0 or added:
            out.append("{}min".format(self.minutes))
            added = True
        if self.seconds != 0:
            out.append("{}s".format(self.seconds))

        return " ".join(out)


class Location:
    def __init__(self, json):
        if "id" in json and json["id"] is not None:
            self.id = int(json["id"])
        else:
            self.id = None
        if "name" in json:
            self.name = json["name"]
        else:
            self.name = None
        if "score" in json:
            self.score = json["score"]
        else:
            self.score = None
        if "distance" in json and json["distance"] is not None:
            self.distance = int(json["distance"])
        else:
            self.distance = None
        if "coordinate" in json and json["coordinate"] is not None:
            self.coordinates = Coordinates(json["coordinate"])
        else:
            self.coordinates = None

    def __str__(self):
        return self.name


class Coordinates:
    def __init__(self, json):
        if "x" in json:
            self.x = json["x"]
        else:
            self.x = None
        if "y" in json:
            self.y = json["y"]
        else:
            self.y = None

    def __str__(self):
        return "({}, {})".format(self.x, self.y)
