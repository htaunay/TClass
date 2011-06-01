#encoding: utf8
"""

@author: Thuener Armando da Silva
@contact: thuener@gmail.com
"""

from xml.dom.minidom import parse, parseString
import os

from tclass.corpus.dir import CorpusDir
from tclass.corpus import CorpusDocument

from tclass.util.tokenizer import Tokenizer
from tclass.util.stemmer import RSLP
from tclass.util.stemmer import PorterStemmer
   

class CorpusDirXmlCineplayers (CorpusDir):
    """
    This class implements the interface defined in CorpusDir for files in the 
    Cineplayers xml corpus.
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
        dom = parse(_file)
        filhos = dom.childNodes[0].childNodes
        
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
        i = 3
        while i < (len( filhos )- 1):
            body_data = filhos[i].getElementsByTagName("Resenha")[0].childNodes[0].data
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
            #document is a CorpusDocument object. The docid is the path to the file
            #(_file).
            document = CorpusDocument(filhos[i].getAttribute('id'))
            
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
            i += 2
        
if __name__ == "__main__":
    CORP =  CorpusDirXmlCineplayers()
    CORP.load(os.path.join(os.environ['TCLASS'], "tests", "reuters"))
