#encoding: utf8
"""
Implementation of CorpusDir subclass for txt files

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""
import os

from tclass.corpus.dir import CorpusDir
from tclass.corpus import CorpusDocument

from tclass.util.tokenizer import Tokenizer
from tclass.util.stemmer import RSLP
from tclass.util.stemmer import PorterStemmer

class CorpusDirTxt (CorpusDir):
    """
    This class implements the interface defined in CorpusDir for files in txt
    format.
    """    
    _suffix = ".txt"

    def _load_file(self, _file, _class, rem_stopwords, stem):
        """
        Implementation of method that opens file, tokenizes it and adds it to
        the corpus.
        """
        #print _file, _class
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
        #document is a CorpusDocument object. The docid is the path to the file
        #(_file).
        document = CorpusDocument(_file)
        for key, value in token_dict.iteritems():
            if not (rem_stopwords and key in stopwords):
            
                if stemmer != None:
                    key = stemmer.stem(key)
                
                if key != None:
                	document[self._add_word_to_lex(key)] = value
                
        if self.insert_document(document, _class):
            self._file_number += 1
        else:
            self._repeated_files += 1
                    
                    
