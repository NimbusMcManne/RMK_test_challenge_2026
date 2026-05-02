"""
Data processing package for Estonia Statistics API
"""

from .data_request import GETData
from .calc_probabilities import Calculations

__all__ = ['GETData', 'Calculations']
