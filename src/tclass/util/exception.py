"""
This module contains the exception classes for the tclass framework

@author: Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

class TClassException(Exception):
    """
    TextClass Exception class.
    All exception classes must inherit this class.

    Descending classes must set the value of _message attribute corresponding
    to a message to be displayed.
    """
    
    def __init__(self, class_name, method_name, message = ""):
        """
        Constructor.
        
        @param string className: the name of class where the error is raised.
        @param string methodName: the name of method where the error is raised.
        @param message: message to be printed when exception is raised.
        """
        if (message == ""):
            self._message = "No error message defined."
        else:
            self._message = message

        self._className = class_name
        self._methodName = method_name
    
    def __str__(self):
        """
        Return the string representation of error.
        """
        return self._message + " - Class: "+ self._className + " Method: " + \
               self._methodName



