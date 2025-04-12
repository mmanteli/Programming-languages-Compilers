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

class Value:
    def __init__(self, val):
        self.val = val
    def printout(self):
        return self.val
    def translate(self):
        return self.val
    
class ExpressionTail:
    def __init__(self, oper, term, tail):
        assert oper is not None, "No operator given for ExpressionTail"
        assert term is not None, "No term given for ExpressionTail"
        self.oper = oper
        self.term = term
        self.tail = tail
        print(f"Doing a expression tail. Values were of type \n {type(self.oper)}, \n {type(self.term)}, \n {type(self.tail)}")
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
        return Value(val["value"])
    print("SHould not be here")

def parseFunctionCall(t):
    if debug: print("Now in parseFuntionCall()")
    # "modify" should be removed already
    assert t.first() == "MODIFY", "tried parsefunctioncall without modify"
    values = parseOperatorList(t)

    pass



    

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
        if t.first() == "OPER" and t.second() is not "LPAREN":
            oper = t.pop()
            term = parseTerm(t)
            tail = parseExpressionTail(t)
            if debug: print(f'Returning expressiontail with {oper["value"]}, {term.printout()}')
            return ExpressionTail(oper["value"], term, tail)
        if t.first() == "OPER" and t.second() == "LPAREN":
            oper = t.pop()
            return OperatorCommalist(oper["value"], t)

    def parseTerm(t):
        print(f"in parseTerm() with {t.first()}")
        if t.first() == "MODIFY":
            return parseFunctionCall(t)
        elif t.first() == "OPER":
            return parseOperatorList(t)
        elif t.first() in OPERANTS:
            return parseOperant(t)
        print(f'Should not be here!!')
        
    if debug: print(f"Now in parseExpression, first token = {t.first()}, second token = {t.second()}")
    term = parseTerm(t)
    print("WE HERE?")
    print(f"{term.printout()}")
    print("MOVING toward expressiong tail with ")
    t.print()
    print("")
    print("NEXT LINE SHOULD BE PARSING TAIL WHY IS IT NOT")
    tail = parseExpressionTail(t)
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
    print("WE MADE IT BOYTS")
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
            return_values.append(Value(new_val["value"]))
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


test_snippet = """
function add_one acts on x,
return +(x,1).
Done.

Let x be 5.
Let y be and(x,1,1).
Let z be "hiya".
"""
test_snippet2="""
Let a be 1 and 2.
Let b be and(1,3).
"""
test_snippet3="""
Let c be +(1,1, "moi") - +(1,2).
Let x be -(1,2).
Print x.
"""

token_stream = Lexer().tokenize(test_snippet2)

parsed = []
while token_stream.size() > 0:
    if debug: print("New round, baby")
    #if debug: token_stream.print()
    if token_stream.first() == "LET":
        token_stream.pop()
        t = parseAssignment(token_stream)
    elif token_stream.first() == "PRINT":
        token_stream.pop()
        t = parsePrintStmt(token_stream)
    else:
        raise SyntaxError(f"I do not know what I'm doing")
    print(f'appending {t.printout()}')
    parsed.append(t)


print("RESULT FINALLY HERE WOO")
print("---------My language-----------")
for p in parsed:
    print(p.printout(), end="")
print("-----------Python--------------")
for p in parsed:
    print(p.translate(), end="")
print("-------------------------------")