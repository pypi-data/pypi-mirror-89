# coding:utf8
# @Time : 2020/12/26 1:19 下午 
# @Author : vic

import unittest

from vic_pkg.hello import Hello


class TestHello(unittest.TestCase):

    def test_get(self):
        Hello().get()
