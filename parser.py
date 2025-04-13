from lexer import Lexer
OPERANTS = ["IDENTIFIER","VAL", "MODIFY"]
debug = True

#----------------------ast trying----------------------#
#import ast

#text_code_in_python = """
#x = 1
#y = 2
#if x < y:
#    print("yayy")
#"""
#AST = ast.parse(text_code_in_python)
#print(ast.dump(AST))
#print(ast.unparse(AST))
#---------------------ast trying-----------------------#

class Identifier:
    def __init__(self, name):
        self.name = name
    def printout(self):
        return self.name
    def translate(self):
        return self.name

value_map = {"STRING": str,
             "INT": int,
             "FLOAT": float,
             }
class Value:
    def __init__(self, val, typ="STRING"):
        self.val = val
        self.type = typ
        self.pythontype = value_map.get(typ, str)
    def printout(self):
        return self.val
    def translate(self):
        #return self.pythontype(self.val)  # TODO, this causes crash in printing block
        return self.val
    
class ExpressionTail:
    def __init__(self, oper, term, tail):
        assert oper is not None, "No operator given for ExpressionTail"
        assert term is not None, "No term given for ExpressionTail"
        self.oper = oper
        self.term = term
        self.tail = tail
    def printout(self):
        if self.tail is None:
            return f'{self.oper} {self.term.printout()}'
        else:
            return f'{self.oper} {self.term.printout()}{self.tail.printout()}'
    def translate(self):
        if self.tail is None:
            if self.oper == "and":
                return f',{self.term.translate()}]'
            return f'{self.oper}{self.term.translate()}'
        else:
            if self.oper == "and":
                return f',{self.term.translate()},{self.tail.translate()}'
            return f'{self.oper}{self.term.translate()}{self.tail.translate()}'


class Expression:
    def __init__(self, term, tail):
        assert term is not None
        self.term = term
        self.tail = tail 
    def printout(self):
        if self.tail is None:
            return f"{self.term.printout()}"
        else:
            return f"{self.term.printout()} {self.tail.printout()}"
    def translate(self):
        if self.tail is None:
            return f"{self.term.translate()}"
        else:
            if self.tail.oper == "and":
                return f'[{self.term.translate()}{self.tail.translate()}'
            return f"{self.term.translate()} {self.tail.translate()}"

class Assignment:
    def __init__(self, id_, val):
        assert isinstance(id_, Identifier), "Tried to put non-identifier in left position in assignment"
        self.id = id_
        #assert isinstance(val, Value) or isinstance(val, Identifier) or isinstance(val, OperatorCommalist), f"Assigning prohibited value ({val.printout()}) to an identifier"
        assert isinstance(val, Expression), f"Tried to assing non-expression to the right.S"
        self.value = val
    def printout(self):
        return f"Let {self.id.printout()} be {self.value.printout()}.\n"
    def translate(self):
        return f"{self.id.translate()} = {self.value.translate()}\n"

class PrintStatement:
    def __init__(self, val):
        self.val = val
    def printout(self):
        return f"Print {self.val.printout()}.\n"
    def translate(self):
        return f"print({self.val.translate()})\n"

class OperatorCommalist:
    def __init__(self, operator, values):
        assert isinstance(values, list)
        self.operator = operator
        self.values = values
    def printout(self):
        return f'{self.operator}({",".join([i.printout() for i in self.values])})'
    def translate(self):
        if self.operator == "and":
            return f'{[i.translate() for i in self.values]}'
        else:
            return f'{self.operator.join([i.translate() for i in self.values])}'
        
class IfStatement:
    def __init__(self, expr, block):
        assert isinstance(expr, Expression)
        self.expr = expr
        self.block = block
    def printout(self):
        return f"""If {self.expr.printout()} is true,
        {[i.printout() for i in self.block]}
Done.
"""
    def translate(self):
        return f"""if {self.expr.translate()}:
        {[i.translate() for i in self.block]}
"""

class WhileStatement:
    def __init__(self, expr, block):
        assert isinstance(expr, Expression)
        self.expr = expr
        self.block = block
    def printout(self):
        return f"""While {self.expr.printout()} is true,
        {[i.printout() for i in self.block]}
Done.
"""
    def translate(self):
        return f"""While {self.expr.translate()}:
        {[i.translate() for i in self.block]}
"""

