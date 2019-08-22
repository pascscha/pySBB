from datetime import timedelta, datetime

# Author: Pascal Schärli


class SBBObject():

    blacklist = {
        "from": "start",
        "to": "end",
    }

    def __init__(self, data, name=None):
        self._data = data

        self.__name__ = name

        for key, value in data.items():

            if key in self.blacklist:
                key = self.blacklist[key]

            if type(value) == dict:
                self.__dict__[key] = SBBObject(value, name=key.title())
            elif key in ["departure", "arrival"] and value is not None:
                self.__dict__[key] = datetime.strptime(value[:-5], "%Y-%m-%dT%H:%M:%S")
            elif key == "duration" and value is not None:
                days = int(value[0:2])
                hours = int(value[3:5])
                minutes = int(value[6:8])
                seconds = int(value[9:10])
                self.__dict__[key] = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

            elif self.isint(value):
                self.__dict__[key] = int(value)

            elif self.isfloat(value):
                self.__dict__[key] = float(value)
            else:
                self.__dict__[key] = value

    def __repr__(self):
        return "<{} at 0x{:0x}>".format(self.__name__, id(self))

    def __str__(self):
        if self.__name__ in ["Start", "End"]:
            out = "{}".format(self.station)

            info = []
            if self.arrival is not None:
                info.append(self.arrival.strftime("%H:%M"))
            if self.departure is not None:
                info.append(self.departure.strftime("%H:%M"))
            if self.platform is not None:
                info.append("Plat. {}".format(self.platform))
            if self.delay is not None and self.delay != 0:
                info.append("Delay {} min".format(self.delay))
            if len(info) > 0:
                out = out + " (" + ", ".join(info) + ")"
            return out
        elif self.__name__ == "Station":
            return self.name
        else:
            out = []
            for key, value in self.__dict__.items():
                if type(value) == str and not key.startswith("__"):
                    out.append(key + "=" + value)
            return "{}: {}".format(self.__name__, ", ".join(out))

    @staticmethod
    def _timedelta_string(timedelta):
        out = []

        if timedelta.days < 0:
            timedelta = -timedelta
            out.append("-")

        days = timedelta.days
        hours, rem = divmod(timedelta.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        added = False
        if days != 0:
            out.append("{}d".format(days))
            added = True
        if hours != 0 or added:
            out.append("{}h".format(hours))
            added = True
        if minutes != 0 or added:
            out.append("{}min".format(minutes))
            added = True
        if not added:
            out.append("{}s".format(seconds))
        return " ".join(out)

    @staticmethod
    def isfloat(value):
        try:
            float(value)
            return True
        except:
            return False

    @staticmethod
    def isint(value):
        try:
            int(value)
            return True
        except:
            return False


class Connection(SBBObject):
    def __init__(self, data):
        super().__init__(data, name="Connection")

    def __str__(self):
        return "{} -> {} | {}".format(self.start, self.end, self._timedelta_string(self.duration))


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
