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

class TimeUnit(_Enum):
    ONE_MINUTE = 0
    THREE_MINUTE = 1
    FIVE_MINUTE = 2
    FIFTEEN_MINUTE = 3
    THIRTY_MINUTE = 4
    FOURTY_FIVE_MINUTES = 5
    ONE_HOUR = 6
    TWO_HOUR = 7
    THREE_HOUR = 8
    FOUR_HOUR = 9
    ONE_DAY = 10
    TWO_DAY = 11
    THREE_DAY = 12
    FOUR_DAY = 13
    ONE_WEEK = 14
    TWO_WEEK = 15
    THREE_WEEK = 16
    ONE_MONTH = 17
