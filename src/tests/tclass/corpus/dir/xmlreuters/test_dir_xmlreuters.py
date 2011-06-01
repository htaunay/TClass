#encoding: utf8
"""
Pyunit Test module for the CorpusTxt class
"""
import unittest
import sys
import os
from collections import deque

from tclass.corpus.dir.xmlreuters import CorpusDirXmlReuters

sys.path.append(os.environ['TCLASS'])

class TestCorpusDirxmlReuters(unittest.TestCase):
    def test_load (self):
        corp = CorpusDirXmlReuters()
        corp.load(os.path.join(os.environ['TCLASS'], "tests", "corpora", \
                               "reuters"))
        corp.normalize_classnames()
        for item in corp.get_classes()['map']:
            assert item in \
            {'money-supply/': 2, 'coffee/': 7, 'money-fxinterest/': 8, \
             'gnp/': 11, 'grainwheat/': 9, 'money-fx/': 1, 'gold/': 6, \
             'ship/': 0, 'acq/': 10, 'cocoa/': 12, 'sugar/': 13, 'earn/': 3, \
             'interest/': 5, 'trade/': 14, 'crude/': 4}
        assert corp.get_documents()[0][0] == \
        {0: 1, 1: 1, 2: 1, 3: 5, 4: 1, 5: 4, 6: 1, 7: 1, 8: 2, 9: 1, 10: 1, \
         11: 1, 12: 1, 13: 1, 14: 2, 15: 1, 16: 2, 17: 1, 18: 3, 19: 2, 20: 1, \
         21: 1, 22: 1, 23: 2, 24: 2, 25: 2, 26: 1, 27: 1, 28: 2, 29: 1, 30: 1, \
         31: 5, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 2, 39: 1, 40: 2, \
         41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 1, 48: 1, 49: 2, 50: 1, \
         51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 3, 60: 1, \
         61: 2, 62: 1}
        