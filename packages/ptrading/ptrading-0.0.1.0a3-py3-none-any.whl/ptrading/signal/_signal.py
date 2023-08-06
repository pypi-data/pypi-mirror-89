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
from ..utils import CircularBuffer as _CircularBuffer

from typing import Dict as _Dict

class SignalBase(ABC):
	def __init__(self, ticker: str, buffer_size: int = 1000):
		super().__init__()
		self.ticker = ticker
		self.buffer_size = buffer_size
		self.buffer = _CircularBuffer(buffer_size)

	def ready(self):
		return self.buffer.ready()

	def process_bar(self, bar) -> float:
		assert bar.ticker == self.ticker
		return self.process_bar_wrapper(bar)

	@abstractmethod
	def process_bar_wrapper(self, bar) -> float:
		return
