import abc
import requests
from datetime import datetime
from data.bar import Bar
from data.bar import BarContainer


class APILink(abc.ABC):

    """
    Class representing a link til an API. this object is returned from an API call when link = True. This object then
    contains a url and relevant data to process http response
    """

    def __init__(self, url):
        self.url = url

    @abc.abstractmethod
    def fetch(self):
        pass


class AlphaVantageLink(APILink):

    def __init__(self, url, json_header, datetime_format, interval, opn, close, high, low, volume, ascending):
        super().__init__(url)
        self.json_header = json_header
        self.datetime_format = datetime_format
        self.interval = interval
        self.opn = opn
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.ascending = ascending

    def fetch(self):
        response = requests.get(self.url).json()
        bars = []

        for i in response[self.json_header]:
            data = response[self.json_header][i]

            try:
                open_price = data[self.opn]
            except KeyError:
                open_price = 0

            try:
                close_price = data[self.close]
            except KeyError:
                close_price = 0

            try:
                low_price = data[self.low]
            except KeyError:
                low_price = 0

            try:
                high_price = data[self.high]
            except KeyError:
                high_price = 0

            try:
                volume = data[self.volume]
            except KeyError:
                volume = 0

            bar = Bar(datetime.strptime(i, self.datetime_format),
                      open_price,
                      close_price,
                      high_price,
                      low_price,
                      volume)

            bars.append(bar)

        if self.ascending:
            bars.reverse()

        response = BarContainer(bars, self.interval)
        return response


