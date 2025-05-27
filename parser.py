from lexer import Lexer

class Parser:
    def __init__(self, debug=False):
        self.lexer = Lexer()
        self.OPERANTS = ["IDENTIFIER", "VAL", "MODIFY"]
        self.program = []
        self.debug = debug

    def tokenize(self, t):
        return self.lexer.tokenize(t)

    def parse(self, p):
        token_stream = self.tokenize(p)
        StatementList = []
        while token_stream.size() > 0:
            if token_stream.first() == "FUNCTION":
                token_stream.pop()
                t = self.parseDefinitionStatement(token_stream)
            else:
                t = self.parseExecutionStatement(token_stream)
            if self.debug:
                print(f'appending {t.printout()}')
            StatementList.append(t)
        self.program = StatementList

    def get_ast(self):
        return self.program

    def print_program(self):
        StatementList = parser.get_ast()
        for p in StatementList:
            print(p.printout(), end="")

    def translate_program(self):
        StatementList = parser.get_ast()
        for p in StatementList:
            print(p.translate(), end="")
        

    def parseOperant(self, t):
        if self.debug:
            print(f'In parseOperant() with {t.first()}')
        if t.first() == "IDENTIFIER":
            if self.debug:
                print(f'In parseOperant(), identifier found')
            new_id = t.pop()
            return Identifier(new_id["value"])
        elif t.first() == "MODIFY":
            if self.debug:
                print(f'In parseOperant(), function call found')
            t.pop()
            return self.parseFunctionCall(t)
        elif t.first() == "VAL":
            if self.debug:
                print(f"In parseOperant(), Value found {t.first()}")
            val = t.pop()
            return Value(val["value"], typ=val["type"])
        raise SyntaxError("Should not reach this, parseOperant with no operant in sight.")

    def parseFunctionCall(self, t):
        if self.debug:
            print("Now in parseFuntionCall()")
        params = self.parseOperatorList(t)
        assert t.first() == "WITH"
        if t.second() == "FUNCTION":
            t.pop()
        t.pop()
        function_name = self.parseOperant(t)
        assert t.first() == "DOT"
        t.pop()
        return FunctionCall(function_name, params)

    def parseExpression(self, t):
        def parseExpressionTail(t):
            if self.debug:
                print(f"In expression tail, first = {t.first()}")
            if t.first() == "OPER" and t.second() != "LPAREN":
                oper = t.pop()
                term = parseTerm(t)
                tail = parseExpressionTail(t)
                if self.debug:
                    print(f'Returning expressiontail with {oper["value"]}, {term.printout()}')
                return ExpressionTail(oper["value"], term, tail)
            if t.first() == "OPER" and t.second() == "LPAREN":
                oper = t.pop()
                return OperatorCommalist(oper["value"], t)

        def parseTerm(t):
            if self.debug:
                print(f"in parseTerm() with {t.first()}")
            if t.first() == "MODIFY":
                return self.parseFunctionCall(t)
            elif t.first() == "OPER":
                return self.parseOperatorList(t)
            elif t.first() in self.OPERANTS:
                return self.parseOperant(t)
            raise SyntaxError("In parseTerm() without a term.")

        if self.debug:
            print(f"Now in parseExpression, first token = {t.first()}, second token = {t.second()}")
        term = parseTerm(t)
        if self.debug:
            print("MOVING toward expressiong tail with ")
        tail = parseExpressionTail(t)
        if self.debug:
            print("Returning an Expression.")
        return Expression(term, tail)

    def parseAssignment(self, t):
        if self.debug:
            print("in parseAssignment()")
        assert t.first() == "IDENTIFIER"
        id_ = self.parseOperant(t)
        if self.debug:
            print(f"Identifier {id_.printout()} parsed.")
        assert t.first() == "BE"
        t.pop()
        val = self.parseExpression(t)
        assert t.first() == "DOT", f"Expected DOT, got {t.first()}"
        t.pop()
        return Assignment(id_, val)

    def parseCommaList(self, t):
        if self.debug:
            print("Now in parseCommaList()")
        assert t.first() == 'LPAREN'
        t.pop()
        return_values = []
        while t.first() != 'RPAREN':
            if t.first() == "IDENTIFIER":
                new_id = t.pop()
                return_values.append(Identifier(new_id["value"]))
                if self.debug:
                    print(f'Identifier {return_values[-1].printout()} added to parsing list')
            elif t.first() == "VAL":
                new_val = t.pop()
                return_values.append(Value(new_val["value"], typ=new_val["type"]))
                if self.debug:
                    print(f'Value {return_values[-1].printout()} added to parsing list')
            else:
                raise SyntaxError(f"Only literal or identifier inside (...), found {t.first()}")
            if t.first() in ["COMMA"]:
                t.pop()
        t.pop()
        return return_values

    def parseOperatorList(self, t):
        if self.debug:
            print(f"in parseOperatorList(), first = {t.first()}")
        if t.first() in self.OPERANTS and t.second() != "OPER":
            return self.parseOperant(t)
        elif t.first() == "OPER":
            op = t.pop()
            return OperatorCommalist(op["value"], self.parseCommaList(t))
        elif t.first() in self.OPERANTS and t.second() == "OPER":
            new_id = t.pop()
            return Identifier(new_id["value"]), self.parseOperatorList(t)

    def parsePrintStmt(self, t):
        if self.debug:
            print("in parsePrintStmt()")
        new_id = self.parseOperatorList(t)
        if t.first() == 'DOT':
            t.pop()
            return PrintStatement(new_id)

    def parseExecutionStatement(self, t):
        if self.debug:
            print(f"parsing an Execution Statement, top of stream is {t.first()}")
        if t.first() == "LET":
            t.pop()
            return self.parseAssignment(t)
        elif t.first() == "PRINT":
            t.pop()
            return self.parsePrintStmt(t)
        elif t.first() == "WHILE":
            t.pop()
            return self.parseWhileStatement(t)
        elif t.first() == "FOR":
            t.pop()
            return self.parseForStatement(t)
        elif t.first() == "IF":
            t.pop()
            return self.parseIfStatement(t)
        elif t.first() == "MODIFY":
            t.pop()
            return self.parseFunctionCall(t)
        else:
            raise SyntaxError("Unknown execution statement")

    def parseBlock(self, t):
        block = []
        while t.first() not in ["RETURN", "DONE"]:
            if t.first() == "FUNCTION":
                t.pop()
                stmt = self.parseDefinitionStatement(t)
            else:
                if self.debug:
                    print(f'Parsing Execution inside Function definition, top of stream is {t.first()}')
                stmt = self.parseExecutionStatement(t)
            if self.debug:
                print(f'appending inside function {stmt.printout()}')
            block.append(stmt)
        return block

    def parseForStatement(self, t):
        if self.debug:
            print("In parseForStatement")
        new_id = self.parseOperant(t)
        assert isinstance(new_id, Identifier)
        assert t.first() == "IN" and t.second() == "LIST"
        t.pop(); t.pop()
        if t.first() == "IDENTIFIER":
            oplist = self.parseOperant(t)
        else:
            oplist = self.parseOperatorList(t)
        assert t.first() == "COMMA"
        t.pop()
        block = self.parseBlock(t)
        assert t.first() == "DONE" and t.second() == "DOT"
        t.pop(); t.pop()
        return ForStatement(new_id, oplist, block)

    def parseIfStatement(self, t):
        expr = self.parseExpression(t)
        if self.debug:
            print(f'Extracted expression {expr.printout()}')
        assert t.first() == "IS" and t.second() == "TRUE"
        t.pop(); t.pop(); t.pop()
        block = self.parseBlock(t)
        assert t.first() == "DONE" and t.second() == "DOT"
        t.pop(); t.pop()
        return IfStatement(expr, block)

    def parseWhileStatement(self, t):
        if self.debug:
            print("In parseWhileStatement")
        expr = self.parseExpression(t)
        if self.debug:
            print(f'Extracted expression {expr.printout()}')
        assert t.first() == "IS" and t.second() == "TRUE"
        t.pop(); t.pop(); t.pop()
        block = self.parseBlock(t)
        assert t.first() == "DONE" and t.second() == "DOT"
        t.pop(); t.pop()
        return WhileStatement(expr, block)

    def parseDefinitionStatement(self, t):
        assert t.first() == "IDENTIFIER"
        new_id = Identifier(t.pop()["value"])
        assert t.first() == "ACTS" and t.second() == "ON"
        t.pop(); t.pop()
        opers = self.parseOperatorList(t)
        assert t.first() == "COMMA"
        t.pop()
        block = self.parseBlock(t)
        if t.first() == "RETURN":
            t.pop()
            return_value = self.parseOperatorList(t)
            t.pop(); t.pop(); t.pop()
            return FunctionDefinition(new_id, opers, block, return_values=return_value)
        t.pop(); t.pop(); t.pop()
        return FunctionDefinition(new_id, opers, block)




