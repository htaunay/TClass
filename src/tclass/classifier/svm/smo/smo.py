"""
Module containing SMO SVM Classifier class that implemets an SVM based on
Platt's sequential minimal optimization algorithm.

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

from math import exp, sqrt
from random import random
from collections import deque

from tclass.classifier import Classifier
from tclass.corpus import Corpus

class ClassifierSmoSvm(Classifier):
    """
    This class implements Platt's SMO SVM classifier.
    """
    def __init__(self, config = None):
        """
        Constructor
        
        @ivar _config: contains algorithm configurations 
        """
        if config == None:
            self._config = {"kernel":{"type":None, "params":None}, \
                            "tolerance":None, \
                            "C":None}
        else:
            self._config = config
        self._model = {"alpha":None, "b":None}
        self._support_vectors = []
        ### Caches
        #maintains a cache of alphas that are not at the bounds
        self._cache_alpha = []
        #maintains a cache of errors
        self._cache_error = {}
        
    def train(self, corpus, class_index):
        """
        Hotspot implementation. Based on pseudo-code presented by Platt.
        """
        ### training structures
        #training corpus
        corp = Corpus(corpus).get_documents()
        #alpha contains the Lagrange multipliers for each training document
        self._model["alpha"] = []
        #threshold of the SMO (the b parameter in the equation)
        self._model['b'] = 0
        #mapping of documents to indexes
        _map = {"class":{}, "index":[]}
        
        ### initialization of structures
        size = 0
        for _class in range(len(corp)):
            _map["class"][_class] = range(size, size + len(corp[_class]))
            _map["index"].extend([(_class, i) for i in \
                                  range(len(corp[_class]))])
            size += len(corp[_class])
            #initializes all alpha to 0
            self._model["alpha"].extend([0 for i in range(len(corp[_class]))])
        
        ### auxiliary functions
        def class_of(index):
            """
            Returns tuple (class, document index) in the corpus of document 
            with index 'index' 
            """
            return _map["index"][index]
        
        def target(doc):
            """
            Returns -1 ou +1, depending on doc's class
            """
            _class, ind = class_of(doc)
            if _class == class_index:
                return 1
            else:
                return -1
            
        def svm_output(doc):
            """
            Classifies doc using current model
            """
            res = 0
            class_k, doc_k = class_of(doc)
            for i in range(size):
                if self._model["alpha"][i] > 0:
                    class_i, doc_i = class_of(i)
                    res += self._model["alpha"][i] * target(i) * \
                    kernelfuncnorm(corp[class_i][doc_i], corp[class_k][doc_k], \
                                   self._config["kernel"]["type"], \
                                   self._config["kernel"]["params"][0], \
                                   self._config["kernel"]["params"][1])
            return res - self._model['b']
        
        def compute_L_H(doc_1, doc_2):
            """
            Computes L and H values for doc_1 and doc_2 (please refer to 
            Platt's paper)
            """
            if target(doc_1) != target(doc_2):
                delta = self._model["alpha"][doc_2] - \
                        self._model["alpha"][doc_1]
                if delta > 0:
                    L = delta
                    H = self._config['C']
                else:
                    L = 0
                    H = self._config['C'] + delta
            else:
                delta = self._model["alpha"][doc_2] + \
                        self._model["alpha"][doc_1]
                if delta > self._config['C']:
                    L = delta - self._config['C']
                    H = self._config['C']
                else:
                    L = 0
                    H = delta
            return L, H 
        
        def take_step(doc_1, doc_2):
            """
            Optimizes two Lagrange mulitpliers
            """
            if doc_1 == doc_2: 
                return False
#            try :
#                error_1 = self._cache_error[doc_1]
#            except KeyError:
#                error_1 = svm_output(doc_1) - target(doc_1)
            error_1 = svm_output(doc_1) - target(doc_1)
#            try:
#                error_2 = self._cache_error[doc_2]
#            except KeyError:
#                error_2 = svm_output(doc_2) - target(doc_2)
            error_2 = svm_output(doc_2) - target(doc_2)
            s = target(doc_1) * target(doc_2)
            #computation of L an H
            L, H = compute_L_H(doc_1, doc_2)
            if L == H:
                return False
            class_1, doc_1 = class_of(doc_1)
            class_2, doc_2 = class_of(doc_2)
            k11 = kernelfuncnorm(corp[class_1][doc_1], corp[class_1][doc_1], \
                                 self._config["kernel"]["type"], \
                                 self._config["kernel"]["params"][0], \
                                 self._config["kernel"]["params"][1])
            k12 = kernelfuncnorm(corp[class_1][doc_1], corp[class_2][doc_2], \
                                 self._config["kernel"]["type"], \
                                 self._config["kernel"]["params"][0], \
                                 self._config["kernel"]["params"][1])
            k22 = kernelfuncnorm(corp[class_2][doc_2], corp[class_2][doc_2], \
                                 self._config["kernel"]["type"], \
                                 self._config["kernel"]["params"][0], \
                                 self._config["kernel"]["params"][1])
            eta = k11 + k22 - 2 * k12
            if eta > 0:
                new_alpha_2 = self._model["alpha"][doc_2] + \
                              target(doc_2) * (error_1 - error_2) / eta
                if new_alpha_2 < L:
                    new_alpha_2 = L
                elif new_alpha_2 > H:
                    new_alpha_2 = H
            else:
                f_1 = target(doc_1) * (error_1 + self._model['b']) - \
                      self._model["alpha"][doc_1] * k11 - s * \
                      self._model["alpha"][doc_2] * k12
                f_2 = target(doc_2) * (error_2 + self._model['b']) - s * \
                      self._model["alpha"][doc_1] * k12 - \
                      self._model["alpha"][doc_2] * k22
                L_1 = self._model["alpha"][doc_1] + s * \
                      (self._model["alpha"][doc_2] - L)
                H_1 = self._model["alpha"][doc_1] + s * \
                      (self._model["alpha"][doc_2] - H)
                Lobj = L_1 * f_1 + L * f_2 + 1/2 * L_1**2 * k11 + 1/2 * \
                       L**2 * k22 + s * L * L_1 * k12
                Hobj = H_1 * f_1 + H * f_2 + 1/2 * H_1**2 * k11 + 1/2 * \
                       H**2 * k22 + s * H * H_1 * k12
                if Lobj < Hobj - self._config["tolerance"]:
                    new_alpha_2 = L
                elif Lobj > Hobj + self._config["tolerance"]:
                    new_alpha_2 = H
                else:
                    new_alpha_2 = self._model["alpha"][doc_2]
            if abs(new_alpha_2 - self._model["alpha"][doc_2]) < \
               self._config["tolerance"] * (new_alpha_2 + \
                                            self._model["alpha"][doc_2] + \
               self._config["tolerance"]):
                return False
            new_alpha_1 = self._model["alpha"][doc_1] + s * \
                          (self._model["alpha"][doc_2] - new_alpha_2)
            #Updating the threshold
            b_1 = b_2 = None
            if L < new_alpha_1 < H:
                b_1 = error_1 + target(doc_1) * (new_alpha_1 - \
                      self._model["alpha"][doc_1]) * k11 + target(doc_2) * \
                      (new_alpha_2 - self._model["alpha"][doc_2]) * k12 + \
                      self._model['b']
            elif L < new_alpha_2 < H:
                b_2 = error_2 + target(doc_1) * (new_alpha_1 - \
                      self._model["alpha"][doc_1]) * k12 + target(doc_2) * \
                      (new_alpha_2 - self._model["alpha"][doc_2]) * k22 + \
                      self._model['b']
            else:
                b_1 = error_1 + target(doc_1) * (new_alpha_1 - \
                      self._model["alpha"][doc_1]) * k11 + target(doc_2) * \
                      (new_alpha_2 - self._model["alpha"][doc_2]) * k12 + \
                      self._model['b']
                b_2 = error_2 + target(doc_1) * (new_alpha_1 - \
                      self._model["alpha"][doc_1]) * k12 + target(doc_2) * \
                      (new_alpha_2 - self._model["alpha"][doc_2]) * k22 + \
                      self._model['b']
            if not b_1:
                if not b_2:
                    self._model['b'] = (b_1 + b_2)/2
                else:
                    self._model['b'] = b_2
            else:
                self._model['b'] = b_1
            #updating alphas
            self._model["alpha"][doc_1] = new_alpha_1
            self._model["alpha"][doc_2] = new_alpha_2
            try:
                self._cache_alpha.remove(doc_1)
            except ValueError:
                pass
            try:
                self._cache_alpha.remove(doc_2)
            except ValueError:
                pass
            if 0 < new_alpha_1 < self._config['C']:
                self._cache_alpha.insert(0, doc_1)
                self._cache_error[doc_1] = error_1
            if 0 < new_alpha_2 < self._config['C']:
                self._cache_alpha.insert(0, doc_2)
                self._cache_error[doc_2] = error_2
            return True
        
        def examine_example(doc):
            """
            Given doc, checks if it's corresponding Lagrange multiplier 
            violates the KKT conditions by more than self._config["tolerance"].
            If yes, it looks for a second document and calls take_step to
            jointly optimize the Lagrange multipliers. 
            """
            y_2 = target(doc)
            error_2 = svm_output(doc) - target(doc)
            R_2 = error_2 * y_2
            #Test if doc violates KKT conditions
            if (R_2 < -self._config["tolerance"] and \
                self._model["alpha"][doc] < self._config["C"]) or \
               (R_2 > self._config["tolerance"] and \
                self._model["alpha"][doc] > 0):
                #look in unbounded set:
                if len(self._cache_alpha) > 1:
                    #try |E2 - E1|
                    e_max = 0
                    i_1 = -1
                    for i in self._cache_alpha:
#                        try:
#                            error_1 = self._cache_error[i]
#                        except KeyError:
#                            error_1 = svm_output(i) - target(i)
                        error_1 = svm_output(i) - target(i)
                        temp = abs(error_2 - error_1)
                        if temp > e_max:
                            e_max = temp
                            i_1 = i
                    if take_step(i_1, doc):
                        return True
                    #if this did not help, iterate over all unbounded alphas
                    rand = int(random() * len(self._cache_alpha))
                    for i in range(rand, rand + len(self._cache_alpha)):
                        i = i % len(self._cache_alpha)
                        if take_step(i, doc):
                            return True
                else:
                    rand = int(random() * size)
                    for i in range(rand, rand + size):
                        i = i % size
                        if take_step(i, doc):
                            return True
            return False
        
        #### Main routine of train method ####
        num_changed = 0
        examine_all = 1
        while num_changed > 0 or examine_all:
            num_changed = 0
            if examine_all:
                for i in range(size):
                    if examine_example(i):
                        num_changed += 1
            else:
                for i in self._cache_alpha:
                    if examine_example(i):
                        num_changed += 1
            if examine_all == 1:
                examine_all = 0
            elif num_changed == 0:
                examine_all = 1
        for a in range(len(self._model["alpha"])):
            if self._model["alpha"][a] > self._config["tolerance"]:
                self._support_vectors.append(a)
        return self._support_vectors
                
    def classify(self, corpus):
        """
        Hotspot implementation.
        """
    
    def load_model(self, model):
        """
        Hotspot implementation
        """
        
    def save_model(self, model):
        """
        Hotspot implementation
        """
                     
                
            
        
def innerprod (dic_1, dic_2):
    """
    Sparse inner product computation
    """
    temp = 0
    for word in dic_1:
        try:
            temp += dic_2[word] * dic_1[word]
        except KeyError:
            continue
    return temp

def kernelfunc (dic_1, dic_2, _type, par_1, par_2):
    """
    Function that computes the kernel between two documents
    """
    temp = 0
    if _type == "ident":
        temp = innerprod (dic_1, dic_2)
    elif _type == "poly":
        #par_1 = constant, par_2 = degree 
        temp = pow((innerprod (dic_1, dic_2) + par_1), par_2)
    elif _type == "gaussian":
        #par_1 = constant
        tmp = dicsub (dic_1, dic_2)
        temp = exp(- par_1 * innerprod(tmp, tmp))
    return temp

def kernelfuncnorm (dic_1, dic_2, _type, par_1, par_2):
    """
    Function that computes the unity normalized kernel value.
    """
    return kernelfunc (dic_1, dic_2, _type, par_1, par_2) / \
           sqrt(kernelfunc (dic_1, dic_1, _type, par_1, par_2) * \
           kernelfunc (dic_2, dic_2, _type, par_1, par_2))
           
def dicsub (dic_1, dic_2):
    """
    Sparse vector subtraction (used in gaussian kernel)
    """
    temp = {}
    for word in dic_1:
        temp[word] = dic_1[word]
    for word in dic_2:
        try:
            temp[word] = temp[word] - dic_2[word]
        except KeyError:
            temp[word] = - dic_2[word]
    return temp


###offline testing

if __name__ == "__main__":
    from tclass.corpus.dir.xmlreuters import CorpusDirXmlReuters
    import os
    TCLASS = os.environ['TCLASS']
    c = CorpusDirXmlReuters()
    c.load(os.path.join((TCLASS),"tests","corpora","reuters_subset"))
    print c
    cl = ClassifierSmoSvm({"kernel":{"type":"ident", "params":[1,2]}, \
                           "tolerance": 1e-3, "C":0.5})
    print cl.train(c, 1)
        