#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import itertools
from saliency_map import *
from utils import OpencvIo


class GaussianPyramidTest(unittest.TestCase):
    def setUp(self):
        oi = OpencvIo()
        src = oi.imread('./images/fruit.jpg')
        self.__gp = GaussianPyramid(src)

    def test_get_intensity(self):
        its = self.__gp._GaussianPyramid__get_intensity(10, 20, 30)
        self.assertEqual(20, its)
        self.assertNotEqual(type(1), type(its))

    def test_get_colors(self):
        real = self.__gp._GaussianPyramid__get_colors(0.9, 0.9, 0.9, 0.9, 10)
        self.assertEqual([0.0, 0.0, 0.0, 0.0], real)


class FeatureMapTest(unittest.TestCase):
    def setUp(self):
        oi = OpencvIo()
        src = oi.imread('./images/fruit.jpg')
        gp = GaussianPyramid(src)
        self.__fm = FeatureMap(gp.maps)

    def test_scale_diff(self):
        c, s = np.zeros((4, 6)), np.zeros((2, 3))
        expect = np.ones((4, 6))
        for y, x in itertools.product(xrange(len(s)), xrange(len(s[0]))):
            s[y][x] = (-1) ** x
        self.assertTrue(np.array_equal(expect, self.__fm._FeatureMap__scale_diff(c, s)))

    def test_scale_color_diff(self):
        c1, s1 = np.zeros((4, 6)), np.zeros((2, 3))
        c2, s2 = np.zeros((4, 6)), np.zeros((2, 3))
        expect = np.ones((4, 6))
        for y, x in itertools.product(xrange(len(s1)), xrange(len(s1[0]))):
            s1[y][x] = (-1) ** x
        real = self.__fm._FeatureMap__scale_color_diff((c1, s1), (c2, s2))
        self.assertTrue(np.array_equal(expect, real))


class ConspicuityMapTest(unittest.TestCase):
    def setUp(self):
        oi = OpencvIo()
        src = oi.imread('./images/fruit.jpg')
        gp = GaussianPyramid(src)
        fm = FeatureMap(gp.maps)
        self.__cm = ConspicuityMap(fm.maps)

    def test_scale_add(self):
        srcs = [np.ones((4, 6)), np.zeros((2, 3))]
        expect = np.ones((4, 6))
        self.assertTrue(np.array_equal(expect, self.__cm._ConspicuityMap__scale_add(srcs)))


class SaliencyMapTest(unittest.TestCase):
    def setUp(self):
        self.sm = SaliencyMap()


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(GaussianPyramidTest))
    suite.addTests(unittest.makeSuite(FeatureMapTest))
    suite.addTests(unittest.makeSuite(ConspicuityMapTest))
    suite.addTests(unittest.makeSuite(SaliencyMapTest))
    return suite
