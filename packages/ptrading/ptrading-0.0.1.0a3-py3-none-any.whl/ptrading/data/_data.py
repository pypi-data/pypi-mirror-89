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

import nest_asyncio
nest_asyncio.apply()

from abc import ABC, abstractmethod

import alpaca_trade_api as _tradeapi
from alpaca_trade_api import StreamConn as _StreamConn
from datetime import datetime as _datetime
from datetime import timedelta as _timedelta
import numpy as _np
import pytz
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

    @abstractmethod
    def set_callback(self, data_callback):
        return

    @abstractmethod
    def start_feed(self):
        return

class AlpacaDataSource(DataSourceBase):
    DELTA = _timedelta(days=1)
    def __init__(self, alpaca_key: str, alpaca_secret: str, config: _Config,
                 live: bool):
        self._alpaca_key = alpaca_key
        self._alpaca_secret = alpaca_secret
        self._api = _tradeapi.REST(self._alpaca_key, self._alpaca_secret,
                                   api_version='v2')

        self._conn = _StreamConn(self._alpaca_key, self._alpaca_secret)

        self.buffer_bar = []
        self.cursor = 0
        self.data_callback = None

        super().__init__(config, live)
        
        if not self.live:
            self._get_ticker_array()

    def _daylight_savings_offset(self, date):
        tz = pytz.timezone('America/New_York')
        offset_seconds = tz.utcoffset(date).seconds
        offset_hours = offset_seconds / 3600.0
        offset_hours -= 24
        if (offset_hours == -4.00):
            return "-04:00"
        else:
            return "-05:00"
        # return ("{:+02d}:{:02d}".format(int(offset_hours), int((offset_hours % 1) * 60)))

    def _create_bar_backtest(self, bar, ticker):
        return _Bar(bar.t, bar.o, bar.c, bar.h, bar.l, bar.v, ticker)

    def _create_bar_live(self, bar):
        return _Bar(bar.timestamp, bar.open, bar.close, bar.high, bar.low, bar.volume, bar.symbol)

    def _get_ticker_array(self):
        self.start_time = self.config.start_time
        self.end_time = self.config.end_time

        current_day = self.start_time
        while current_day != self.end_time:
            current_day_str = current_day.strftime("%Y-%m-%d")
            if _np.is_busday(current_day_str):
                start_day = current_day + _timedelta(hours=9, minutes=30)
                end_day = current_day + _timedelta(hours=16)

                start_day_str = start_day.strftime("%Y-%m-%dT%H:%M:%S" + self._daylight_savings_offset(current_day))
                end_day_str = end_day.strftime("%Y-%m-%dT%H:%M:%S" + self._daylight_savings_offset(current_day))

                for t in self.config.tickers:
                    barset = self._api.get_barset(t, 'minute',
                                                  start=start_day_str,
                                                  end=end_day_str)
                    bars = barset[t]
                    bar_set = [ self._create_bar_backtest(b, t) for b in bars]
                    self.buffer_bar.extend(bar_set)
                    _time.sleep(0.5)

            current_day += AlpacaDataSource.DELTA
        self.buffer_bar.sort(key=lambda x: x.timestamp)

    def reset(self) -> bool:
        self.data_callback = None
        if not self.live:
            self.cursor = 0

        return True

    def has_next(self) -> bool:
        if not self.live:
            return self.cursor < len(self.buffer_bar)
        else:
            return True

    def next(self) -> BarList:
        if not self.live:
            tickers = [ self.buffer_bar[self.cursor] ]
            self.cursor += 1
            return tickers

    def current(self) -> BarList:
        return [ self.buffer_bar[self.cursor] ]

    def set_callback(self, data_callback):
        self.data_callback = data_callback
        if self.live:
            @self._conn.on(r'^AM.*$', self.config.tickers)
            async def on_bar(conn, channel, bar):
                processed_bar = self._create_bar_live(bar)
                self.data_callback([processed_bar])

    def start_feed(self):
        if self.data_callback != None:
            if not self.live:
                while(self.has_next()):
                    datum = self.next()
                    self.data_callback(datum)
            else:
                ticker_array = [ 'AM.' + t for t in self.config.tickers ]
                sself._conn.run(ticker_array)
