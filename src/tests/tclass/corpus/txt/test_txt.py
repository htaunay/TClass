#encoding: utf8
"""
Pyunit Test module for the CorpusTxt class
"""
import unittest
import sys
import os
import os.path
from collections import deque

from tclass.corpus.txt import CorpusTxt

sys.path.append(os.environ['TCLASS'])

class TestCorpusTxt(unittest.TestCase):
    """
    Unit test class for the Txt Class
    """
    
    def test_tokenize(self):
        """
        Tests the loading of a corpus 
        """
        import os
        print os.environ['PWD']
        corpus = CorpusTxt()
        corpus.load(os.path.join(os.environ["TCLASS"], \
                            "tests", "corpora", "corpus1", "economy", "e1.txt"))
        documents = eval(open(os.path.join(os.environ["TCLASS"], "tests", \
                        "tclass", "corpus", "txt", "documents"), 'r').read())
        classes = {'map': {'Unknown': 0}, 'list': ['Unknown']}
        
        assert (documents == corpus.get_documents())
        assert (classes == corpus.get_classes())
