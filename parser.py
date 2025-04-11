from lexer import Lexer
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

class Assignment:
    def __init__(self, id_, val):
        assert isinstance(id_, Identifier), "Tried to make non-identifier left in assignment"
        self.id = id_
        assert isinstance(val, Value) or isinstance(val, Identifier) or isinstance(val, OperatorCommalist), f"Assigning non-value ({val.printout()}) to an identifier"
        self.value = val
    def printout(self):
        return f"Let {self.id.printout()} be {self.value.printout()}.\n"
    def translate(self):
        return f"{self.id.translate()} = {self.value.translate()}\n"

class IdentifierList:
    pass

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

def parseFunctionCall(t):
    if debug: print("Now in parseFuntionCall()")
    pass

def parseTerm():
    pass

def parseExpression(t):
    ''' <expression> ::= <term> <expression_tail>
        <term> ::= <functioncall>
                | <identifier>
                | <literal>
                # | "[" <expression> "]"
        <expression_tail> ::= <operator> <term> <expression_tail>
                            | ε'''
    if debug: print(f"Now in parseExpression, first token = {t.first()}")
    if t.first() == "VAL":
        if t.second != "OPER":
            val = t.pop()
            return Value(val["value"])
        else:
            pass
    if t.first() == "IDENTIFIER" and t.second() not in ["AND", "OPERATOR"]:
        val = t.pop()
        return Identifier(val["value"])
    elif t.first() == "MODIFY":
        t.pop()
        return parseFunctionCall()
    elif t.first() == "OPER" and t.second() == 'LPAREN':
        op = t.pop()
        return OperatorCommalist(op["value"], parseCommaList(t))

def parseAssignment(t):
    '''<assignmentstatement> ::= "Let" <identifier> "be" <expression> "." '''
    if debug: print("in parseAssignment()")
    assert t.first() == "IDENTIFIER"
    id_val = t.pop()
    id_ = Identifier(id_val["value"])
    if debug: print(f"Identifier {id_.printout()} parsed.")
    assert t.first() == "BE"
    t.pop()
    val = parseExpression(t)
    if debug: print(f"Value {val.printout()} parsed.")
    assert t.first() == "DOT"
    t.pop()
    #print(id_val["value"], val)
    print(f"HERE HERE {type(val)}")
    return Assignment(id_, val)

def parseCommaList(t):
    '''<commaidlist> ::= <literal|identifier> "," <commaidlist>
                | <literal|identifier>'''
    '''Here we have the parenthesis as well even if they are
       actually associated with OperatorList and ExpressionList'''
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

        

def parseIdentifierList(t):
    '''<identifierlist> ::= <identifier> "and" <identifierlist>
                   | <identifier>
                   | "and" "(" <commaidlist> ")"'''
    if debug: print("in parseIdentifierList()")
    if t.first() == 'IDENTIFIER' and t.second() != "AND":   # we only have one identifier
        new_id = t.pop()
        return Identifier(new_id["value"])
    elif t.first() == "and":
        and_ = t.pop(0)
        return OperatorCommalist(and_, parseCommaList(t))
    elif t.first() == 'IDENTIFIER' and t.second() == "AND":
        new_id = t.pop()
        return Identifier(new_id), parseIdentifierList(t)
    
    

def parsePrintStmt(t):
    '''<printstatement> ::= "Print" <identifierlist> "."'''
    if debug: print("in parsePrintStmt()")
    new_id = parseIdentifierList(t)
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
Let c be +(1,1).
Let a be 1+1.
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