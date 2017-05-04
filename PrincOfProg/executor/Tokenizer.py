'''
===========================================
    Author : Charles Stevenson
    Date : 02/13/2017
    Description:
        Tokenizer for the any defined
        programming language. The definition
        of the language is contained in a
        python object, in this case
        Core
============================================
'''

import re
import Token as tok
import Core #Description of language

'''Helper Functions'''
def splitLine(f):
    line = f.readline()
    line = line[:-1]
    #line = re.split('([^\s;+,><!()=-]+)', line)# RegExpr, matche
    line = re.split('([\s\[\]=;+--,><!()*])', line)
    line = list(filter(('').__ne__, line))
    for i in range(len(line)):
        line[i] = filter((' ').__ne__, line[i])
    line = list(filter(('').__ne__, line))
    line = list(filter(('  ').__ne__, line))
    line = list(filter(('   ').__ne__, line))
    line = list(filter(('    ').__ne__, line))
    line = list(filter(('\n').__ne__, line))
    line = list(filter(('\t').__ne__, line))
    line = list(filter(('\t ').__ne__, line))
    #print(line)
    return line
'''
    Class Tokenize
        Tokenize object to tokenize any language
        depending on its definition object
'''
class Tokenizer(object):

    def __init__(self, fileName):
        '''private'''
        self.__lineNum = 1

        '''public'''
        self.f = open(fileName, 'r')
        self.fSize = self.getFileSize()
        self.line = splitLine(self.f)
        self.currentIndex = 0
        self.tokens = []
        self.cToken = None
        self.grammar = Core.CoreGrammar()#Language Description Object

    '''
        @nextToken
            return next token from Queue
    '''
    def nextToken(self):
        nextToken = self.tokens.pop(0).token
        self.cToken = nextToken
        return nextToken

    def peekToken(self):
        return self.tokens[0].token

    def currentToken(self):
        return self.cToken


    def getFileSize(self):
        counter = 0
        for line in self.f:
            counter += 1
        self.f.seek(0)
        return counter
    '''
        @closeFile
            closes file loaded in f
    '''
    def lcloseFile(self):
        self.f.close()
    '''
        @currentToken
            returns current token loaded in an array
            from a split string
    '''
    def lcurrentToken(self):
        if (len(self.line) > 0 and (self.__lineNum != self.fSize or self.currentIndex < len(self.line)-1)):
            return self.line[self.currentIndex]
        else:
            return 'EOF'
    '''
        @seeNextToken
            returns nextToken without setting
            the current token
    '''
    def lseeNextToken(self):
        nextToken = ''
        if (self.currentIndex < len(self.line)-1):
            nextToken = self.line[self.currentIndex+1]
        return nextToken
    '''
        @nextToken
            sets the next token as the current token
    '''
    def lnextToken(self):
        if(self.currentIndex < len(self.line)-1):
            token = tok.Token(self.line[self.currentIndex], self.__lineNum)
            self.currentIndex += 1
        else:
            token = tok.Token(self.line[self.currentIndex], self.__lineNum)
            self.currentIndex = 0
            self.__lineNum += 1
            self.line = splitLine(self.f)
        self.tokens.append(token)
        self.lcurrentToken()
    '''
        @ProcessTokens
            processes each token and print out their specified code
    '''
    def lprocessTokens(self):
        if (len(self.line) > 0):
            code = self.grammar.validateTokens(self.line[self.currentIndex])
            if (code != 0 and not self.grammar.error):
                pass
                #print(code)
            else:
                pass
                #self.grammar.error = False
                #print("CURRENT TOKEN : " + str(self.lcurrentToken()) + " ERROR = " + str(self.grammar.errorMsg) +
                 # " Line Number = " + str(self.__lineNum))
