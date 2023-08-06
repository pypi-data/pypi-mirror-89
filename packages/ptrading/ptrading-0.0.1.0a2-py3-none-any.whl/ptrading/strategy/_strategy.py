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

from typing import List as _List

BarList = _List[_Bar]

class StrategyBase(ABC):
    def __init__(self, config : _Config):
        self.config = config

    @abstractmethod
    def process_bar(self, state, bars: BarList, add_order, cancel_order):
        return

class NoopStragegy(StrategyBase):
    def __init__(self, config):
        super().__init__(config)
        self.index = 0

    def process_bar(self, state, bars: BarList, add_order, cancel_order):
        from ..simulator import OrderSide as _OrderSide
        # signal 1
        # signal 2
        # process all signals

        if self.index == 2:
            add_order(bars[0], _OrderSide.BUY, 186.50, 10)

        if self.index == 3000:
            add_order(bars[0], _OrderSide.BUY, 170.0, 100)

        self.index += 1