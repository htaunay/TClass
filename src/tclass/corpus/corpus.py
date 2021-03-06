#encoding: utf8
"""
Module containing corpus class

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

from collections import deque
from copy import deepcopy, copy
from sys import maxint
from random import randrange

from tclass.util import exception

class CorpusDocument (dict):
    """
    Class for documents apearing in the corpus.
    """
    def __init__(self, id = None):
        """
        Constructor
        
        @ivar docid: unique string id of document
        """
        self._docid = id
    
    def get_id(self):
        """
        Getter for self._docid attribute
        """
        return self._docid
    
    def _set_id(self, id):
        """
        Setter for self._docid attribute
        """
        self._docid = deepcopy(id)
        

class Corpus (object):
    """
    Class for corpus. This is an abstract class.
    """
#>------------------------------------------------------------------------------
#> Special Methods    
    
    def __init__(self, corp=None, lang="En"):
        """
        Constructor
        
        @param corp: corpus to be duplicated. (optional)
        
        @ivar _documents: deque of deques of CorpusDocuments
                            |         |           |
                         corpus     class      document
        @ivar _classes: dictionary containing two elements:
                        map := dictionary mapping name -> index
                        list := list mapping index -> name
        @ivar _lexicon: lexicon that maps words to integers (and the oposite).
                        The documents should not contain strings, instead the 
                        corresponding index of the string in the lexicon should
                        be used. This boosts performance, since comparing 
                        integers is much faster than comparing strings.
                        Contains also term-document counts for document 
                        frequency thresholding purposes.
        """
        self._documents = deque()
        self._classes = {'map':{}, 'list':[]}
        self._lexicon = {'map':{}, 'list':[], 'count':{}}
        self._size = 0
        self._lang = lang
        if corp != None:
            self._set_documents(corp.get_documents())
            self._set_classes(corp.get_classes())
            self._set_lexicon(corp.get_lexicon())
            self._size = corp.size()
                       
    def __str__(self):
        """
        String representation of a corpus
        """
        ret = ""
        for cla in range(len(self._documents)):
            if len(self._documents[cla]) > 0:
                doc_1 = str(self._documents[cla][0])
                if len(doc_1) > 30:
                    doc_1 = doc_1[:30] + '...}'
            else:
                doc_1 = "None"
            num_docs = len(self._documents[cla])
            ellipses = ""
            if num_docs > 1:
                ellipses = ", ..."
            ret += '[' + str(self._classes['list'][cla]) + ']' + \
                   " --> [" + doc_1 + ellipses +'] (' + str(num_docs) + ')\n'
        return ret
        
    def __repr__(self):
        """
        Default representation of a corpus
        """
        return self.__str__()
    
#>------------------------------------------------------------------------------
#> Getters and setters 
#> Public: getters

    def get_documents(self):
        """
        Getter for self._documents
        
        @return: self._documents
        """
        return self._documents
    
    def get_classes(self):
        """
        Getter for self._classes
        
        @return: self._classes
        """
        return self._classes
    
    def get_lexicon(self):
        """
        Getter for the self._lexicon atribute
        
        @return: the lexicon of the corpus
        """
        return self._lexicon
        
#> Protected: setters    

    def _set_documents(self, docs):
        """
        Setter for self._documents
        
        @param docs: deque of deques of dictionaries to be set
        """
        self._documents = deepcopy(docs)    
    
    def _set_classes(self, classes):
        """
        Setter for self._classes
        
        @param cl: mapping of classes and their indexes (in both directions)
        """
        self._classes =  deepcopy(classes)
    
    def _set_lexicon(self, lex):
        """
        Setter for the self._lexicon atribute
        
        @param lex: lexicon
        """
        self._lexicon = deepcopy(lex)    

#>------------------------------------------------------------------------------
#> Hotspot methods
#> Public:

    def load(self, _file, rem_stopwords = True, stem = True, merge = True):
        """
        Virtual function, loads corpus into memory.
        
        @param _file: Input file, containing corpus (or part of it)
        @param merge: boolean (default = True). If True, the input file will
                      be merged with the current state of the object.
                      If False, will erase all information stored in object
                      and will create new one.
        """
        raise NotImplementedError
       
#>------------------------------------------------------------------------------
#> Other methods
#> Public:

    def size(self):
        """
        Returns the size of the corpus, in number of documents
        """
        return self._size

    def document_frequency_thresholding(self, threshold):
        """
        Implements document frequency thresholding.
        
        @param threshold: minimum number of documents for a term to exist in the
                          corpus. (if 0 < threshold < 1, it is interpreted as 
                          relative to the total number of documents)
        """
        for term, freq in self._lexicon['count'].iteritems():
            if threshold >= 1:
                if freq < threshold:
                    self._remove_term_from_corpus(term)
            elif 0 <= threshold < 1:
                if freq < threshold * self._size:
                    self._remove_term_from_corpus(term)
                
    def remove_class(self, classname):
        """
        Removes a class from the corpus
        
        @param classname: name of the class to be removed
        """
        self._documents.remove(self._documents[self._classes['map'][classname]])
        index = self._classes['map'].pop(classname)
        for item in self._classes['map']:
            if self._classes['map'][item] > index:
                self._classes['map'][item] -= 1
        self._classes['list'].remove(classname)
               
    def insert_document(self, doc, _class = 'Unknown', lexicalize = False):
        """
        Insert one document into self._documents
        
        @param doc: CorpusDocument object already with id
        @param _class: classname, defaults to Unknown
        @param lexicalize: boolean. Lexicalize terms or not. Default is False
        """
        #If the class already exists:
        if not self._classes['map'].has_key(_class):
            self._add_class(_class)
        #if we have to lexicalize the document
        if lexicalize:
            document = CorpusDocument(doc.get_id())
            for key, value in doc.iteritems():
                document[self._add_word_to_lex(key)] = value
            doc = document
        #If the document doesn't already exist in the corpus:
        if not doc in self._documents[self._classes['map'][_class]]:
            # Doc Freq Thresholding:
            for key, value in doc.iteritems():
                self._increment_term_count(key)
            # end
            self._documents[self._classes['map'][_class]].append(doc)
            self._size += 1
            return True
        return False
    
    def clear(self):
        """
        Clears all corpus information. Resets object.
        """
        self._documents = deque()
        self._classes = {'map':{}, 'list':[]}
        self._lexicon = {'map':{}, 'list':[], 'count':{}}
        self._size = 0
        
    def partition (self, quotient):
        """
        Method that partitions a corpus object into two new corpus objects, 
        one training corpus with relative size 'quotient' and a testing corpus
        with relative size 1 - 'quotient'. 
        
        @param quotient: fraction to be used as training corpus
        @return: (train, test) corpus tuple.
        """
        #Entry assertives
        assert 0 <= quotient <= 1
        
        #Initializations
        train = Corpus()
        test = Corpus(self)
        classes = self.get_classes()
        lexicon = self.get_lexicon()
        docs = self.get_documents()
        len_docs = len(docs)
        
        #Not very pretty, but there's no other way... Unless we 'unprotect' 
        #this method, which is not wanted.
        train._set_lexicon(lexicon)
                
        #corpus size:
        i = size = 0
        while i < len_docs:
            size += len(docs[i])
            i += 1
        
        #number of training documents
        num = int(size * quotient)
        
        j = 0
        classnum = len_docs
        #also ugly, but, as above, there's no other way...
        while j < classnum:
            train._add_class(classes["list"][j])
            j += 1
        j = 0 
        to_add_list = []
        while j < num:
            doc = randrange(0, size)
            if (bin_search(doc, to_add_list) == False):
                to_add_list.append(doc)
                to_add_list.sort()
                j += 1        
        while len(to_add_list) > 0:
            doc = to_add_list.pop()
            i = 0
            while i < len_docs:
                if doc < len(docs[i]):
                    temp = copy(docs[i][doc])
                    train.insert_document(temp, classes["list"][i])
                    temp = None
                    test._remove_document(i, doc)
                    break
                else:
                    doc -= len(docs[i])
                    i += 1
        return (train, test)
        
    def lex_word(self, index):
        """
        Returns the word of the index in the lexicon.
        
        @param index: index of the word
        @return: word in the lexicon. None if there is no word with this index.
        """
        try:
            word = self._lexicon['list'][index]
            return word
        except KeyError:
            return None
    
#> Protected:

    def _remove_term_from_corpus(self, term):
        """
        Removes term from all documents and invalidates its entries in the 
        lexicon.
        
        @param term: int. lexicalized term to be removed.
        """
        for clazz in range(len(self._documents)):
            for doc in range(len(self._documents[clazz])):
                try:
                    self._documents[clazz][doc].pop(term)
                    #verify the extremely rare case when the document has no 
                    #more terms...
                    if len(self._documents[clazz][doc]) == 0:
                        self._remove_document(clazz, doc)
                except KeyError:
                    continue
        #instead of removing, invalidate entries in lexicon to be more efficient
        self._lexicon['map'][self._lexicon['list'][term]] = None
        self._lexicon['list'][term] = None
        self._lexicon['count'][term] = None

    def _increment_term_count(self, term):
        """
        Increment term count in the lexicon. Used for document frequency 
        thresholding.
        
        @param term: int. term (already lexicalized) to be incremented
        """
        try:
            self._lexicon['count'][term] += 1
        except KeyError:
            self._lexicon['count'][term] = 1

    def _add_class(self, classname):
        """
        Adds a class to the corpus
        
        @param classname: name of the new class
        """
        if not self._has_class(classname):
            self._classes['map'][classname] = len(self._classes['list'])
            self._classes['list'].append(classname)
            self._documents.append(deque())
        else:
            raise exception.TClassException("Corpus", "add_class", 
                                "Trying to add existing class to corpus.")

    def _has_class(self, name):
        """
        Tests if the class <name> already exists in the corpus
        
        @param name: name of the class
        @return: boolean
        """
        return self._classes['map'].has_key(name)
    
    def _add_word_to_lex(self, word):
        """
        Returns the index of the word in the lexicon.
        Adds word to the lexicon if not contained.
        
        @param word: word to be added
        @return: index in the lexicon
        """
        if self._lexicon["map"].has_key(word):
            return self._lexicon["map"][word]
        else:
            index = len(self._lexicon["list"])
            self._lexicon["list"].append(word)
            self._lexicon["map"][word] = index
            return index
    
    def _remove_document(self, class_index, doc_index):
        """
        Removes document from class. If class only has one document, remove
        class also.
        
        @param class_index: class index (in the self._documents vector)
        @param doc_index: document index (in the class vector)
        @return: boolean. If removal occured or not.
        """
        try:
            class_name = self._classes["list"][class_index]
        except IndexError:
            return False
        try:
            self._documents[class_index].remove(self._documents[class_index]\
                                                [doc_index])
        except ValueError:
            return False
        except IndexError:
            return False
        if len(self._documents[class_index]) == 0:
            self.remove_class(class_name)
        return True
            
#>------------------------------------------------------------------------------
#>------------------------------------------------------------------------------
#> Auxiliary functions

def bin_search(item, lista):
    """
    Boolean function that implements a binary search.
    
    @param item: item searched for
    @param list: ordered list in which the item is looked for
    
    @return: boolean. list contains item -> True, otherwise, False 
    """
    mid = int(len(lista) /2)

    if (len (lista) == 0 or ( len(lista) == 1 and lista[0] != item )) :
        return False
    elif (lista[mid] == item or ( len(lista) == 1 and lista[0] == item )) :
        return True
    elif (item < lista[mid]):
        return bin_search (item, lista[0:mid])
    elif (item > lista[mid]):
        return bin_search (item, lista[mid:len(lista)])
    return False
       
            
