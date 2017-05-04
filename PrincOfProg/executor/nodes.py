

'''
    Author = Charles Stevenson
    Date : March 1st, 2017
    Description
        Recursive Descent Parser
        for Princples of Programming

        Overall Structure:
            Following the Core grammer description, documented in red,
            It starts with a tokenized program and then this parses
            out a series of nodes based on the program's instructions.
'''

#imports
import Core
import sys
grammar = Core.CoreGrammar()#TODO not sure if I still use this.
symTab = {}#Global symTab #TODO integrate into a parsetree class
#TODO Break up nodes into separate files via categories.
#TODO Break up Printing Processes and Parsing Processes


#                                    Bark                                            #
'''================================================================================'''
'''
    Class : ProgramNode
        <Prog> ::= program <decl-seq> begin <stmt-seq> end
        Initiates Parsing
'''

class ProgramNode:

    def __init__(self):
        self.ds = DeclSeqNode()
        self.ss = StmtSeqNode()

    def parseProgram(self, t):
        tok = t.nextToken()#Leash program
        #print("PARSE PROGRAM : (EXP : PROGRAM) : " + str(tok))#Debug
        self.ds.parseDeclSeq(t)
        tok = t.nextToken()#Consume begin
        #print("PARSE PROGRAM : (EXP : BEGIN) : " + str(tok))#Debug
        #print("STATEMENT SEQUENCE")#Debug
        tok = t.nextToken()#Leash first token after begin
        #print("PARSE PROGRAM : (EXP : STMT) : " + str(tok))#Debug
        self.ss.parseStmtSeq(t)

    def printProgram(self):
        sys.stdout.write("program\n")
        self.ds.printDeclSeq()
        sys.stdout.write("\nbegin\n")
        self.ss.printStmtSeq()
        sys.stdout.write("end\n")
	
	def execProgram(self):
		self.ds.execDeclSeq()
		self.ss.execStmtSeq()
'''
    Class : DeclSeqNode
        <decl-seq> ::= <decl> | <decl><decl-seq>
        Header : Static Declarations
'''
class DeclSeqNode:

    def __init__(self):
        self.d = DeclNode()
        self.ds = None

    def parseDeclSeq(self, t):
        self.d.parseDecl(t)
        tok = t.peekToken()#Peek at either int or Begin; (ExCase) of another line of declarations
        #print("DeclSeq Node : (EXP : INT || BEGIN) : " + str(tok))#Debug
        if (tok == 'int'):
            self.ds = DeclSeqNode()
            self.ds.parseDeclSeq(t)

    def printDeclSeq(self):
        self.d.printDecl()
        if (self.ds != None):
            self.ds.printDeclSeq()

	def execDeclSeq(self):
		self.d.declExec()
		if (self.ds != None):
			self.ds.execDeclSeq()

'''
    Class : StmtSeqNode
        <stmt-seq> ::= <stmt> | <stmt><stmt-seq>
        Header : Container for the main Statements in the program
            i.e. <assign> | <if> | <loop> | <in> | <out>
'''
class StmtSeqNode:

    def __init__(self):
        self.s = StmtNode()
        self.ss = None

    def parseStmtSeq(self, t):
        self.s.parseStmt(t)
        #print("STMTSEQ CURRENT TOKEN " + (t.currentToken()))#Debug
        tok = t.currentToken()
        if (tok != 'end' and tok != 'else' and tok != ';'):
            self.ss = StmtSeqNode()
            self.ss.parseStmtSeq(t)

    def printStmtSeq(self):
        self.s.printStmt()
        if (self.ss != None):
            self.ss.printStmtSeq()
	
	def execStmtSeq(self):
		self.s.execStmt()
		if (self.ss != None):
			self.ss.execStmtSeq()
