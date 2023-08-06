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

from ..config import Config as _Config
from ..data import Bar as _Bar
from ..signal import MovingAverage as _MovingAverage
from ..simulator import OrderSide as _OrderSide
from ..utils import CircularBuffer as _CircularBuffer

from typing import List as _List

BarList = _List[_Bar]

class StrategyBase(ABC):
    def __init__(self, config, buffer_size: int = 20):
        super().__init__()
        self.config = config
        self.ticker_signals = {}
        self.output_buffer = {}
        self.buffer_size = buffer_size
        self._define_buffers()
        self._define_tickers()

    def ready(self):
        if len(self.config.tickers) == 0:
            return False
        ready = True
        for t in self.config.tickers:
            ready = (ready and self.output_buffer[t].ready())
        return ready

    def _signal_ready(self, signal_methods):
        ready = True
        for sm in signal_methods:
            ready = (ready and sm.ready())
        return ready

    def _define_output_buffer(self):
        arr_buffer = _CircularBuffer(self.buffer_size)
        return arr_buffer

    def _define_buffers(self):
        for t in self.config.tickers:
            self.output_buffer[t] = self._define_output_buffer()

    def _define_tickers(self):
        for t in self.config.tickers:
            self.ticker_signals[t] = self.define_signals(t)

    def process_bar(self, state, bars: BarList, add_order, cancel_order):
        for b in bars:
            signal_methods = self.ticker_signals[b.ticker]
            signal_outputs = []
            signal_ready = self._signal_ready(signal_methods)
            for sm in signal_methods:
                signal_outputs.append(sm.process_bar(b))

            if signal_ready:
                self.output_buffer[b.ticker].add(signal_outputs)

            if self.ready():
                signals = self.output_buffer[b.ticker].get()
                self.process_bar_wrapper(state, b, add_order, cancel_order, signals)

    @abstractmethod
    def define_signals(self, ticker):
        return

    @abstractmethod
    def process_bar_wrapper(self, state, bar:_Bar, add_order, cancel_order, signals):
        return

    
class SimpleMovingAverageStragegy(StrategyBase):
    def __init__(self, config, buffer_size: int = 2):
        super().__init__(config, buffer_size)

    def define_signals(self, ticker):
        twenty_moving_average = _MovingAverage(ticker, 20)
        fifty_moving_average = _MovingAverage(ticker, 50)
        return [twenty_moving_average, fifty_moving_average]

    def process_bar_wrapper(self, state, bar:_Bar, add_order, cancel_order, signals):
        previous_timestep = signals[0]
        current_timestep = signals[1]

        if current_timestep[0] > previous_timestep[0] and  current_timestep[1] < previous_timestep[1]:
            add_order(bar, _OrderSide.SELL, bar.close + 0.1, 1)
        elif current_timestep[0] < previous_timestep[0] and  current_timestep[1] > previous_timestep[1]:
            add_order(bar, _OrderSide.BUY, bar.close - 0.1, 1)

