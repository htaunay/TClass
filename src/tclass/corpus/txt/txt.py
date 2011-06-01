#encoding: utf8
"""
Implementation of corpus subclass for txt files

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.coms
"""

# global dependencies
import os

# local dependecies
from tclass.corpus import Corpus
from tclass.corpus import CorpusDocument
from tclass.util.tokenizer import Tokenizer
from tclass.util.stemmer import RSLP
from tclass.util.stemmer import PorterStemmer

class CorpusTxt (Corpus):
    """
    This class implements the interface defined in Corpus for files in txt
    format
    """
    def load(self, _file, rem_stopwords = True, stem=True, merge = True, \
             class_name = None):
        """
        Abstract method implementation for the txt format
        """
        in_file = open(_file, 'r')
        text = in_file.read()
        in_file.close()     
        text = text.split()        
        tokens = []        
       	tok = Tokenizer()
        
	    ##############Stopword removal############################
        stopwordFile = "stopwords" + self._lang                     
        f = open(os.path.join(os.environ['TCLASS'], "tclass", "corpus", stopwordFile), 'rt')
        stopwords = f.read()
        f.close()
        stopwords = stopwords.split()
	    ##########################################################

        #################Stem setup###############################
        stemmer = None
        if stem:

            if self._lang == 'Pt':
                stemmer = RSLP()
            elif self._lang == 'En':
	            stemmer = PorterStemmer()
        ##########################################################
        
        for word in text:
            tokens.extend(tok.fineTokenization(word))            
        token_dict = {}        
        for token in tokens:
            try:
                token_dict[token.lower()] += 1
            except KeyError:
                token_dict[token.lower()] = 1    
        document = CorpusDocument(_file)
        for key, value in token_dict.iteritems():
            if not (rem_stopwords and key in stopwords):
            
                if stemmer != None:
                    key = stemmer.stem(key)
                
                if key != None:
                	document[self._add_word_to_lex(key)] = value
                    
        if not merge:
            self.clear()
            self.insert_document(document, class_name)
        else:
            self.insert_document(document, class_name)