'''
    Class : DeclNode
        <decl> ::= int <id_list>;
        Header : Container for the main Statements in the program
            i.e. <assign> | <if> | <loop> | <in> | <out>
'''
class DeclNode:

    def __init__(self):
        self.idList = IdListNode()

    def parseDecl(self, t):
        tok = t.nextToken()#consumes int
        #print("DECL NODE : (EXP : int) : " + str(tok))#Debug
        self.idList.parseIdList(t)
        tok = t.nextToken()#consumes ;
        #print("DECL NODE : (EXP : ; ) : " + str(tok))#Debug

    def printDecl(self):
        sys.stdout.write("int ")
        self.idList.printIdList()

	def execDecl(self):
		#TODO what is suppose to go here?

'''
    Class : IdListNode
        <id> ::= <id>, <id_list>;
        Header : Container for variables
'''
class IdListNode:

    def __init__(self):
        self.idn = None
        self.idList = None

    def parseIdList(self, t):
        tok = t.nextToken()#grab ID
        #print("IDLIST NODE : (EXP : ID) : " + str(tok))#Debug
        self.idn = IdNode(t.currentToken())
        self.idn.parseId(t)
        tok = t.peekToken()#Signals another variable declaration
        if (tok == ','):
            tok = t.nextToken()
            #print("IDLIST NODE = (EXP : , " + str(tok))
            self.idList = IdListNode()
            self.idList.parseIdList(t)

    def printIdList(self):
        sys.stdout.write(self.idn.getName())
        if (self.idList != None):
            sys.stdout.write(', ')
            self.idList.printIdList()
            sys.stdout.write(';')

	def execIdList(self):
		self.idn.execId()
		if (self.idList != None):
			self.idList.execIdList()
'''================================================================================'''
#                                  Trunk                                             #
'''================================================================================'''

'''
    Class : StmtNode
        <stmt> ::= <assign> | <if> | <loop> | <in> | <out>
        Body of the program
'''
class StmtNode:

    def __init__(self):
        self.assign = None
        self.fi = None
        self.loop = None
        self.inp = None
        self.out = None
        self.altNo = 1

    def parseStmt(self, t):
        tok = t.currentToken()
        #print("STMT NODE : (exp : STMT) : " + str(tok))#debug
        if (tok == 'if'):#Nodes are set by tok
            self.fi = IfNode()
            self.altNo = 2
            self.fi.parseIf(t)
        elif (tok == "while"):
            self.loop = LoopNode()
            self.altNo = 3
            self.loop.parseLoop(t)
        elif (tok == "read"):
            self.inp = InputNode()
            self.altNo = 4
            self.inp.parseInput(t)
        elif (tok == "write"):
            self.out = OutputNode()
            self.altNo = 5
            self.out.parseOutput(t)
        else:
            self.assign = AssignNode()
            self.altNo = 1
            self.assign.parseAssign(t)

    def printStmt(self):
        if (self.altNo == 1):
            self.assign.printAssign()
        elif(self.altNo == 2):
            self.fi.printIf()
        elif(self.altNo == 3):
            self.loop.printLoop()
        elif(self.altNo == 4):
            self.inp.printInput()
        elif(self.altNo == 5):
            self.out.printOutput()

	def execStmt(self):
		if (self.altNo == 1):
			self.assign.execAssign()
		elif (self.altNo == 2):
			self.fi.execIf()
		elif (self.altNo == 3):
			self.loop.execLoop()
		elif (self.altNo == 4):
			self.inp.execOutput()
		elif (self.altNo == 5):
			self.out.execInpuit()

'''
    Class : AssignNode
        <assign> ::= <id> = <exp>
        Variable Updates or Assignments
'''
class AssignNode:

    def __init__(self):
        self.idn = None
        self.expr = ExprNode()

    def parseAssign(self,t):
        self.idn = IdNode(t.currentToken())#sets variable label into memory
        self.idn.parseId(t)#
        tok = t.nextToken()# Consumesi =
        #print("ASSIGN NODE : (EXP : = ) : " + str(tok))#Debug
        tok = t.nextToken()# Expression
        #print("ASSIGN NODE : (EXP : EXPR ) : " + str(tok))#Debug
        self.expr.parseExpr(t)

    def printAssign(self):
        sys.stdout.write('  ')
        sys.stdout.write(self.idn.getName())
        sys.stdout.write('=')
        self.expr.printExpr()
        sys.stdout.write(';\n')

	def execAssign(self):
		self.idn.execId()
		self.expr.execExpr()