class ForStatement:
    def __init__(self, looper, loopee, block):
        self.looper = looper
        self.loopee = loopee
        self.block = block
    def printout(self):
        return f"""For {self.looper.printout()} in list {self.loopee.printout()},
        {[i.printout() for i in self.block]}
Done.
"""
    def translate(self):
        return f"""for {self.looper.translate()} in {self.loopee.translate()},
        {[i.translate() for i in self.block]}
"""
        

class FunctionCall:
    def __init__(self, name, params):
        assert isinstance(name, Identifier)
        self.name=name
        self.params=params
    def printout(self):
        return f'Modify {self.params.printout()} with function {self.name.printout()}.\n'
    def translate(self):
        return f'{self.name.translate()}({self.params.translate()})\n'
        

class FunctionDefinition:
    def __init__(self, name, params, block, return_values=None):
        self.name = name
        self.params = params
        self.block = block
        self.return_values = return_values
    def printout(self):
        if self.return_values:
            return f"""Function {self.name.printout()} acts on {self.params.printout()},
                    {[i.printout() for i in self.block]}
                    Return {self.return_values.printout()}.
                    Done.
                    """
        else:
            return f"""Function {self.name.printout()} acts on {self.params.printout()},
                    {[i.printout() for i in self.block]}
                    Done.
                    """
    def translate(self):
        if self.return_values:
            return f"""def {self.name.translate()}({self.params.translate()}):,
                    {[i.translate() for i in self.block]}
                    return {self.return_values.translate()}
                    """
        else:
            return f"""def {self.name.translate()}({self.params.translate()}):,
                    {[i.translate() for i in self.block]}
                    """


def parseOperant(t):
    '''<operant> :: <literal> | <identifier | <functioncallstatement>'''
    if debug: print(f'In parseOperant() with {t.first()}')
    if t.first() == "IDENTIFIER":
        if debug: print(f'In parseOperant(), identifier found')
        new_id = t.pop()
        return Identifier(new_id["value"])
    elif t.first() == "MODIFY":
        if debug: print(f'In parseOperant(), function call found')
        t.pop()
        return parseFunctionCall(t)
    elif t.first() == "VAL":
        if debug: print(f"In parseOperant(), Value found {t.first()}")
        val = t.pop()
        return Value(val["value"], typ=val["type"])
    raise SyntaxError("Should not reach this, parseOperant with no operant in sight.")

def parseFunctionCall(t):
    '''
    <functioncallstatement> ::= "Modify" <operatorlist> "with" <identifier> "."    # TODO Function vs function problem
    '''
    if debug: print("Now in parseFuntionCall()")
    # "modify" should be removed already
    params = parseOperatorList(t)
    assert t.first() == "WITH" 
    if t.second() == "FUNCTION":  # TODO HERE
        t.pop()
    t.pop()
    function_name = parseOperant(t)
    assert t.first() == "DOT"
    t.pop()
    return FunctionCall(function_name, params)



    

def parseExpression(t):
    '''
    <expression> ::= <term> <expression_tail>
    <term> ::= <functioncallstatement>
            | <operatorlist>
            | <operant>
    <expression_tail> ::= <operator> <term> <expression_tail>
                        | ε
    '''

    def parseExpressionTail(t):
        if debug: print(f"In expression tail, first = {t.first()}")
        if t.first() == "OPER" and t.second() != "LPAREN":
            oper = t.pop()
            term = parseTerm(t)
            tail = parseExpressionTail(t)
            if debug: print(f'Returning expressiontail with {oper["value"]}, {term.printout()}')
            return ExpressionTail(oper["value"], term, tail)
        if t.first() == "OPER" and t.second() == "LPAREN":
            oper = t.pop()
            return OperatorCommalist(oper["value"], t)

    def parseTerm(t):
        if debug: print(f"in parseTerm() with {t.first()}")
        if t.first() == "MODIFY":
            return parseFunctionCall(t)
        elif t.first() == "OPER":
            return parseOperatorList(t)
        elif t.first() in OPERANTS:
            return parseOperant(t)
        raise SyntaxError(f'YOU SHOULD NOT REACH THIS EVER: IN parseTerm() without a term.')
        
    if debug: print(f"Now in parseExpression, first token = {t.first()}, second token = {t.second()}")
    term = parseTerm(t)
    if debug: print("MOVING toward expressiong tail with ")
    if debug: t.print()
    tail = parseExpressionTail(t)
    if debug: print("Returning an Expression.")
    return Expression(term, tail)


