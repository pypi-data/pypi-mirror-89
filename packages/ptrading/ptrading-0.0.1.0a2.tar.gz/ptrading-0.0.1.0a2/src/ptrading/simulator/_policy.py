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

class ClosePolicy(ABC):
    def __init__(self, config : _Config):
        self.config = config

    @abstractmethod
    def process_bar(self, state, bar: BarList, add_order, cancel_order):
        return
