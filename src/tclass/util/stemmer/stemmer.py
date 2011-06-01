# encoding: utf8
"""
Module containing stemmer

@authors: Henrique d'Escragnolle-Taunay
@contact: htaunay@gmail.com
"""

class Stemmer(object):
	"""
    Class for stemmer. This is an abstract class.
    """

#>------------------------------------------------------------------------------
#> Public:

	def stem(self, word):
		"""
		Virtual function, stemms and returns given word

		@param word: Char pointer strcuture, representing the word to be stemmed
		"""
		raise NotImplementedError
   
