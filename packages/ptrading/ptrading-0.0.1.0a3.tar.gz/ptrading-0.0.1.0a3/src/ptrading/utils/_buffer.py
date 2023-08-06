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

class CircularBuffer:
    def __init__(self, buffer_size: int):
        self.buffer_size = buffer_size
        self.array = []

    def add(self, element):
        if len(self.array) < self.buffer_size:
            self.array.append(element)
        else:
            del self.array[0]
            self.array.append(element)

    def ready(self) -> bool:
        return len(self.array) == self.buffer_size

    def get(self) -> list:
        return self.array