'''
    Class : IfNode
        <if> ::= if <cond> then <stmt-seq> end;
               | if <cond> then <stmt-seq> else <stmt-seq> end;
        Control Flow
'''
class IfNode:

    def __init__(self):
        self.cond = CondNode()
        self.thenSeq = StmtSeqNode()
        self.elseSeq = None
        self.altNo = 1

    def parseIf(self,t):
        self.cond.parseCond(t)
        tok = t.nextToken()#Consumes end of cond )
        #print("PARSE IF : (EXP = THEN) : " + str(tok))#Debug
        self.thenSeq.parseStmtSeq(t)
        tok = t.currentToken()#Leashes else
        #print("PARSE IF : (EXP = ELSE || END) : " + str(tok))#Debug
        if (tok == "else"):
            t.nextToken()#Consume else
            #print("PARSE ELSE IN ELSE-IF " + str(tok))Debug
            self.altNo = 2
            self.elseSeq = StmtSeqNode()
            self.elseSeq.parseStmtSeq(t)
        #tok = t.currentToken()#Debug
        #print("PARSE IF : (EXP = END ) : " + str(tok))#Debug
        tok = t.nextToken()
        #print("PARSE IF : (EXP = ; ) : " + str(tok))#Debug

    def printIf(self):
        sys.stdout.write("  if ")
        self.cond.printCond()
        sys.stdout.write(" then\n")
        self.thenSeq.printStmtSeq()
        if (self.altNo == 2):
            sys.stdout.write("  else\n")
            self.elseSeq.printStmtSeq()
        #print("end;")
	
	def execIf(self):
		self.cond.execCond()
		self.thenSeq.execStmtSeq()
		if (self.altNo == 2):
			self.elseSeq.execStmtSeq()
'''
    Class : LoopNode
        <loop> ::= while <cond> loop <stmt-seq> end;
        Iteration
'''
class LoopNode:

    def __init__(self):
        self.cond = CondNode()
        self.ss = StmtSeqNode()

    def parseLoop(self, t):
        tok = t.currentToken()#while
        #print("PARSE LOOP : (EXP : WHILE) : " + str(t.currentToken()))
        self.cond.parseCond(t)
        #print("PARSE LOOP : (EXP: LOOP) : " + str(t.currentToken()))
        tok = t.nextToken()#Consumes previous token -_-
        self.ss.parseStmtSeq(t)
        #print("END OF LOOP : (EXP : END) : " + str(t.currentToken()))
        t.nextToken()

    def printLoop(self):
        sys.stdout.write("  while ")
        self.cond.printCond()
        sys.stdout.write(" loop\n")
        self.ss.printStmtSeq()
        sys.stdout.write("  end;\n")

	def execLoop(self):
		self.cond.execCond()
		self.ss.execStmtSeq()

'''
    Class : InputNode
        <in> ::= read <idlist>;
        Reads : User_Input
'''
class InputNode:

    def __init__(self):
        self.IdList = None

    def parseInput(self, t):
        tok = t.currentToken()#Consumes Read
        #print("PARSE INPUT : (EXP : READ) : " + str(tok))#Debug
        self.IdList = IdListNode()
        self.IdList.parseIdList(t)
        tok = t.nextToken()#Consumes ;
        #print("PARSE INPUT : (EXP : ; ) : " + str(tok))#Debug
        tok = t.nextToken()

    def printInput(self):
        sys.stdout.write("    read ")
        self.IdList.printIdList()
        sys.stdout.write("\n")

	def execInput(self):
		self.IdList.execIdList()

'''
    Class : OutputNode
        <out> ::= write <idlist>;
  =^.^= Writes : User_Output
'''

