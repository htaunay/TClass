#encoding: utf8
"""
Pyunit Test module for the Tokenizer class
"""
import unittest
import sys
import os.path
import os
import codecs

from tclass.util.tokenizer import Tokenizer

sys.path.append(os.environ["TCLASS"])

class TestTokenizer(unittest.TestCase):
    """
    Unit test class for the Tokenizer Class
    """
    
    def test_tokenize(self):
        """
        Tests the tokenization
        """
        _file = codecs.open(os.path.join(os.environ["TCLASS"], "tests", \
                       "corpora", "corpus1/", "economy", "e1.txt"), 'r', "utf8")
        text = _file.read()
        text = text.split()
        tokens = []
        tok = Tokenizer()     
        for word in text:
            tokens.extend(tok.fineTokenization(word))
        saida = eval(codecs.open(os.path.join(os.environ["TCLASS"], "tests", \
                           "tclass", "tokenizer", "saida"), 'r', "utf8").read())
                           
        print saida, tokens
                           
        assert(saida == tokens)
        
tt = TestTokenizer()
tt.test_tokenize()
