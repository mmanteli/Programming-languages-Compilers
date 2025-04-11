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
    def __init__(self, id, val):
        self.id = id
        self.value = val
    def printout(self):
        return f"Let {self.id.printout()} be {self.value.printout()}.\n"
    def translate(self):
        return f"{self.id.printout()} == {self.value.printout()}\n"

class IdentifierList:
    pass

class PrintStatement:
    def __init__(self, val):
        self.val = val
    def printout(self):
        return f"Print {self.val.printout()}.\n"
    def translate(self):
        return f"print({self.val.printout()})\n"



def parseExpression(t):
    return None

def parseAssignment(t):
    '''<assignmentstatement> ::= "Let" <identifier> "be" <expression> "." '''
    if debug: print("in parseAssignment")
    assert t.first() == "IDENTIFIER"
    id = t.pop(0)
    assert t.first() == "BE"
    t.pop(0)
    val = parseExpression(t)
    return Assignment(id, val)


def parseIdentifierList(t):
    '''<identifierlist> ::= <identifier> "and" <identifierlist>
                   | <identifier>
                   | "and" "(" <commaidlist> ")"'''
    if debug: print("in parseIdentifierList()")
    if t.first() == 'IDENTIFIER' and t.second() != "AND":   # we only have one identifier
        new_id = t.pop()
        return Identifier(new_id["value"])
    

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
Print x."""

token_stream = Lexer().tokenize(test_snippet2)

parsed = []
while token_stream.size() > 0:
    if debug: print("At the start with")
    if debug: token_stream.print()
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
print(parsed[0].printout())
print(parsed[0].translate())