class OutputNode:

    def __init__(self):
        self.IdList = IdListNode()

    def parseOutput(self, t):
        tok = t.currentToken()# write
        #print("PARSE OUTPUT : (EXP : WRITE) : " + str(tok))
        self.IdList.parseIdList(t)
        tok = t.nextToken()# ;
        #print("PARSE OUTPUT : (EXP : ; ) : " + str(tok))
        tok = t.nextToken()

    def printOutput(self):
        sys.stdout.write("    write ")
        self.IdList.printIdList()
        sys.stdout.write("\n")

	def execOutput(self):
		self.IdList.execIdList()

'''================================================================================'''
#                        Phloem     &&      Xylem                                    #
'''================================================================================'''
'''
    Class : CondNode
        <cond> ::= <comp> | !<cond> | [<cond> and <cond>]
                                    | [<cond> or  <cond>]
  =^.^= Conditionals : Relations [(X>10)and(Y<8)]
'''
class CondNode:

    def __init__(self):
        self.comp = None
        self.cond1 = None
        self.cond2 = None
        self.altNo = 1

    def parseCond(self,t):
        tok = t.currentToken()#Must Start right before condition i.e. (
        nTok = t.peekToken() # First Check of Which Condition
        if (nTok == '!'):
            self.altNo = 2
            self.comp = CompNode()
            tok = t.nextToken()#Consume !
            tok = t.nextToken() # Set with a (
            self.comp.parseComp(t)
        elif (nTok == '['):
            tok = t.nextToken()#Consume [
            self.cond1 = CondNode()
            self.cond1.parseCond(t)
            tok = t.currentToken()
            if (tok == 'and'):
                self.altNo = 3
                self.cond2 = CondNode()
                self.cond2.parseCond(t)
                tok = t.nextToken() #Consumes ']'
            elif (tok == 'or'):
                self.altNo = 4
                self.cond2 = CondNode()
                self.cond2.parseCond(t)
                tok = t.nextToken() #Consumes ']'
        elif (nTok == '('):
            self.altNo = 1
            tok = t.nextToken() #Sets with (
            self.comp = CompNode()
            self.comp.parseComp(t)

    def printCond(self):
        if (self.altNo == 1):#comp
            self.comp.printComp()
        elif (self.altNo == 2):#!
            sys.stdout.write('!')
            sys.stdout.write(self.comp.printComp())
        elif (self.altNo == 3):#and
            sys.stdout.write('[')
            self.cond1.printCond()
            sys.stdout.write('and')
            self.cond2.printCond()
            sys.stdout.write(']')
        elif (self.altNo == 4):#
            sys.stdout.write('[')
            self.cond1.printCond()
            sys.stdout.write('or')
            self.cond2.printCond()
            sys.stdout.write(']')

	def execCond(self):#evalutes a condtion
		result = None
		if (self.altNo == 1):
			result = self.comp.execComp()
		elif (self.altNo == 2):# '!'
			result = not self.comp.execCond()
		elif (self.altNo == 3):# 'and'
			result = self.cond1.execCond() and self.cond2.execCond()
		elif (self.altNo == 4):# 'or'
			result = self.cond1.execCond() or self.cond2.execCond()
