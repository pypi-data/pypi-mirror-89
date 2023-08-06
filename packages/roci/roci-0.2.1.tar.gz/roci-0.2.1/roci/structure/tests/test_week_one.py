#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:58:55 2020

@author: andrewblance
"""

import src.day01 as d1


class TestDayOne:
    def test_two_factors(self):
        L = [1, 5, 20000, 1009, 1011, 2]
        factors = d1.DayOne().find_two_factors(L)
        assert factors == 1020099

    def test_three_factors(self):
        L = [1, 5, 20000, 1009, 1010]
        factors = d1.DayOne().find_three_factors(L)
        assert factors == 1019090
