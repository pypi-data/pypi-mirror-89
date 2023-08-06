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

from abc import ABC, abstractmethod

import alpaca_trade_api as _tradeapi
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta
import numpy as _np
import time as _time

from ..config import Config as _Config
from ..data import Bar as _Bar

from typing import List as _List

BarList = _List[_Bar]

class DataSourceBase(ABC):
    def __init__(self, config : _Config, live: bool):
        self.config = config
        self.live = live
        super().__init__()

    @abstractmethod
    def reset(self) -> bool:
        return

    @abstractmethod
    def has_next(self) -> bool:
        return

    @abstractmethod
    def next(self) -> BarList:
        return

    @abstractmethod
    def current(self) -> BarList:
        return

class AlpacaDataSource(DataSourceBase):
    DELTA = _timedelta(days=1)
    def __init__(self, alpaca_key: str, alpaca_secret: str, config: _Config,
                 live: bool):
        self._alpaca_key = alpaca_key
        self._alpaca_secret = alpaca_secret
        self._api = _tradeapi.REST(self._alpaca_key, self._alpaca_secret,
                                   api_version='v2')
        self.buffer_bar = []
        self.cursor = 0
        super().__init__(config, live)

        self._get_ticker_array()

    def _create_bar(self, bar, ticker):
        return _Bar(bar.t, bar.o, bar.c, bar.h, bar.l, bar.v, ticker)


    def _get_ticker_array(self):
        # TODO: allow multiple tickers
        self.ticker = self.config.tickers[0]
        self.start_time = self.config.start_time
        self.end_time = self.config.end_time

        current_day = self.start_time
        while current_day != self.end_time:
            current_day_str = current_day.strftime("%Y-%m-%d")
            if _np.is_busday(current_day_str):
                start_day = current_day + _timedelta(hours=9, minutes=30)
                end_day = current_day + _timedelta(hours=16)
                    
                # TODO: fix daylight savings offset
                # TODO: add premarket
                start_day_str = start_day.strftime("%Y-%m-%dT%H:%M:%S-04:00")
                end_day_str = end_day.strftime("%Y-%m-%dT%H:%M:%S-04:00")
                
                barset = self._api.get_barset(self.ticker, 'minute',
                                              start=start_day_str,
                                              end=end_day_str)

                bars = barset[self.ticker]
                bar_set = [ self._create_bar(b, self.ticker) for b in bars]
                self.buffer_bar.extend(bar_set)

                _time.sleep(0.5)

            current_day += AlpacaDataSource.DELTA

    def reset(self) -> bool:
        self.cursor = 0
        return True

    def has_next(self) -> bool:
        return self.cursor < len(self.buffer_bar)

    def next(self) -> BarList:
        # TODO: aggregrate bars based on config time_unit
        tickers = [ self.buffer_bar[self.cursor] ]
        self.cursor += 1
        return tickers

    def current(self) -> BarList:
        return [ self.buffer_bar[self.cursor] ]