'''
    Class : CompNode
        <cond> ::= (<fac> <comp-op> <fac>)
  =^.^=  The organization of the inside of the parentheses:
                                           [(X>10)and(Y<8)]
                                            ^____^   ^___^
'''
class CompNode:

    def __init__(self):
        self.fac1 = FacNode()
        self.compOp = CompOpNode()
        self.fac2 = FacNode()

    def parseComp(self,t):
        tok = t.nextToken() #Consume (
        #print("PARSE COMPNODE : (EXP : ID ) : " + str(tok))#Debug
        self.fac1.parseFac(t)#Id or Int or Expr
        #print("PARSE COMPNODE bewtween factors : (EXP : compop) : " + str(t.currentToken()))#Debug
        self.compOp.parseCompOp(t)
        #print("PARSE COMPNODE : (EXP : NUM ) : " + str(t.currentToken()))#Debug
        self.fac2.parseFac(t)

    def printComp(self):
        sys.stdout.write('(')
        self.fac1.printFac()
        self.compOp.printCompOp()
        self.fac2.printFac()
        sys.stdout.write(')')

	def execComp(self):#returns a boolean from a relation
		result = 0
		compOp = self.compOp.execCompOp()
		if (compOp == '<'):
			result = self.fac1.execFac() < self.fac2.execFac()
		elif (compOp == '>'):
			result = self.fac1.execFac() > self.fac2.execFac()
		elif (compOp == '<='):
			result = self.fac1.execFac() <= self.fac2.execFac()
		elif (compOp == '>='):
			result = self.fac1.execFac() >= self.fac2.execFac()
		elif (compOp == '=='):
			result = self.fac1.execFac() == self.fac2.execFac()	
		elif (compOp == '!='):	
			result = self.fac1.execFac() !=  self.fac2.execFac()
		return result
'''
    Class : ExprNode
        <expr> ::= <term> | <term> + <expr> | <term> - <expr>
=^.^=   Expressions handle the or(+) and complements(-) factors
'''
class ExprNode:

    def __init__(self):
        self.term = None
        self.expr = None
        self.altNo = 1

    def parseExpr(self,t):
        tok = t.currentToken()
        #print("EXPR FIRST TOKEN : (EXP, VARIABLE) : " + str(tok))
        nTok = t.peekToken()#sees if there is a conjunction
        if (nTok == '+'):
            self.altNo = 2
            self.term = TermNode()
            self.term.parseTerm(t)
            tok = t.nextToken()
            #print("ALT 2 EXPR " + str(tok))
            self.expr = ExprNode()
            self.expr.parseExpr(t)
        elif (nTok == '-'):
            self.altNo = 3
            self.term = TermNode()
            self.term.parseTerm(t)
            tok = t.nextToken()
            #print("ALT 3 EXPR " + str(tok))
            self.expr = ExprNode()
            self.expr.parseExpr(t)
        else:
            self.term = TermNode()
            self.term.parseTerm(t)
            if(t.currentToken() == '-'):
                self.altNo = 3
                t.nextToken()
                self.expr = ExprNode()
                self.expr.parseExpr(t)
            elif(t.currentToken() == '+'):
                self.altNo = 2
                t.nextToken()
                self.expr = ExprNode()
                self.expr.parseExpr(t)

    def printExpr(self):
        if (self.altNo == 1):
            self.term.printTerm()
        elif (self.altNo == 2):
            self.term.printTerm()
            sys.stdout.write("+")
            self.expr.printExpr()
        elif (self.altNo == 3):
            self.term.printTerm()
            sys.stdout.write("-")
            self.expr.printExpr()

	def execExpr(self):
		result = None
		if (self.altNo == 1):
			result = self.term.execTerm()
		elif (self.altNo == 2):
			result = self.term.execTerm() + self.expr.execExpr()
		elif (self.altNo == 3):
			result = self.term.execTerm() - self.expr.execExpr()
		return result
'''
    Class : TermNode
        <term> ::= <term> | <fac> * <term>
=^.^=   Handles Ands(+) of Factors
'''
class TermNode:

    def __init__(self):
        self.fac = FacNode()
        self.altNo = 1
        self.term = None

    def parseTerm(self, t):
        nTok = ''
        #print("TERM NODE!!")
        self.fac = FacNode()
        self.fac.parseFac(t)
        tok = t.currentToken()
        #print("currTERM NODE : (EXP : * || + | - | ; ) : " + str(tok))
        if (tok == '*'):
            self.altNo = 2
            self.term = TermNode()
            tok  = t.nextToken() # DIGIT OR VARIABLE
            #print("PARSE TERM ALT 2 : (EXP : NUMBER OR VARIABLE) : " + str(tok))
            self.term.parseTerm(t)

    def printTerm(self):
        self.fac.printFac()
        if (self.altNo == 2):
            sys.stdout.write('*')
            self.term.printTerm()

	def execTerm(self):
		self.fac.execFac()
		if (altNo == 2):
			self.term.execTerm()

