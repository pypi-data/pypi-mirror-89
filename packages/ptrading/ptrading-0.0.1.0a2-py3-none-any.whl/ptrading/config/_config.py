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

from ..utils import TimeUnit as _TimeUnit

from typing import List as _List

TickerType = _List[str]

class Config:
    def __init__(self, tickers: TickerType, pre_market: bool,
                 time_unit: _TimeUnit, start_time: _datetime,
                 end_time: _datetime):
        self.tickers: TickerType = tickers
        self.pre_market: bool = pre_market
        self.time_unit: _TimeUnit  = time_unit
        self.start_time: _datetime = start_time
        self.end_time: _datetime = end_time

class UserConfig:
    def __init__(self, principal: float):
        self.principal: float = principal
