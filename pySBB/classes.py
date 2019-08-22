# Author: Pascal Schärli

from datetime import timedelta, datetime


class SBBObject():

    # Element names we want to rename
    # (we can't use the variable name from as its a python keyword)
    blacklist = {
        "from": "start",
        "to": "end",
    }

    def __init__(self, data, name):
        self._data = data
        self.__name__ = name

        # Recursively convert dictionary into python classes
        for key, value in data.items():

            # Rename key if its in blacklist
            if key in self.blacklist:
                key = self.blacklist[key]

            # By adding variables to __dict__ we can access them just like
            # Other class variables
            self.__dict__[key] = self._get_object(key, value)

    def __repr__(self):
        return "<{} at 0x{:0x}>".format(self.__name__, id(self))

    def __str__(self):
        """String representation for SBBObjects. Different representations are used depending on what kind of class it is."""

        #
        # Start,Stop points
        #
        if self.__name__ in ["Start", "End", "Stop", "Passlist","Departure","Arrival"]:
            out = "{}".format(self.station)

            info = []
            if self.arrival is not None:
                info.append(self.arrival.strftime("%H:%M"))
            elif self.departure is not None:
                info.append(self.departure.strftime("%H:%M"))
            if self.platform is not None:
                info.append("Plat. {}".format(self.platform))
            if self.delay is not None and self.delay != 0:
                info.append("Delay {} min".format(self.delay))
            if len(info) > 0:
                out = out + " (" + ", ".join(info) + ")"
            return out
        elif self.__name__ in ["Station", "Location"]:
            if self.name is None:
                return ""
            else:
                return self.name
        elif self.__name__ == "Section":
            return "{} -> {}".format(self.departure, self.arrival)
            departure.station
        elif self.__name__ == "Journey":
            return "{}: {}".format(self.name, "->".join([str(p) for p in self.passList]))
        elif self.__name__ == "Coordinate":
            return "({}, {})".format(self.x, self.y)
        else:
            out = []
            for key, value in self.__dict__.items():
                if type(value) in [str, int, float] and not key.startswith("__"):
                    out.append(key + "=" + str(value))
            return "{}: {}".format(self.__name__, ", ".join(out))

    def _get_object(self, key, value):
        if type(value) == dict:
            return SBBObject(value, key.title())
        elif type(value) == list:
            out = []
            for val in value:
                if key[-1] == "s":
                    key = key[:-1]
                out.append(self._get_object(key, val))
            return out
        elif self.isnumber(value):
            if int(value) == float(value):
                return int(value)
            else:
                return float(value)
        elif key in ["departure", "arrival"] and value is not None:
            return datetime.strptime(value[:-5], "%Y-%m-%dT%H:%M:%S")
        elif key == "duration" and value is not None:
            days = int(value[0:2])
            hours = int(value[3:5])
            minutes = int(value[6:8])
            seconds = int(value[9:10])
            return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        else:
            return value

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
    def isnumber(value):
        try:
            float(value)
            return True
        except:
            return False


class Connection(SBBObject):
    def __init__(self, data):
        super().__init__(data, "Connection")

    def __str__(self):
        return "{} -> {} | {}".format(self.start, self.end, self._timedelta_string(self.duration))


class StationBoardEntry(SBBObject):
    def __init__(self, data):
        super().__init__(data, "StationBoardEntry")

    def __str__(self):
        return "{} -> {} ".format(self.stop, self.end)


class Location(SBBObject):
    def __init__(self, data):
        super().__init__(data, "Location")