'''================================================================================'''
#                                  Chloroplast                                       #
'''================================================================================'''
'''
    Class : FacNode
        <fac> ::= <int> | <id> | (<expr>)
=^.^=   Atoms (LR of equal sign) in an expression || comparison
'''
class FacNode:

    def __init__(self):
        self.idn = None
        self.digit = None
        self.expr = None
        self.altNo = 0

    def parseFac(self, t):
        tok = t.currentToken()
        #print("PARSE FACTOR : EXP( NUM, ID, OR ( ) : " + str(tok))
        if (tok != '(' and not tok.isdigit()):
            self.altNo = 1
            #print("FACTOR " + t.currentToken())
            self.idn = IdNode(t.currentToken())
            self.idn.parseId(t)
            tok = t.nextToken()
            #print("FACTOR LEAVING" + t.currentToken())
        elif (tok.isdigit()):
            self.altNo = 2
            self.digit = DigitNode(t)
            self.digit.parseDigit(t)
            tok = t.nextToken()
            #print("DIGIT IN FAC : " + str(tok))
        elif (tok == '('):
            #print("EXPRESSION")
            self.altNo = 3
            tok = t.nextToken()
            self.expr = ExprNode()
            self.expr.parseExpr(t)
            tok = t.nextToken() #consume )

    def printFac(self):
        if (self.altNo == 1):
            sys.stdout.write(self.idn.getName())
        elif (self.altNo == 2):
            sys.stdout.write(self.digit.printDigit())
        elif (self.altNo == 3):
            sys.stdout.write('(')
            self.expr.printExpr()
            sys.stdout.write(')')
		
	def execFac(self):#This Should return a symbol table
		result = 1
		if (self.altNo == 1):
			result = self.idn.execId()
		elif (self.altNo == 2):#Or a digit
			result = self.digit.execDigit()
		elif (self.altNo == 3):
			self.expr.execExpr()
		if (self.altNo != 3):
			return result
'''
    Class : CompOpNode
        <compOp> ::= != | == | < | > | <= | >=
=^.^=   Comparison Operations
'''
class CompOpNode:

    def __init__(self):
        self.compOp = None

    def parseCompOp(self,t):
        tok = t.currentToken()
        nTok = t.peekToken()
        if (nTok == '='):
            self.compOp = tok + nTok
            t.nextToken()
        else:
            self.compOp = tok
            t.nextToken()

    def printCompOp(self):
        sys.stdout.write(self.compOp)

	def execCompOp(self):
		return self.compOp

'''
    Class : IdNode
        <id> ::= |A|B|C|...|X|Y|Z|
=^.^=   Letters
'''
class IdNode:

    def __init__(self, n):
        self.name = n
        self.value = None
        self.initialized = False

    def parseId(self, t):
        tok = t.currentToken()
        if (tok not in symTab):
            #node = IdNode(tok)
            symTab[tok] = self
            #print("Symbol Table : " + str(symTab))
        return symTab[tok]

    def setValue(self, v):
        self.value = v
        self.initialized = True

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

	def execId(self):
		return self.name #TODO maybe return value too?
'''
    Class : DigitNode
        <digit> ::= |0|1|2|3|4|5|6|7|8|9|
=^.^=   NoomBahs!
'''
class DigitNode:

    def __init__(self,t):
        #print("DIGIT CURRENT TOKEN : " + str(t.currentToken()))
        self.value = int(t.currentToken())

    def parseDigit(self, t):
        #print("Parsing Digit")
        if (t.peekToken() == ')' or t.peekToken() == ';'):
            t.nextToken() #consume )
        #print("DIGIT self.value = " + str(self.value))

    def printDigit(self):
        return str(self.value)

	def execDigit(self):
		return self.value

'''================================================================================'''
