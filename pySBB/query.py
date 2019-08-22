#!/usr/bin/python3

# Author: Pascal Schärli
import requests
import json


class Query:
    def __init__(self, url, return_class, return_key, *args, **kwargs):
        self.url = url
        self.args = args
        self.kwargs = kwargs
        self.return_class = return_class
        self.return_key = return_key

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

        response = requests.get(self.url, params=params).json()

        if "errors" in response:
            raise ValueError("The API responded with the following error: " + str(response["errors"]))

        data = response[self.return_key]

        out = []

        for elem in data:
            out.append(self.return_class(elem))

        return out
