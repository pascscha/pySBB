from datetime import datetime


class Parameter:
    def __init__(self, name, optional=True, default=None, valid_types=None, valid_values=None):
        self.name = name
        self.default = default
        self.valid_types = valid_types
        self.valid_values = valid_values

    def parse(self, value):
        if value is None:
            if self.optional:
                return None
            else:
                raise TypeError("{}: Non-Optional value cannot be None".format(self.name))

        if self.valid_types is not None and type(value) not in self.valid_types:
            expected_types = " or ".join([str(t) for t in self.valid_types])
            raise TypeError("{}: Expected {} but got {} with type {}".format(self.name, expected_types, value, type(value)))
        else:
            processed_value = self.process(value)

            if self.valid_values is not None and processed_value not in self.valid_values:
                expected_values = " or ".join([str(v) for v in self.valid_values])
                raise ValueError("{}: Expected {} but got {}".format(self.name, expected_values, processed_value))
            else:
                return processed_value

    def process(self, value):
        return str(value)


class ListParameter(Parameter):
    def __init__(self, name, element_parameter, *args, min_length=None, max_length=None, **kwargs):
        if element_parameter.valid_types is None:
            super().__init__(name, *args, **kwargs)
        else:
            super().__init__(name, *args, valid_types=[list] + element_parameter.valid_types, **kwargs)
        self.element_parameter = element_parameter
        self.min_length = min_length
        self.max_length = max_length

    def process(self, value):
        if type(value) is not list:
            value = [value]
        out = []
        for elem in value:
            out.append(self.element_parameter.parse(elem))

        if self.min_length is not None and len(out) < self.min_length:
            raise ValueError("{}: List length can't be smaller than {} but is {}".format(self.name, self.min_length, len(out)))
        if self.max_length is not None and len(out) > self.max_length:
            raise ValueError("{}: List length can't be bigger than {} but is {}".format(self.name, self.max_length, len(out)))

        return out


class BoolParameter(Parameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, valid_types=[bool], **kwargs)

    def process(self, value):
        if value:
            return "1"
        else:
            return "0"


class BoundedParameter(Parameter):
    def __init__(self, *args, lower_bound=None, upper_bound=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def process(self, value):
        if self.lower_bound is not None and value < self.lower_bound:
            raise ValueError("{}: Value can't be smaller than {} but is {}".format(self.name, self.lower_bound, value))
        if self.upper_bound is not None and value > self.upper_bound:
            raise ValueError("{}: Value can't be bigger than {} but is {}".format(self.name, self.upper_bound, value))
        return str(value)


class DateParameter(Parameter):
    def __init__(self, *args, in_format="%Y-%m-%d", out_format="%Y-%m-%d", **kwargs):
        super().__init__(*args, valid_types=[str], **kwargs)
        self.in_format = in_format
        self.out_format = out_format

    def process(self, value):
        datetime_object = datetime.strptime(value, self.in_format)
        return datetime_object.strftime(self.out_format)
