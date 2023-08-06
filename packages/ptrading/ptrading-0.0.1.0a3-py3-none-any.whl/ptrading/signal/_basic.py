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

from ._signal import SignalBase as _SignalBase

class MovingAverage(_SignalBase):
    def __init__(self, ticker: str, buffer_size: int = 1000):
        super().__init__(ticker, buffer_size)

    def _get_average(self, arr):
        price = 0
        for a in arr:
            price += ((1.0 * (a.open + a.close + a.high + a.low))/ 4.0)

        if len(arr) == 0:
            return 0.0
        else:
            return (1.0 * price) / len(arr)

    def process_bar_wrapper(self, bar) -> float:
        self.buffer.add(bar)
        if self.buffer.ready():
            arr = self.buffer.get()
            return self._get_average(arr)
        return 0.0
