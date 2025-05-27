import re

class TokenStream:
    def __init__(self, t, l):
        self.stream = t
        self.lines = l
    def first(self):
        return self.stream[0]["token"]
    def second(self):
        return self.stream[1]["token"]
    def line(self):
        return self.stream[0]["line"]
    def get_row(self, r):
        return self.lines[r]
    def num_rows(self):
        return len(self.lines)
    def pop(self):
        val = self.stream.pop(0)
        return val
    def print(self):
        print(self.stream)
    def size(self):
        return len(self.stream)

class Lexer:
# this dict and the list below was done using ChatGPT
# as I did not bother to make such a long list myself
    def __init__(self):

        self.TOKENS = {
            'FUNCTION':    r'\bFunction\b',
            'ACTS':        r'\bacts\b',
            'ON':          r'\bon\b',
            'RETURN':      r'\bReturn\b',
            'DONE':        r'\bDone\b',
            'LET':         r'\bLet\b',
            'BE':          r'\bbe\b',
            'PRINT':       r'\bPrint\b',
            'WHILE':       r'\bWhile\b',
            'IS':          r'\bis\b',
            'TRUE':        r'\btrue\b',
            'FOR':         r'\bFor\b',
            'IN':          r'\bin\b',
            'LIST':        r'\blist\b',
            'IF':          r'\bIf\b',
            'MODIFY':      r'\bModify\b',
            'WITH':        r'\bwith\b',
            'AND':         r'\band\b',
            'AND_OP':      r'&&',
            'OR_OP':       r'¤¤',
            'EQEQ':        r'==',
            'GT':          r'>',
            'LT':          r'<',
            'PLUS':        r'\+',
            'MINUS':       r'-',
            'MULT':        r'\*',
            'DIV':         r'/',
            'BITAND':      r'&',
            'BITOR':       r'¤',
            'LPAREN':      r'\(',
            'RPAREN':      r'\)',
            'COMMA':       r',',
            'DOT':         r'\.',
            'FLOAT':       r'\d+\.\d+',
            'INT':         r'\d+',
            'STRING':      r'\"([^"\\]|\\.)*\"', 
            'IDENTIFIER':  r'[a-zA-Z_][a-zA-Z0-9_]*',
            'WHITESPACE':  r'[ \t\n]+',  # ignored
            'COMMENT':     r'\#.*', # not yet in grammar
        }

        self.TOKEN_TYPES = {
            'AND_OP':      "OPER",
            'OR_OP':       "OPER",
            'EQEQ':        "OPER",
            'GT':          "OPER",
            'LT':          "OPER",
            'PLUS':        "OPER",
            'MINUS':       "OPER",
            'MULT':        "OPER",
            'DIV':         "OPER",
            'BITAND':      "OPER",
            'BITOR':       "OPER",
            'AND':         "OPER",
            'FLOAT':       "VAL",
            'INT':         "VAL",
            'STRING':      "VAL",
        }
        self.ordered_token_names = [i for i in self.TOKENS.keys()]

        token_regex = '|'.join(
            f'(?P<{name}>{self.TOKENS[name]})' for name in self.ordered_token_names
        )
        self.matcher = re.compile(token_regex)



    def tokenize(self, snippet):

        # initialize score keepers and return value
        line_in_code = 0
        last_index_covered = 0
        parenthesis_check = 0
        parenthesis_location = []
        tokens_to_forward = []
        lines = snippet.split("\n")

        # loop over segments that match rules (everything should match some rule!)
        for i in self.matcher.finditer(snippet):
            matched_segment, location, token_rule_name = i.group(),i.span(), i.lastgroup
            token = self.TOKEN_TYPES.get(token_rule_name, token_rule_name)

            # check for errors
            # unrecognized segment was found:
            if not location[0] == last_index_covered: raise SyntaxError(f'Segment "{snippet[last_index_covered:location[0]]}" not recognized on line {line_in_code}:  {lines[line_in_code]} ')
            last_index_covered = location[1]

            # period or comma missing after \n (not in string)
            if "\n" in matched_segment:
                if tokens_to_forward != []:
                    if not tokens_to_forward[-1]["token"] in ["DOT", "COMMA"]: raise SyntaxError(f'Missing "." or "," on line {line_in_code}: {lines[line_in_code]} .')
            # parenthesis error
            if token in ["LPAREN", "RPAREN"]:
                if token == "LPAREN":
                    parenthesis_check += 1 # next RPAREN puts this back to zero
                    parenthesis_location.append(line_in_code)
                else:
                    parenthesis_check -=1
                    if not parenthesis_check>=0: raise SyntaxError(f'Unclosed parenthesis on line {line_in_code}: {lines[line_in_code]} ')
                    parenthesis_location.pop(-1)
            if token in ["DOT"]:
                if not parenthesis_check == 0: raise SyntaxError(f'Unclosed parenthesis on line {line_in_code}: {lines[line_in_code]} ')

            # put token to return value if no errors are present
            if token not in ["WHITESPACE", "COMMENT"]:
                tokens_to_forward.append(dict(token=token, type=token_rule_name, value=matched_segment, span=location, line=line_in_code))
            # move the line number for error reporting when needed
            if "\n" in matched_segment:
                line_in_code += matched_segment.count("\n")

        if not parenthesis_check == 0: raise SyntaxError(f'Unclosed parenthesis on line(s) {",".join([str(i) for i in parenthesis_location])}.')

        return TokenStream(tokens_to_forward, lines)

if __name__=="__main__":
    lexer = Lexer()
    test_snippet = """
    function add_one acts on x,
    return +(x,1).
    Done.

    Let x be 5.
    Let y be and(x,1,1).
    Let z be "hiya".

    For i in list y,
        if i > 1,
            print i.
        Done.
        if i<1 or i==1,
            Modify i with function add_one.
        Done.
    Done.

    Let x be 1.
    While x == 1,
    Let x be +(x,1).
    Done.
    """
    result = lexer.tokenize(test_snippet)
    #result.print()
    print("")
    print(result.first())
    first_val = result.pop()
    print(first_val)
    print("")
    result.print()