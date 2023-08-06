"""
Trading-Technical-Indicators (tti) python library

tti is a python library for calculating more than 60 trading technical
indicators from stocks data. The library provides an API for:

* trading technical indicators value calculation
* trading technical indicators graph preparation
* trading signal calculation

For complete documentation see https://www.trading-technical-indicators.org/
"""

from tti import indicators
from tti import utils

__version__ = '0.1.b3'

__all__ = ['indicators', 'utils']
