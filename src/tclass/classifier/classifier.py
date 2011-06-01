"""
Module containing abstract Classifier class

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

class Classifier (object):
    """
    Abstract class for classification algorithms        
    """

    def train(self, corpus, class_index):
        """
        Hotspot method for model training.
        
        @param corpus: Training corpus        
        @param class_index: True class (positive)
        """
        raise NotImplementedError
        

    def classify(self, corpus):
        """
        Hotspot method for corpus classification.
        
        @param corpus: Corpus to be classified
        @return: class of each document (depending on the algorithm it may
                 include more information, like confidence)
        """
        raise NotImplementedError
    
    def clear(self):
        """
        Hotspot. Clears models and other specific fields. Allows new training.
        """
        raise NotImplementedError
        
    
    def load_model(self, model):
        """
        Hotspot for model loading.
        
        @param model: Model file        
        """
        raise NotImplementedError
        

    def save_model(self, model):
        """
        Hotspot for model saving.
        
        @param model: Model file
        """
        raise NotImplementedError
