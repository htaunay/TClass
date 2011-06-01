#encoding: utf8
"""
Evaluation tools for trained models. Computes Precision, Recall and F1 values
for classification experiments. 

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

class Measures(object):
    """
    Implements IR evaluation tools (Precision, Recall and F1).
    """
    
    def __init__(self, test_corpus, class_index, result):
        """
        @param test_corpus: Corpus. Test corpus
        @param class_index: int. Index of 'true' (or positive) class
        @param result: list. Contains the classification results on the test
                             corpus
        """
        docs = test_corpus.get_documents()
        self.__result = result
        self.__true = []
        for clazz in range(len(docs)):
            for document in docs[clazz]:
                if clazz == class_index:
                    self.__true.append(1)
                else:
                    self.__true.append(-1)
        self.__positives = 0
        for item in range(len(result)):
            if (result[item] >= 0 and self.__true[item] >= 0):
                self.__positives += 1
            
    def recall(self):
        """
        Computes the recall of the classification model in the experiment.
                         true positives
        Recall = --------------------------------
                 true positives + false negatives
        """
        num = 0
        for item in self.__true:
            if item > 0:
                num += 1
        return self.__positives/float(num)
    
    def precision(self):
        """
        Computes the precision of the classification model in the experiment.
                            true positives
        Precision = --------------------------------
                    true positives + false positives
        """
        num = 0
        for item in self.__result:
            if item > 0:
                num += 1
        return self.__positives/float(num)
        
    def f_1(self):
        """
        Computes the F1 measure of the classification model in the experiment.
             2 * Precision * Recall 
        F1 = ----------------------
               Precision + Recall
        """
        precision = self.precision()
        recall = self.recall()
        
        return 2 * precision * recall / (precision + recall)
        
   
   
   
   