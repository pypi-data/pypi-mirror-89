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

from enum import Enum as _Enum
from ..data import Bar as _Bar

class OrderStatus(_Enum):
    OPEN = 0
    CANCELLED = 1
    FILLED = 2

class OrderSide(_Enum):
    BUY = 0
    SELL = 1

class Order:
    def __init__(self, bar: _Bar, price: float, order_side: OrderSide,
                 num_shares: int):
        self.bar = bar
        self.price = price
        self.num_shares = num_shares
        self.order_side = order_side
        self.order_status = OrderStatus.OPEN

    def cancel(self) -> bool:
        if self.order_status == OrderStatus.OPEN:
            self.order_status = OrderStatus.CANCELLED
            return True
        return False