def parseAssignment(t):
    '''<assignmentstatement> ::= "Let" <identifier> "be" <expression> "."'''
    if debug: print("in parseAssignment()")
    assert t.first() == "IDENTIFIER"
    #id_val = t.pop()
    id_ = parseOperant(t)
    if debug: print(f"Identifier {id_.printout()} parsed.")
    assert t.first() == "BE"
    t.pop()
    val = parseExpression(t)
    assert t.first() == "DOT", f"Expected DOT, got {t.first()}"
    t.pop()
    if debug: f"Returning assignment"
    return Assignment(id_, val)

def parseCommaList(t):
    '''<commalist> ::= "(" <operant> "," <commaidlist> ")"
              | <operant> '''
    if debug: print("Now in parseCommaList()")
    assert t.first() == 'LPAREN', f"Comma list starts with '(', instead got {t.first()}"
    t.pop()
    return_values = []
    while t.first() != 'RPAREN':
        if t.first() == "IDENTIFIER":
            new_id = t.pop()
            return_values.append(Identifier(new_id["value"]))
            if debug: print(f'Identifier {return_values[-1].printout()} added to parsing list')
        elif t.first() == "VAL":
            new_val = t.pop()
            return_values.append(Value(new_val["value"], typ=new_val["type"]))
            if debug: print(f'Value {return_values[-1].printout()} added to parsing list')
        else: raise SyntaxError(f"Only literal or identifier inside (...), found {t.first()}")
        assert t.first() in ["COMMA", 'RPAREN'], "This error should not happen, we checked this in the lexer"
        if t.first() in ["COMMA"]:
            t.pop()
    t.pop() # remove rparen
    if debug: print(f'Returning {[i.printout() for i in return_values]} from parseCommaList()')
    return return_values

        

def parseOperatorList(t):
    '''
    <operatorlist> ::= <operant> <operator> <operatorlist>
                    | <operant>
                    | <operator> <commaidlist> 
    '''
    if debug: print(f"in parseOperatorList(), first = {t.first()}")
    if t.first() in OPERANTS and t.second() != "OPER":
        if debug: print("goint to parseoperant")
        return parseOperant(t)
    elif t.first() == "OPER":
        op = t.pop()
        if debug: print("going to parse commalist and after returning new operatorcommalist")
        return OperatorCommalist(op["value"], parseCommaList(t))
    elif t.first() in OPERANTS and t.second() == "OPER":
        new_id = t.pop()
        if debug: print("returning new value plut continuih parsing")
        return Identifier(new_id["value"]), parseOperatorList(t)
    
    

def parsePrintStmt(t):
    '''<printstatement> ::= "Print" <identifierlist> "."'''
    if debug: print("in parsePrintStmt()")
    new_id = parseOperatorList(t)
    if t.first() == 'DOT':
        dot = t.pop()
        if debug: print(f"Returning a new printstatement")
        return PrintStatement(new_id)




def parseExecutionStatement(t):
    '''
     <executionstatement> ::= <assignmentstatement>
                            | <printstatement>
                            | <whilestatement>
                            | <loopstatement>
                            | <ifstatement>
                            | <functioncallstatement>
    '''
    if debug: print(f"parsing an Execution Statement, top of stream is {t.first()}")
    if t.first() == "LET":
        t.pop()
        return parseAssignment(t)
    elif t.first() == "PRINT":
        t.pop()
        return parsePrintStmt(t)
    elif t.first() == "WHILE":
        t.pop()
        return parseWhileStatement(t)
    elif t.first() == "FOR":
        t.pop()
        return parseForStatement(t)
    elif t.first() == "IF":
        t.pop()
        return parseIfStatement(t)
    elif t.first() == "MODIFY":
        t.pop()
        return parseFunctionCall(t)
    else:
        raise SyntaxError(f"I do not know what I'm doing")
    
def parseBlock(t):
    block = []
    while t.first() not in ["RETURN", "DONE"]:
        if token_stream.first == "FUNCTION":
            token_stream.pop()
            stmt = parseDefinitionStatement(token_stream)
        else:
            if debug: print(f'Parsing Execution inside Function definition, top of stream is {t.first()}')
            stmt = parseExecutionStatement(token_stream)
        if debug: print(f'appending inside function {stmt.printout()}')
        block.append(stmt)
        if debug: print(f'Appended, now stream first and second are {t.first()}, {t.second()}')
    return block

