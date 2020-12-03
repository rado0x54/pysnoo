# -*- coding: utf-8 -*-
"""Dummy test class."""
import unittest
from pysnoo import simple


class Simple(unittest.TestCase):
    """Simple Test class"""

    def test_add(self):
        """Dummy test class"""
        self.assertEqual(3, simple.add(1, 2))
        self.assertEqual(3, simple.add(2, 1))
        self.assertEqual(3, simple.add(1, 2.0))
