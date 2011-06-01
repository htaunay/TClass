#encoding: utf8
"""
Implementation of CorpusDir subclass for txt files

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import os

from tclass.corpus.dir import CorpusDir
from tclass.corpus import CorpusDocument

from tclass.util.tokenizer import Tokenizer
from tclass.util.stemmer import RSLP
from tclass.util.stemmer import PorterStemmer

class ReutersHandler(ContentHandler):
    """
    Implements a sax handler for Reuters corpus XML tags. 
    """
    def __init__(self, tag):
        self.__inLABEL = 0
        self.__numOfLABEL = 0
        self.__buffer = ""
        self.LABEL = []
        self.__tag = tag
        
    def startElement(self, name, attributes):
        if name == self.__tag:
            self.__inLABEL = 1
            self.__numOfLABEL = self.__numOfLABEL + 1
 
    def characters(self, data):
        if self.__inLABEL:
            self.__buffer += data
   
    def endElement(self, name):
        if name == self.__tag:
            self.__inLABEL = 0
            self.LABEL.append(self.__buffer)
            self.__buffer = ""

class CorpusDirXmlReuters (CorpusDir):
    """
    This class implements the interface defined in CorpusDir for files in the 
    Reuters-21578 xml corpus.
    """    
    _suffix = ".xml"

    def _load_file(self, _file, _class, rem_stopwords, stem):
        """
        Implementation of method that opens file, tokenizes it and adds it to
        the corpus.
        
        @param _file: file to be loaded
        @param _class: class of the file
        """
        #initialization
        handlerbody = ReutersHandler("BODY")
        parserbody = make_parser()
        parserbody.setContentHandler(handlerbody)
        parserbody.parse(_file)
        
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
        
        body_data = "" 
        for i in range(len(handlerbody.LABEL)):
            body_data = str(handlerbody.LABEL[i])
            text = body_data.split()        
            tokens = []        
            tok = Tokenizer()        
            for word in text:
                tokens.extend(tok.fineTokenization(word))            
            token_dict = {}
            for token in tokens:
                try:
                    token_dict[token.lower()] += 1
                except KeyError:
                    token_dict[token.lower()] = 1
            #document is a CorpusDocument object. The docid is the path to the
            #file (_file).
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
            body_data = ""
        
if __name__ == "__main__":
    CORP =  CorpusDirXmlReuters()
    CORP.load(os.path.join(os.environ['TCLASS'], "tests", "reuters"))
