import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
from inspect import Parameter, Signature


class StructMeta(type):
    def __new__(cls, name, bases, dict):
        clsobj = super().__new__(cls, name, bases, dict)
        sig = cls.make_signature(clsobj._fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj
    
    def make_signature(names):
        return Signature(
                Parameter(v, Parameter.POSITIONAL_OR_KEYWORD) for v in names
                )
        
class Stock(metaclass=StructMeta):
    """
    Class object to extract data and perform some analysis.
    - symbol: NASDAQ Symbol to be check
    - days: How many days of data you want to analyse
    - source: this are the datasources declared in https://github.com/pydata/pandas-datareader/blob/master/pandas_datareader/data.py
    - Construct issue with keyword args: https://stackoverflow.com/questions/8187082/how-can-you-set-class-attributes-from-variable-arguments-kwargs-in-python
    """
    _fields = []
    def __init__(self, source, days=0, *args, **kwargs):
        self.days = days
        self.source = source
        self._today = datetime.today()
        self._start_date = self._today-timedelta(days=self.days)
            
    @property
    def get_data(self):
        if self.source == 'nasdaq':
            df = web.get_nasdaq_symbols
        self._start_date = self._start_date.strftime('%Y-%m-%d')
        self._today = self._today.strftime('%Y-%m-%d')
        if self.symbol:
            assert hasattr(self, 'self.symbol')
            self.symbol = self.symbol.upper()
            df = web.DataReader(
                    self.symbol,
                    self.source,
                    self._start_date,
                    self._today)
        else:
            df = web.DataReader(
                    self.symbols,
                    self.source,
                    self._start_date,
                    self._today)
            yield df
        return df

aapl = Stock(source='nasdaq')
for _ in aapl.get_data:
    print(_)
