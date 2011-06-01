#encoding: utf8
"""
Implementation of CorpusDir abstract class

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

from os.path import sep
from os.path import isdir, walk
from sys import maxint
from time import time

from tclass.corpus import Corpus
from tclass.util import exception

class CorpusDir (Corpus):
    """
    Abstract class for corpora in tree directory structure.
    """    
    _suffix = None
    _file_number = 0
    _repeated_files= 0

    def load(self, _file, rem_stopwords = True, stem = True, \
    								merge = True, level = maxint):
        """
        Abstract method implementation for directory trees
        """
        start = time()
        
        if not isdir(_file):
            raise exception.TClassException("CorpusDirTxt", "load", 
                                "Path provided is not a directory. " + _file)
        if merge == False:
            self.clear()
        walk(_file, self.__load, (rem_stopwords, stem, level))        
        duration = time() - start
        print "Loaded %d documents in %0.2f seconds. (%0.0f docs/s)" \
              % (self._file_number, duration, (self._file_number / duration))
        self._file_number = 0
        if self._repeated_files != 0:
            print "%d repeated files were found. They were added only once." % \
              (self._repeated_files)
            self._repeated_files = 0
        
    def __load(self, (rem_stopwords, stem, level), dirname, names):
        """
        Function passed to the walk method.  
        """
        dir_name = dirname.split(sep)
        classname = ""
        #Build class name
        for i in range(len(dir_name)):
            classname += dir_name[i] + sep
            if i >= level:
                break
        #print classname
        #Add class if it is not part of the corpus yet
        if not self._has_class(classname):
            self._add_class(classname)
        flag = False
        for _file in names:
            if not isdir(dirname + sep + _file) and \
                                                _file.endswith(self._suffix):
                flag = True
                self._load_file(dirname + sep + _file, classname, \
                							rem_stopwords, stem)
        if not flag:
            if len(self._documents[self._classes['map'][classname]]) == 0:
                self.remove_class(classname)      
                
    def normalize_classnames(self):
        """
        Normalizes classnames to remove common superpaths
        """
        classes = self.get_classes()
        start = common = classes["list"][0]
        for _class in classes["map"].iterkeys():
            if len(_class) < len(common):
                for i in range(len(_class)):
                    if _class[i] != common[i]:
                        common = _class[:i]
                        break
            else:
                for i in range(len(common)):
                    if common[i] != _class[i]:
                        common = _class[:i]
                        break
        # For the case where a class is the superpath of other classes
        if common == start:
            common = common.split(sep)[-1]
        new_classes = {"map":{}, "list":[]}
        for value in range(len(classes["list"])):
            new_classes["map"][classes["list"][value].replace(common, \
                                     '')] = value
            new_classes["list"].append(classes["list"] \
                                    [value].replace(common, ''))
        self._set_classes(new_classes)
        
    def _load_file(self, _file, _class):
        """
        Abstract method that opens file, tokenizes it and adds it to the corpus
        """
        raise NotImplementedError
