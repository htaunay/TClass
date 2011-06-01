"""
Module containing Hard-margin SVM Classifier class using convex optimization
library.
This is the most straight forward implementation.

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

from math import sqrt, exp
import sys, os
from collections import deque

from cvxopt.base import matrix, spmatrix, symv
from cvxopt.solvers import qp
from cvxopt.solvers import options as solvers_options

sys.path.append(os.environ['TCLASS'])

from tclass.classifier import Classifier
from tclass.corpus import Corpus, CorpusDocument

solvers_options['show_progress'] = False

class ClassifierSvmRaw(Classifier):
    """
    Class implementing SVM hard-margin text classifier
    """
#>------------------------------------------------------------------------------
    
    def __init__(self, config = None):
        """
        Constructor
        
        @ivar _config: contains algorithm configurations 
        """
        #Default values
        if config == None:
            self._config = {"kernel":{"type":"ident", "params":[1, 2]}, \
                            "zero":1e-03}
        else:
            self._config = config
        self._model = {"alpha":None, "Dalpha":None, "b":None}
        self._support_vectors = {}
        self._sv_number = None
        
        self._true_class = None
        
#>------------------------------------------------------------------------------

    def get_support_vectors(self):
        """
        Getter for self._support_vectors
        
        @ret: dictionary of lists of support vectors for each class
        """
        return self._support_vectors

    def train(self, corpus, class_index):
        """
        Training algorithm.
        
        @param corpus: training corpus
        @param class_index: index of class in corpus considered as the 'true'
                            class
        """        
        corp = Corpus(corpus)
        self._true_class = corp.get_classes()['list'][class_index]
        ############# Creation of K matrix (kernel), D and vector y ############
        #Number of documents:
        docs = corp.get_documents()
        dim = 0
        for _class in range(len(docs)):
            dim += len(docs[_class])
        #####################
        K = matrix(0.0, size = (dim, dim))
        y = matrix(0.0, size = (1, dim))
        linha = 0
        classe1 = 0
        while classe1 < len(docs):
            documento1 = 0
            while documento1 < len(docs[classe1]):
                coluna = 0
                classe2 = 0
                while classe2 < len(docs):
                    documento2 = 0
                    while documento2 < len(docs[classe2]):
                        K[ linha, coluna ] = \
                        kernelfuncnorm(docs[classe1][documento1], \
                                       docs[classe2][documento2], \
                                       self._config["kernel"]["type"], \
                                       self._config["kernel"]["params"][0], \
                                       self._config["kernel"]["params"][1])
                        if (linha == coluna):
                            if (classe1 == class_index):
                                y[0, linha] = 1
                            else:
                                y[0, linha] = -1
                        documento2 += 1
                        coluna += 1
                    classe2 += 1
                documento1 += 1
                linha += 1
            classe1 += 1
        D = spmatrix(0, range(dim), range(dim))
        D.V = y.trans()
        ####### Hessian and auxiliary matrices #######
        Dt = D.trans()
        H = Dt*K*D
        q = matrix(-1.0, (dim, 1))
        G = spmatrix(-1.0, range(dim), range(dim))
        h = matrix(0.0, (dim, 1))
        b = matrix([0.0])
        sol = qp(H, q, G, h, y, b)
        ####### Save alpha to the model #######
        self._model["alpha"] = matrix(0.0, size = (dim, 1))
        i = 0
        while i < len(sol['x']):
            self._model["alpha"][i, 0] = sol['x'][i]
            i += 1
        ######## b ########
        i = 0
        while i < len(self._model["alpha"]):
            if self._model["alpha"][i, 0] > self._config["zero"]:
                break
            i += 1
        #######
        ysv = y[i]        
        temp = matrix (0.0, size = self._model["alpha"].size)
        symv(D, self._model["alpha"], temp)
        self._model["Dalpha"] = temp.trans()
        
        classe = 0
        flag = True
        while flag:
            if i > len(docs[classe]):
                i -= len (docs[classe])
                classe += 1
            else:
                flag = False
                
        xsv = matrix(0.0, size = (dim, 1))
        l = 0
        m = 0
        while m < len(docs):
            n = 0
            while n < len(docs[m]):
                xsv[l, 0] = kernelfuncnorm (docs[classe][i], docs[m][n], \
                                    self._config["kernel"]["type"], \
                                    self._config["kernel"]["params"][0], \
                                    self._config["kernel"]["params"][1])
                l += 1
                n += 1
            m += 1
        
        self._model["b"] = ysv - self._model["Dalpha"]*xsv

        self._sv_number = 0
        for item in range(len(self._model["alpha"])):
            if self._model['alpha'][item] > self._config["zero"]:
                i_linha = item
                classe = 0 
                while i_linha >= 0:
                    if i_linha < len(docs[classe]):
                        try:
                            self._support_vectors[classe].append(docs[classe]\
                                                               [i_linha])
                        except KeyError:
                            self._support_vectors[classe] = [docs[classe][i_linha]]
                        finally:
                            self._sv_number += 1
                            break
                    else:
                        i_linha -= len(docs[classe])
                        classe += 1
        
        #save support vectors as string vectors
#        for clazz in support_vectors:
#            for vector in range(len(support_vectors[clazz])):
#                try:
#                    self._support_vectors[clazz].append({})
#                except KeyError:
#                    self._support_vectors[clazz] = [{}]
#                for index, freq in support_vectors[clazz][vector].iteritems():
#                    self._support_vectors[clazz][vector]\
#                                         [corp.lex_word(index)] = freq
#>------------------------------------------------------------------------------
        
    def classify(self, corpus):
        """
        Classificarion algorithm.
        
        @param corpus: corpus to be classified. 
        """
        docs = corpus.get_documents()
        len_docs = len(docs)
        Dalfal = matrix ( 0.0, size = (1, self._sv_number) )
        j = 0
        i = 0
        while i < self._model["Dalpha"].size[1]:
            if self._model["alpha"][i] > self._config["zero"]:
                Dalfal[0,j] = self._model["Dalpha"][i]
                j += 1
            
            i += 1
            
        dim = 0
        i = 0
        while i < len_docs:
            dim += len(docs[i])
            i += 1

        Kl = matrix(0.0, size = (self._sv_number, dim))
                
        linha = 0
        svs = deque()
        for name, clazz in self._support_vectors.iteritems():
            for sv in clazz:
                corpus.insert_document(sv, "supportvectors" + str(name), True)
            svs.extend(corpus.get_documents()[corpus.get_classes()\
                                       ["map"]["supportvectors" + str(name)]])
                                       
        docid_matrix = {}
        for sv in svs:
            i = 0
            coluna = 0
            while i < len_docs:
                j = 0
                while j < len(docs[i]):
                    Kl[linha, coluna] = kernelfuncnorm(sv, docs[i][j], \
                                    self._config["kernel"]["type"], \
                                    self._config["kernel"]["params"][0],\
                                    self._config["kernel"]["params"][1])
                    try:
                        docid_matrix[linha][coluna] = docs[i][j].get_id()
                    except:
                        docid_matrix[linha] = {coluna:docs[i][j].get_id()}
                    coluna += 1
                    j += 1
                i += 1
            linha += 1
        
        B = matrix ( self._model['b'][0, 0], (1,dim))
        
        result = Dalfal * Kl + B
        
        #clean up
        for name, clazz in self._support_vectors.iteritems():
            corpus.remove_class("supportvectors" + str(name))
        return (result, docid_matrix)
#>------------------------------------------------------------------------------

    def clear(self):
        """
        Hotspot implementation
        """
        self._model = {"alpha":None, "Dalpha":None, "b":None}
        self._support_vectors = {}
        self._sv_number = None
#>------------------------------------------------------------------------------

    def load_model(self, model):
        """
        Hotspot implementation
        """
#>------------------------------------------------------------------------------

    def save_model(self, model):
        """
        Hotspot implementation
        """
        
        def printDalphal():
            """
            Returns the Dalpha matrix in the xml-model format
            """
            y = self._model["Dalpha"].size[1]
            ret = []
            ret.append("\t<Dalphal>\n")
            dim = 0
            for i in xrange(y):
                if self._model["alpha"][i] > self._config["zero"]:
                    ret.append("\t\t0\t%d\t%f;\n" % \
                                                (dim, self._model["Dalpha"][i]))
                    dim += 1
            ret.append("\t</Dalphal>\n")
            
            size = []
            size.append("<DalphalSize>1\t%d</DalphalSize>" % dim)
            size.extend(ret)
            return ''.join(size)
        
        def printSupportVectors():
            """
            Returns the Dalpha matrix in the xml-model format
            """
            ret = []
            for clazz in self._support_vectors.itervalues():
                for sv in clazz:
                    ret.append("\t\t<sv>\n")
                    for key, value in sv.iteritems():
                        ret.append("\t\t\t%s\t%d;\n" %(key, value))
                    ret.append("\t\t</sv>\n")
            return ''.join(ret)
            
        
        f = open(model, 'wt')
        text = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
               '<model>\n' + \
               '    <category>' + self._true_class + '</category>\n' + \
               '    <config>\n' + \
               '        <kernel>\n' + \
               '            <type>' + self._config["kernel"]["type"] + \
                                                                 '</type>\n' + \
               '            <params>\n' + \
               '                ' + str(self._config["kernel"]["params"][0]) + \
                                                                        '\n' + \
               '                ' + str(self._config["kernel"]["params"][1]) + \
                                                                        '\n' + \
               '            </params>\n' + \
               '            <zero>' + str(self._config["zero"]) + '</zero>\n' +\
               '        </kernel>\n' + \
               '    </config>\n' + \
               '    <svnumber>' + str(self._sv_number) + '</svnumber>\n' + \
               '    <b>' + str(self._model['b']) + '</b>\n' + \
               printDalphal() + \
               '    <supportVectors>\n' + \
               printSupportVectors() + \
               '    </supportVectors>\n' + \
               '</model>\n'
              
        f.write(text)
        f.close()
        
        
#>------------------------------------------------------------------------------
#>------------------------------------------------------------------------------

def kernelfunc (dic1, dic2, tipo, const, degree):
    """
    Computes the kernel between two dictionaries
    
    @param dic1: dictionary 1
    @param dic2: dictionary 2
    @param tipo: type of kernel function to be used (valid values are: 'ident',
                 'poly' and 'gaussian')
    @param const: parameter for 'poly' and 'gaussian' kernel types.
    @param degree: parameter for 'poly' kernel type.  
    """
    temp = 0
    if tipo == "ident":
        temp = innerprod (dic1, dic2)

    elif tipo == "poly":
        temp = pow((innerprod (dic1, dic2) + const), degree)

    elif tipo == "gaussian":
        tmp = dicsub (dic1, dic2)
        temp = exp(-const * innerprod(tmp, tmp))
        
    return temp
#>------------------------------------------------------------------------------

def kernelfuncnorm (dic1, dic2, tipo, const, degree):
    """
    Computes the normalized kernel between two dictionaries
    
    @param dic1: dictionary 1
    @param dic2: dictionary 2
    @param tipo: type of kernel function to be used (valid values are: 'ident',
                 'poly' and 'gaussian')
    @param const: parameter for 'poly' and 'gaussian' kernel types.
    @param degree: parameter for 'poly' kernel type.  
    """
    denom = sqrt(kernelfunc(dic1, dic1, tipo, const, degree) \
           * kernelfunc (dic2, dic2, tipo, const, degree))
    if denom > 0.:
        return kernelfunc (dic1, dic2, tipo, const, degree) / denom
    else:
        return 0
        

def innerprod (dic1, dic2):
    """
    Computes the inner product (scalar product) between two sparse vectors
    represented as Python dictionaries.
    
    @param dic1: dictionary 1
    @param dic2: dictionary 2
    """
    temp = 0
    if len(dic1) > len(dic2):
        dic1, dic2 = dic2, dic1
    for word in dic1:
        if dic2.has_key(word):
            temp += dic2[word] * dic1[word]
#        try:
#            temp += dic2[word] * dic1[word]
#        except KeyError:
#            continue

    return temp

def dicsub (dic1, dic2):
    """
    Computes the vector subtraction dic1 - dic2 for sparse vectors represented 
    as Python dictionaries.
    
    @param dic1: dictionary 1
    @param dic2: dictionary 2
    """
    temp = {}
    for word in dic1:
        temp[word] = dic1[word]

    for word in dic2:
        try:
            temp[word] = temp[word] - dic2[word]
        except KeyError:
            temp[word] = - dic2[word]

    return temp
        
#if __name__ == "__main__":
##    from tclass.corpus.dir.txt import CorpusDirTxt
#    from tclass.corpus.dir.xmlreuters import CorpusDirXmlReuters
#    import os
##    _corpus = CorpusDirTxt()
#    _corpus = CorpusDirXmlReuters()
##    _corpus.load(os.path.join(os.environ["TCLASS"],'tests', 'corpora', \
##                           'corpus2'))
#    _corpus.load(os.path.join(os.environ["TCLASS"],'tests', 'corpora', \
#                              'reuters_subset'))
#    print _corpus.get_classes()
#    cl = ClassifierSvmRaw()
#    _class_corp = CorpusDirXmlReuters()
#    _class_corp.load(os.path.join(os.environ["TCLASS"],'tests', 'corpora', \
#                              'reuters', 'money-fx'))
#    print "training:\n", cl.train(_corpus, _corpus.get_classes()["map"]\
#                                                                [raw_input()])
#    print "classification:\n",cl.classify(_class_corp)