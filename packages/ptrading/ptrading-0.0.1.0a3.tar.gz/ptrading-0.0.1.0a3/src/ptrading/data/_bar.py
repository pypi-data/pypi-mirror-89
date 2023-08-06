"""
# -*- coding: utf-8 -*-
# Copyright © 2020 Abhishek Pratapa. All rights reserved.
#
# Use of this source code is governed by a BSD-3-clause license that can
# be found in the LICENSE.txt file or at https://opensource.org/licenses/BSD-3-Clause
"""

from __future__ import print_function as _
from __future__ import division as _
from __future__ import absolute_import as _

from datetime import datetime as _datetime

class Bar:
    def __init__(self, timestamp: _datetime, open_price: float,
                 close_price: float, high_price: float, low_price: float,
                 volume: int, ticker: str):
        self.timestamp = timestamp
        self.open = open_price
        self.close = close_price
        self.high = high_price
        self.low = low_price
        self.volume = volume
        self.ticker = ticker
