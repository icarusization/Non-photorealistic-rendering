#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import saliency_map_test
import utils_test


def suite():
    # all tests
    suite = unittest.TestSuite()
    suite.addTests(saliency_map_test.suite())
    suite.addTests(utils_test.suite())
    return suite