def parseForStatement(t):
    '''<loopstatement> ::= "For" <identifier> "in list" <operatorlist|identifier> "," <statementlist> "Done."'''
    if debug: print("In parseForStatement")
    new_id = parseOperant(t)
    assert isinstance(new_id, Identifier), "Non-identifier as loop argument."
    if debug: print("Looping variable parsed")
    assert t.first() == "IN" and t.second() == "LIST", "Loop not containing keywords 'in list'."
    t.pop(); t.pop()
    if t.first() == "IDENTIFIER":
        oplist = parseOperant(t)
    else:
        oplist = parseOperatorList(t)
    assert t.first() == "COMMA"
    t.pop()
    block = parseBlock(t)
    assert t.first() == "DONE" and t.second() == "DOT"
    t.pop(); t.pop()
    return ForStatement(new_id, oplist, block)

def parseIfStatement(t):
    expr = parseExpression(t)
    if debug: print(f'Extracted expression {expr.printout()}')
    assert t.first() == "IS" and t.second() == "TRUE", f'In if statement but "is true" not found. First = {t.first()}, second = {t.second()}'
    t.pop()
    t.pop()
    t.pop() # COMMA
    block = parseBlock(t)
    assert t.first() == "DONE" and t.second() == "DOT", f'If statement not ending in DONE., first = {t.first()}, second = {t.second()}.'
    t.pop()
    t.pop()
    if debug: print("Returning new IfStatment")
    return IfStatement(expr, block)

def parseWhileStatement(t):
    if debug: print("In parseWhileStatement")
    expr = parseExpression(t)
    if debug: print(f'Extracted expression {expr.printout()}')
    assert t.first() == "IS" and t.second() == "TRUE", f'In if statement but "is true" not found. First = {t.first()}, second = {t.second()}'
    t.pop()
    t.pop()
    t.pop() # COMMA
    block = parseBlock(t)
    assert t.first() == "DONE" and t.second() == "DOT", f'If statement not ending in DONE., first = {t.first()}, second = {t.second()}.'
    t.pop()
    t.pop()
    if debug: print("Returning new WhileStatement")
    return WhileStatement(expr, block)

def parseDefinitionStatement(t):
    '''
    <definitionstatement> ::= "function" <identifier> "acts on" <operatorlist> "," <statementlist> [ "return" <operatorlist> "." ] "Done."
    '''
    assert t.first() == "IDENTIFIER"
    new_id = t.pop()
    new_id = Identifier(new_id["value"])
    assert t.first() == "ACTS" and t.second() == "ON"
    t.pop()
    t.pop()
    opers = parseOperatorList(t)
    assert t.first() == "COMMA"
    t.pop()
    block = parseBlock(t)
    if t.first() == "RETURN":   # we have return value
        t.pop() # take return away
        return_value = parseOperatorList(t)
        t.pop(); t.pop(); t.pop()# take away dot and Done .
        if debug: print(f'Returning a new function definition')
        return FunctionDefinition(new_id, opers, block, return_values=return_value)
    t.pop(); t.pop(); t.pop() # Remove . and  Done .
    if debug: print(f'Returning a new function definition')
    return FunctionDefinition(new_id, opers, block)
    
    

test_snippet = """
Modify x with Function somename.
"""


test_snippet6 = """
function add_one acts on x,
return +(x,1).
Done.

Let x be 5.
Let y be and(x,1,1).
Let z be "hiya".
"""
test_snippet5="""
Let a be 1 and 2.
Let b be and(1,3).
"""
test_snippet2="""
Function somename acts on x,
Let x be x+1.
Return x.
Done.

Let x be 1.
Modify x with somename.
Print x. """
test_snippet3="""
Let c be +(1,1, "moi") - +(1,2).
Let x be -(1,2).
Print x.
"""

test_snippet_if = """
Let x be 1.
If x > 1 is true,
Let x be +(x,1).
Print x.
Done."""

test_snippet_for = """
For i in list x,
Print i.
Done."""

test_snippet4="Let x be -(0,1)."

token_stream = Lexer().tokenize(test_snippet_for)
token_stream.print()


StatementList= []
while token_stream.size() > 0:
    if token_stream.first() == "FUNCTION":
        token_stream.pop()
        t = parseDefinitionStatement(token_stream)
    else:
        t = parseExecutionStatement(token_stream)
    if debug: print(f'appending {t.printout()}')
    StatementList.append(t)


print("\nRESULT:")
print("---------My language-----------")
for p in StatementList:
    print(p.printout(), end="")
print("-----------Python--------------")
for p in StatementList:
    print(p.translate(), end="")
print("-------------------------------")