class Identifier:
    def __init__(self, name):
        self.name = name
    def printout(self):
        return self.name
    def translate(self):
        return self.name


class Value:
    def __init__(self, val, typ="STRING"):
        value_map = {"STRING": str,
             "INT": int,
             "FLOAT": float,
             }
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
            return f'{self.oper}{self.term.printout()}'
        else:
            return f'{self.oper}{self.term.printout()}{self.tail.printout()}'
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
            return f"{self.term.printout()}{self.tail.printout()}"
    def translate(self):
        if self.tail is None:
            return f"{self.term.translate()}"
        else:
            if self.tail.oper == "and":
                return f'[{self.term.translate()}{self.tail.translate()}'
            return f"{self.term.translate()}{self.tail.translate()}"

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

class Block:
    def __init__(self, block):
        self.block = block
    def len(self):
        return len(self.block)
    def printout(self):
        func = lambda x: x.printout()
        return_str = ""
        for b in self.block:
            return_str += str(func(b))
        return return_str
    def translate(self):
        func = lambda x: x.translate()
        return_str = ""
        for b in self.block:
            return_str += "\t" + str(func(b))
        return return_str

    

class IfStatement:
    def __init__(self, expr, block):
        assert isinstance(expr, Expression)
        self.expr = expr
        self.block = Block(block)
    def printout(self):
        return f"If {self.expr.printout()} is true,\n{self.block.printout()}Done.\n"
    def translate(self):
        return f"if {self.expr.translate()}:\n{self.block.translate()}"

