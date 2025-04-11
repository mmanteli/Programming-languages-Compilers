from lexer import Lexer

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
class Assignment:
    def __init__(self, id, val):
        self.id = id
        self.value = val
    def printout(self):
        print(f"Let {self.id} be {self.value}.\n")
    def translate(self):
        print(f"{self.id} == {self.value}\n")
    
class IdentifierList:
    pass

class PrintStatement:
    pass


def parseExpression(t):
    return None

def parseAssignment(t):
    '''<assignmentstatement> ::= "Let" <identifier> "be" <expression> "." '''
    assert t.first == "IDENTIFIER"
    id = t.pop(0)
    assert t.first == "BE"
    t.pop(0)
    val = parseExpression(t)
    return Assignment(id, val)

def parseIdentifierList(t):
    if t.first in ["+"]:
        pass

def parsePrintStmt(t):
    '''<printstatement> ::= "Print" <identifierlist> "."'''
    t = parseIdentifierList(t)


test_snippet = """
function add_one acts on x,
return +(x,1).
Done.

Let x be 5.
Let y be and(x,1,1).
Let z be "hiya".
"""

test_snippet2="Print x."

token_stream = Lexer().tokenize(test_snippet2)


while len(token_stream) > 0:
    if token_stream.first == "LET":
        token_stream.pop()
        parseAssignment(token_stream)
    elif token_stream.first == "PRINT":
        token_stream.pop()
        parsePrintStmt(token_stream)
    else:
        raise SyntaxError(f"I do not know what I'm doing")
