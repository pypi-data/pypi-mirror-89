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

from ..config import Config as _Config
from ..config import UserConfig as _UserConfig
from ..data import Bar as _Bar
from ..data import DataSourceBase as _DataSourceBase
from ._order import Order as _Order
from ._order import OrderSide as _OrderSide
from ._order import OrderStatus as _OrderStatus
from ._policy import ClosePolicy as _ClosePolicy
from ._state import UserState as _UserState
from ._state import UserStateCheckpoint as _UserStateCheckpoint
from ..strategy import StrategyBase as _StrategyBase

from typing import List as _List

BarList = _List[_Bar]
ClosePolicyList = _List[_ClosePolicy]
UserStateCheckpointList = _List[_UserStateCheckpoint]

class Simulator:
    EPSILON = 0.05
    def __init__(self, config: _Config, user_config: _UserConfig,
                 strategy: _StrategyBase, data_source: _DataSourceBase,
                 close_policy_list: ClosePolicyList):
        self.config = config
        self.user_config = user_config
        self.user_state = _UserState(self.user_config.principal)
        self.strategy = strategy
        self.data_source = data_source
        self.close_policy_list = close_policy_list

        self.user_state_checkpoints: UserStateCheckpointList = []

    def _get_average_time(self, bars: BarList):
        return bars[0].timestamp

    def add_order(self, bar: _Bar, order_side: _OrderSide, price: float,
                  num_shares: int) -> bool:
        if price <= 0 or num_shares <= 0:
            return False
        if order_side == _OrderSide.BUY and ((bar.close - Simulator.EPSILON) < price):
            return False
        if order_side == _OrderSide.SELL and ((bar.close + Simulator.EPSILON) > price):
            return False

        # TODO: Check if order exceeds purchasing power
        new_order = _Order(bar, price, order_side, num_shares)
        self.user_state.orders.append(new_order)

        return True

    def cancel_order(self, order: _Order):
        order_index = 0
        try:
            order_index = self.user_state.orders.index(order)
        except:
            return False
        return self.user_state.orders[order_index].cancel()

    def process_strategy(self, bars: BarList):
        self.strategy.process_bar(self.user_state, bars, self.add_order, self.cancel_order)

    def process_closing_policies(self, bars: BarList):
        for p in self.close_policy_list:
            p.process_bar(self.user_state, bars, self.add_order, self.cancel_order)

    def process_user_state(self, bars: BarList):
        self.user_state.update(bars)

        account_value = self.user_state.get_account_value(bars)
        cash_value = self.user_state.get_cash_value()
        purchasing_power = self.user_state.get_purchasing_power()

        timestamp = self._get_average_time(bars)

        new_user_checkpoint = _UserStateCheckpoint(account_value, cash_value, purchasing_power, timestamp)
        self.user_state_checkpoints.append(new_user_checkpoint)

    def start(self):
        if(self.data_source.reset()):
            while(self.data_source.has_next()):
                datum = self.data_source.next()
                self.process_strategy(datum)
                self.process_closing_policies(datum)
                self.process_user_state(datum)
