#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "info@christopherhahne.de"
__license__ = """
    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from color_matcher.hist_matcher import HistogramMatcher
from color_matcher.mvgd_matcher import TransferMVGD
from color_matcher.reinhard_matcher import ReinhardMatcher
import numpy as np

METHODS = ('default', 'mvgd', 'hm', 'hm-mkl-hm', 'reinhard')


class ColorMatcher(HistogramMatcher, TransferMVGD, ReinhardMatcher):

    def __init__(self, *args, **kwargs):
        super(ColorMatcher, self).__init__(*args, **kwargs)

        self._method = kwargs['method'] if 'method' in kwargs else 'default'

    def main(self, method: str = None) -> np.ndarray:
        """
        The main function and high-level entry point performing the mapping. Valid methods are

        :param method: ('default', 'mvgd', 'hm', 'hm-mkl-hm', 'reinhard') describing how to conduct color mapping
        :type method: :class:`str`

        :return: Resulting image after color mapping
        :rtype: np.ndarray
        """

        self._method = self._method.lower() if method is None else method.lower()

        # color transfer methods (to be iterated through)
        if self._method == METHODS[0]:
            funs = [self.transfer]
        elif self._method == METHODS[1]:
            funs = [self.transfer]
        elif self._method == METHODS[2]:
            funs = [self.hist_match]
        elif self._method == METHODS[3]:
            funs = [self.hist_match, self.transfer, self.hist_match]
        elif self._method == METHODS[4]:
            funs = [self.reinhard]
        else:
            raise BaseException('Method type \'%s\' not recognized' % method)

        # proceed with the color match
        for fun in funs:
            self._src = fun(self._src, self._ref)

        return self._src
