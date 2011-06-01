#encoding: utf8
"""
Pyunit Test module for the CorpusTxt class
"""
import unittest
import sys
import os
from collections import deque

from tclass.corpus.dir.txt import CorpusDirTxt

sys.path.append(os.environ['TCLASS'])

class TestCorpusDirTxt(unittest.TestCase):
    def test_load (self):
        corp = CorpusDirTxt()
        corp.load(os.path.join(os.environ['TCLASS'], "tests", "corpora", \
                               "corpus1"))
        corp.normalize_classnames()
        assert corp.get_classes() == {'map': {'sports/tennis/': 0, \
                                              'economy/stocks/': 3, \
                                              'sports/football/': 1, \
                                              'economy/': 2 } , \
                                      'list': ['sports/tennis/', \
                                               'sports/football/', \
                                               'economy/', \
                                               'economy/stocks/']\
                                      }
        assert corp.get_documents()[0] == \
        deque([{0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 6, 8: 1, \
                9: 1, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, \
                17: 2, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 2, \
                25: 4, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, \
                33: 2, 34: 1, 35: 5, 36: 1, 37: 1, 38: 1, 39: 5, 40: 1, \
                41: 1, 42: 1, 43: 1, 44: 1, 45: 5, 46: 1, 47: 1, 48: 1, \
                49: 1, 50: 1, 51: 1, 52: 1, 53: 1, 54: 1, 55: 1, 56: 1, \
                57: 1, 58: 2, 59: 2, 60: 1, 61: 2, 62: 1, 63: 5, 64: 1, \
                65: 2, 66: 1, 67: 1, 68: 1, 69: 1, 70: 1, 71: 1, 72: 1, \
                73: 1, 74: 2, 75: 6, 76: 1, 77: 3, 78: 3, 79: 2, 80: 1, \
                81: 1, 82: 1, 83: 2, 84: 7, 85: 1, 86: 1, 87: 1, 88: 1, \
                89: 1, 90: 2, 91: 1, 92: 3, 93: 1, 94: 11, 95: 1, 96: 2,\
                97: 1, 98: 1, 99: 2, 100: 1}])