# encoding: utf8
"""
Module containing tokenizer

@authors: Cicero Nogueira dos Santos, Breno Alberti Faria
@contact: breno.alberti@gmail.com
"""

import re

class Tokenizer(object):
    """
    Implements a tokenizer for english texts.
    """

    #>------------------------------------------------------------------------
    def __init__(self):
        self.__reTokenization = re.compile("(^\$|^[A-Z][a-zA-Z]{0,3}\.[A-Z]?" + 
                                           "|^[a-zA-Z]+\$\[a-zA-Z]{0,}|" + 
                                           "\d+[,.:]\d+|\.\.+|,|\w(?:\.\w)+\.?" + 
                                        "|\.|\+|\*|:$|;|\?|[!]+|[nN]'[tT]|" + 
                "\"|^O'[A-Z][\w]*|'|``|`|\[|\]|\{|\}|\(|\)|\d+(?:\w+)|\d+)")
        
        
    #>------------------------------------------------------------------------
    def fineTokenization(self, s):
        """
        Makes fine tokenization for a given string. Is used to separate
        contraction and characters like dots, commas, quotes, etc.
        
        @param s: string to be tokenized.
        @return : a list containing the tokens.
        """
        # Some Regular Expressions Used
        # ^O'[A-Z][\w]*  - Do not break proper names like O'Bryan
        # ^[A-Z].{0,2}\. - Do not break the dot of abreviations like Mr.
        # .*\d[,|\.]\d+  - Do not break the dot of float point numbers like 2.3
        # [nN]'[tT]      - Break the negation contraction: don't  ->  do n't

        
        tokensfine = self.__reTokenization.split(s)
                
        i = 0
        tokensToReturn = []
        while i < len(tokensfine):
            if tokensfine[i]:
                tokensfine[i] = tokensfine[i].strip()
                # manipulate contractions different of n't
                tokensToReturn.append(tokensfine[i])
                try:
                    if tokensfine[i] == "'" and tokensfine[i + 1] in ["s", "S", \
                        "d", "D", "re", "RE", "m", "M", "ve", "VE", "ll", "LL"]:
                        tokensToReturn[len(tokensToReturn) - 1] = \
                            tokensfine[i] + tokensfine[i + 1]
                        i += 1
                    elif tokensfine[i] == "'" and tokensfine[i - 1].endswith("s"):
                        tokensToReturn[len(tokensToReturn) - 1] = "'s"
                except:
                    None
            i += 1

        return tokensToReturn
    
