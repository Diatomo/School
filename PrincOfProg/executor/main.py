'''
===================================
    Author : Charles Stevenson
    Date : 02/13/2017
    Description:
        Tokenizes a program : Y, written in language : X
        in which X is a text file of the rules for the grammar
        of which the language of Y is to be tokenized
===================================
'''

import Tokenizer
import Token as tok
import nodes
import sys

def main():
    program = sys.argv[1]
    #tk = Tokenizer.Tokenizer(program)#Create program to be tokenized, based on the rules of the languages
    files = ["validAllOneLine.txt", "validAllSimpleExpressions.txt", "validBooleanComplex.txt", "validComplexExpressions.txt",
             "validMinimalWhitespace.txt", "validTypicalIfElse.txt", "validTypicalLoop.txt"]
    #for i in range(len(files) - 1):
        #program = "validTypicalIfElse.txt"
    tk = Tokenizer.Tokenizer(program)
    while (tk.lcurrentToken() != 'EOF'):#Search through all the tokens
        tk.lprocessTokens()#Print out code
        tk.lnextToken()
    tk.lprocessTokens()
    tk.lcloseFile()
    tk.tokens.append(tok.Token('end', 5))

    parser = nodes.ProgramNode()
    parser.parseProgram(tk)
    #print("PARSE COMPLETE!!")
    #print("==================")
    print(nodes.symTab)
    #print(" ")
    parser.printProgram()


if __name__ == "__main__":
    main()
