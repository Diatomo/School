'''
=========================================================
    Author: Charles C. Stevenson
    Date: 02/05/2017
    Description:
        This is the definition of the allowed tokens
        in the Core Language
========================================================
'''

'''
    Class CoreGrammar
    This class contains dictionaries of several categories
    that contain the allowable symbols in the CORE language.

    Its methods contain instructions to validate a Core program
    and some other instructions to separate tokens correctly.
'''

class CoreGrammar(object):

    def __init__(self):
        self.reserved = {'program' : 1, 'begin' : 2, 'end' : 3,
                         'int' : 4, 'if' : 5, 'then' : 6,
                         'else' : 7, 'while' : 8, 'loop' : 9,
                         'read' : 10, 'write' : 11, 'and' : 12, 'or' : 13}
        self.symbols = {';' : 14, ',' : 15, '=' : 16, '!' : 17, '[' : 18, ']' : 19,
                        '(' : 20, ')' : 21, '+' : 22, '-' : 23, '*' : 24,
                        '!=' : 25, '==' : 26, '>=' : 27, '<=' : 28, '>' : 29, '<' : 30}
        self.integers = {'max' : 8,
                         'valid' : set(map(chr,range(48,58))),
                         'integer' : 31}
        self.identifiers = {'max' : 8,
                            'validLetter' : set(map(chr,range(65,91))),
                            'validNumber' : set(map(chr,range(48,58))),
                            'identifier' : 32}
        self.EOF = {'EOF' : 33}
        self.error = False
        self.errorMsg = ''

    '''
         Validating Tokens
         =================
    '''
    '''
        @ValidateTokens
            main method that validates each token passed in from a tokenizer
            if it a token is valid then it will return a valid code defined
            in one of its data members
    '''
    def validateTokens(self, currentToken):
       code = 0
       code = self.validateKeyWords(currentToken, self.reserved.items(),  code)#reserved words
       code = self.validateKeyWords(currentToken, self.symbols.items(), code)#special symbols
       code = self.validateKeyWords(currentToken, self.EOF.items(), code)#end of file
       if (code == 0 and currentToken[0] in self.identifiers['validLetter']):#identifiers must start with a cap Letter
           code = self.validateIdentifier(currentToken)
       elif (code == 0 and currentToken[0] in self.integers['valid']):#numbers must start with a number
           code = self.validateInteger(currentToken)
       return code
    '''
        @validateKeyWords
            validates reseved symbols or words if they aren't defined
            in the reserved words or symbols dictionaries then they
            are invalid!
    '''
    def validateKeyWords(self, currentToken, keywords, code):
        if (code == 0):
           for key, value in keywords:
               if (key == currentToken):
                   code = value
        return code
    '''
        @validateInteger
            Integers can be composed of strings of integers
            for instance 123, each individual integer '1'
            '2', needs to be checked on several different
            criteria
    '''
    def validateInteger(self, currentToken):
        code = 0
        if (len(currentToken) > 8):#Integer can't exceed a length of 8
            self.errorMsg = "Max Overflow, Integer is too large!!"
            self.error = True
        for i in range(len(currentToken)):#Check each number in string and make sure its valid
            if (currentToken[i] not in self.integers['valid']):
                self.errorMsg = "Incorrect Value for an Integer"
                self.error = True
                code = 0
            elif (currentToken[i] in self.integers['valid'] and not self.error):#if all is valid set the print code
                code = self.integers['integer']
        return code
    '''
        @validateIdentifier
            Identifiers can be composed of numbers and capital letters
            for instance 'X123' is valid but 'X1B' is not! Each Identifier
            needs to be checked on several different criteria
    '''
    def validateIdentifier(self,currentToken):
        code = 0
        if (len(currentToken) > 8):
            self.errorMsg = "Max Overflow, Identifier is too long!!"
            self.error = True
        #print("current token = " + str(currentToken))
        for i in range(len(currentToken)):
            if (currentToken[i] not in self.identifiers['validLetter']):#Start with Cap Letters
                for j in range(i,len(currentToken),1):
                    if (currentToken[j] not in self.identifiers['validNumber']):#End with Numbers
                        self.error = True
                        self.errorMsg = "INVALID SYNTAX FOR IDENTIFIER!!"
                break
        if (not self.error):
            code = self.identifiers['identifier']
        return code
