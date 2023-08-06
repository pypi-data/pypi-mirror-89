#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>

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

from color_matcher.top_level import ColorMatcher, METHODS
from color_matcher.io_handler import *
from color_matcher.bin.cli import main

import unittest
import os, sys
import numpy as np
from ddt import ddt, idata, unpack
try:
    import imageio
except ImportError:
    pass


@ddt
class MatchMethodTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MatchMethodTester, self).__init__(*args, **kwargs)

    def setUp(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')

    @staticmethod
    def avg_hist_dist(img1, img2, bins=2**8-1):

        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]

        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    @idata(([m] for m in METHODS))
    @unpack
    def test_match_method(self, method=None, save=False):

        # skip if no method present
        if method is None:
            self.skipTest('Type \'None\' was passed and skipped')

        # load images
        plain = load_img_file(os.path.join(self.dat_path, 'scotland_plain.png'))
        house = load_img_file(os.path.join(self.dat_path, 'scotland_house.png'))
        refer = load_img_file(os.path.join(self.dat_path, 'scotland_pitie.png'))

        # create color match object
        match = ColorMatcher(src=house, ref=plain, method=method).main()

        # assess quality
        refer_val = self.avg_hist_dist(plain, refer)
        match_val = self.avg_hist_dist(plain, match)
        print('\nAvg. histogram distance of original %s vs. %s %s' % (round(refer_val, 3), method, round(match_val, 3)))

        # assertion
        self.assertEqual(True, refer_val > match_val)

        # write images to tests data directory (if option set)
        if save:
            save_img_file(match, file_path=os.path.join(self.dat_path, 'scotland_'+method), file_type='png')

    @unittest.skipUnless('imageio' in sys.modules, "requires imageio")
    def test_match_method_imageio(self):

        # get tests data from imageio lib
        fn_img1 = 'chelsea'
        fn_img2 = 'astronaut'
        img1 = imageio.imread('imageio:'+fn_img1+'.png')
        img2 = imageio.imread('imageio:'+fn_img2+'.png')

        # create color match object (without using keyword arguments)
        match = ColorMatcher(img1, img2).main()

        # assess quality
        refer_val = self.avg_hist_dist(img1, img2)
        match_val = self.avg_hist_dist(img1, match)
        print('\nAvg. histogram distance of original %s vs. %s' % (round(refer_val, 3), round(match_val, 3)))

        # save result
        output_filename = os.path.join(self.dat_path, fn_img1.split('.')[0] + '_from_' + fn_img2)
        save_img_file(img1, file_path=os.path.join(self.dat_path, fn_img1))
        save_img_file(img2, file_path=os.path.join(self.dat_path, fn_img2))
        save_img_file(match, file_path=output_filename)

        # assertion
        self.assertEqual(True, refer_val > match_val)

    @idata(([kw] for kw in ['-h', '--help']))
    @unpack
    def test_cli_help(self, kw):

        # print help message
        sys.argv.append(kw)
        try:
            ret = main()
        except SystemExit:
            ret = True

        self.assertEqual(True, ret)

    @idata(([kw] for kw in [['-s ', '-r '], ['--src=', '--ref=']]))
    @unpack
    def test_cli_args(self, kw):

        # compose cli arguments
        sys.argv.append(kw[0] + os.path.join(self.dat_path, 'scotland_house.png'))
        sys.argv.append(kw[1] + os.path.join(self.dat_path, 'scotland_plain.png'))

        # run cli command
        ret = main()

        # assertion
        self.assertEqual(True, ret)

    @idata(([kw] for kw in [['-s ', '-r '], ['--src=', '--ref=']]))
    @unpack
    def test_batch_process(self, kw):

        # compose cli arguments
        sys.argv.append(kw[0] + self.dat_path)                                        # pass directory path
        sys.argv.append(kw[1] + os.path.join(self.dat_path, 'scotland_plain.png'))    # pass file path

        # run cli command
        ret = main()

        # assertion
        self.assertEqual(True, ret)


if __name__ == '__main__':
    unittest.main()