class WhileStatement:
    def __init__(self, expr, block):
        assert isinstance(expr, Expression)
        self.expr = expr
        self.block = Block(block)
    def printout(self):
        return f"""While {self.expr.printout()} is true,
{self.block.printout()}Done.
"""
    def translate(self):
        return f"""While {self.expr.translate()}:
{self.block.translate()}"""

class ForStatement:
    def __init__(self, looper, loopee, block):
        self.looper = looper
        self.loopee = loopee
        self.block = Block(block)
    def printout(self):
        return f"""For {self.looper.printout()} in list {self.loopee.printout()},
{self.block.printout()}Done.
"""
    def translate(self):
        return f"""for {self.looper.translate()} in {self.loopee.translate()}:
{self.block.translate()}
"""
        

class FunctionCall:
    def __init__(self, name, params):
        assert isinstance(name, Identifier)
        self.name=name
        self.params=params
    def printout(self):
        return f'Modify {self.params.printout()} with function {self.name.printout()}.'
    def translate(self):
        return f'{self.name.translate()}({self.params.translate()})'
        

class FunctionDefinition:
    def __init__(self, name, params, block, return_values=None):
        self.name = name
        self.params = params
        self.block = Block(block)
        self.return_values = return_values
    def printout(self):
        if self.return_values:
            return f'Function {self.name.printout()} acts on {self.params.printout()},{self.block.printout()}{"Done." if self.block.len()>0 else ""}\nReturn {self.return_values.printout()}.\nDone.\n'
        else:
            return f"Function {self.name.printout()} acts on {self.params.printout()},{self.block.printout()}Done.\n"
    def translate(self):
        if self.return_values:
            return f'def {self.name.translate()}({self.params.translate()}):{self.block.translate()}\n\treturn {self.return_values.translate()}\n'
        else:
            return f'def {self.name.translate()}({self.params.translate()}):{self.block.translate()}\n'





if __name__=="__main__":
    test_snippet4="Let x be -(0,1)."

    test_snippet_all ="""
    Function add_one acts on x,
    Return +(x,1).
    Done.

    Let x be 5.
    Let y be and(x,1,1).
    Let z be "hiya".

    For i in list y,
    If i > 1 is true,
    Print i.
    Done.
    If i == 1 is true,
    Modify i with Function add_one.
    Done.
    Done.

    Let x be 1.
    While x == 1 is true,
    Let x be +(x,1).
    Done.
    """
    test_snippet_if = """
    Let x be 1.
    If x > 1 is true,
    Let x be +(x,1).
    Print x.
    Done.
    Print "Done!".
    """

    parser = Parser()
    parser.parse(test_snippet_all)

    parser.print_program()
    print("---------------")
    parser.translate_program()