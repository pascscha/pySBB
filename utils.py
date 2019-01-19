def parse_bool(b):
    if b is None:
        return None
    if type(b) is not bool:
        raise TypeError("Expected boolean but got {} with type {}".format(b, type(b)))
    elif b:
        return "1"
    else:
        return "0"


def parse_restricted_list(v, l):
    if v is None:
        return None
    v = parse_list(v.lower())

    for value in v:
        parse_restricted(value, l)
    return v


def parse_restricted(v, l):
    if v not in l:
        raise ValueError("The entered value {} is not contained in the list of valid arguments {}.".format(v, l))
    return v


def parse_int(i, lower_bound=None, upper_bound=None):
    if i is None:
        return None
    if type(i) is not int:
        raise TypeError("Expected an integer but got {} with type {}".format(i, type(i)))
    else:
        if lower_bound and i < lower_bound:
            raise ValueError("The entered value {} is too small. (minimum: {})".format(i, lower_bound))
        elif upper_bound and i > upper_bound:
            raise ValueError("The entered value {} is too large. (maximum: {})".format(i, upper_bound))
        else:
            return str(i)


def parse_float(f, lower_bound=None, upper_bound=None):
    if f is None:
        return None
    if type(f) is not float:
        raise TypeError("Expected a fload but got {} with type {}".format(f, type(f)))
    else:
        if lower_bound and f < lower_bound:
            raise ValueError("The entered value {} is too small. (minimum: {})".format(f, lower_bound))
        elif upper_bound and f > upper_bound:
            raise ValueError("The entered value {} is too large. (maximum: {})".format(f, upper_bound))
        else:
            return str(f)


def parse_str(s):
    if s is None or s == "None":
        return None
    if type(s) is not str:
        raise TypeError("Expected a string but got {} with type {}.".format(s, type(s)))
    else:
        return s


def parse_list(v):
    if v is None:
        return None
    if type(v) is str:
        return [v]
    elif type(v) is not list:
        raise TypeError("Expected a string or a list but got {} with type {}.".format(v, type(v)))
    else:
        for via in v:
            if type(via) is not str:
                raise TypeError("Expected a string but got {} with type {}.".format(via, type(via)))
        return v


def parse_date(d):
    if d is None:
        return None
    if len(d) == 10:
        try:
            parse_int(d[0:4], lower_bound=2000, upper_bound=3000)  # year
            parse_int(d[5:7], lower_bound=1, upper_bound=12)  # month
            parse_int(d[8:10], lower_bound=1, upper_bound=31)  # day
        except (TypeError, ValueError):
            raise ValueError("Invalid date format: {} Expected format: YYYY-MM-DD".format(d))
    else:
        raise ValueError("Invalid date format: {} Expected format: YYYY-MM-DD".format(d))


def parse_time(t):
    if t is None:
        return None
    if len(t) == 5:
        try:
            parse_int(t[0:2], lower_bound=0, upper_bound=24)  # hour
            parse_int(t[3:5], lower_bound=0, upper_bound=59)  # minute
        except (TypeError, ValueError):
            raise ValueError("Invalid date format: {} Expected format: HH:MM".format(t))
    else:
        raise ValueError("Invalid date format: {} Expected format: HH:MM".format(t))
