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

from ..data import Bar as _Bar
from ._order import Order as _Order
from ._order import OrderStatus as _OrderStatus
from ._order import OrderSide as _OrderSide

from typing import List as _List

OrderList = _List[_Order]
BarList = _List[_Bar]

class UserState:
    EPSILON = 0.05
    def __init__(self, principal: float):
        self.principal: float = principal
        self.orders: OrderList = []

    def _get_volume(self, orders: OrderList) -> int:
        volume = 0
        for o in orders:
            volume += o.num_shares
        return volume

    def _get_price(self, orders: OrderList) -> float:
        price = 0
        volume = self._get_volume(orders)
        for o in orders:
            price += ((1.0 * o.num_shares * o.price) / volume)
        return price

    def _value_helper(self, bars: BarList, include_open: bool) -> float:
        filled_orders = list(filter(lambda o: o.order_status == _OrderStatus.FILLED, self.orders))
        filled_tickers = [fo.bar.ticker for fo in filled_orders]
        filled_tickers = list(list(set(filled_tickers)))

        total = self.principal
        for ft in filled_tickers:
            buy_orders = list(filter(lambda o: o.order_side == _OrderSide.BUY, filled_orders))
            sell_orders = list(filter(lambda o: o.order_side == _OrderSide.SELL, filled_orders))
            
            buy_volume = self._get_volume(buy_orders)
            buy_price = self._get_price(buy_orders)

            sell_volume = self._get_volume(sell_orders)
            sell_price = self._get_volume(sell_orders)

            if buy_volume > sell_volume:
                realized_profit = (sell_price - buy_price) * sell_volume
                if include_open:
                    buy_open_diff = buy_volume - sell_volume
                    for b in bars:
                        if b.ticker == ft:
                            realized_profit += ((b.close - buy_price) * buy_open_diff)
                            break
                else:
                    buy_open_diff = buy_volume - sell_volume
                    total -= (buy_open_diff * buy_price)
                total += realized_profit
            else:
                realized_profit = (sell_price - buy_price) * buy_volume
                if include_open:
                    sell_open_diff = sell_volume - buy_volume
                    for b in bars:
                        if b.ticker == ft:
                            realized_profit += ((sell_price - b.close) * sell_open_diff)
                            break
                else:
                    sell_open_diff = sell_volume - buy_volume
                    total -= (sell_open_diff * sell_price)
                total += realized_profit

        return total

    def update(self, bars: BarList):
        open_orders = list(filter(lambda o: o.order_status == _OrderStatus.OPEN, self.orders))
        for o in open_orders:
            for b in bars:
                if o.bar.ticker == b.ticker:
                    if o.order_side == _OrderSide.BUY and ((b.close - UserState.EPSILON) > o.price):
                        o.order_status = _OrderStatus.FILLED
                    elif o.order_side == _OrderSide.SELL and ((b.close + UserState.EPSILON) < o.price):
                        o.order_status = _OrderStatus.FILLED

    def get_account_value(self, bars: BarList) -> float:
        return self._value_helper(bars, True)

    def get_cash_value(self) -> float:
        return self._value_helper(None, False)

    def get_purchasing_power(self) -> float:
        open_orders = list(filter(lambda o: o.order_status == _OrderStatus.OPEN, self.orders))
        return self.get_cash_value() - (self._get_volume(open_orders) * self._get_price(open_orders))

class UserStateCheckpoint:
    def __init__(self, account_value:float, cash_value:float, purchasing_power:float, timestamp:_datetime):
        self.account_value = account_value
        self.cash_value = cash_value
        self.purchasing_power = purchasing_power
        self.timestamp = timestamp
