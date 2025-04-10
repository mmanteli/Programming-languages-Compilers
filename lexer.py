import re


# this dict and the list below was done using ChatGPT
# as I did not bother to make such a long list myself
TOKENS = {
    'FUNCTION':    r'\bfunction\b',
    'ACTS':        r'\bacts\b',
    'ON':          r'\bon\b',
    'RETURN':      r'\breturn\b',
    'DONE':        r'\bDone\.\b',
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
    'COMMENT':     r'\¤.*',
}

ordered_token_names = [i for i in TOKENS.keys()]

token_regex = '|'.join(
    f'(?P<{name}>{TOKENS[name]})' for name in ordered_token_names
)
matcher = re.compile(token_regex)

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

line_in_code = 0
last_index_covered = 0
parenthesis_check = 0
parenthesis_location = []
tokens_to_forward = []
for i in matcher.finditer(test_snippet):
    #print(f'LINE IN CODE {line_in_code}')
    matched_segment, location, token = i.group(),i.span(), i.lastgroup
    #print(matched_segment)

    # check for errors
    # unrecognized segment was found:
    assert location[0] == last_index_covered, f'Syntax error on line {line_in_code}, segment "{test_snippet[last_index_covered:location[0]]}" not recognized.'
    last_index_covered = location[1]

    # period or comma in the end of line:
    if "\n" in matched_segment:
        if tokens_to_forward != []:
            assert tokens_to_forward[-1]["token"] in ["DOT", "COMMA"], f'Syntax error on line {line_in_code}, missing "." or ",".'
    # parenthesis error
    if token in ["LPAREN", "RPAREN"]:
        if token == "LPAREN":
            parenthesis_check += 1
            parenthesis_location.append(line_in_code)
        else:
            parenthesis_check -=1
            assert parenthesis_check>=0, f'Syntax error on line {line_in_code}, unclosed parenthesis ")".'
            parenthesis_location.pop(-1)
    if token in ["DOT"]:
        assert parenthesis_check == 0, f'Syntax error on line {line_in_code}, missing parenthesis ")"'

    if token not in ["WHITESPACE", "COMMENT"]:
        tokens_to_forward.append(dict(token=token, value=matched_segment, span=location, line=line_in_code))

    if "\n" in matched_segment:
        line_in_code += matched_segment.count("\n")

assert parenthesis_check == 0, f'Syntax error, unclosed parenthesis on line(s) {",".join([str(i) for i in parenthesis_location])}.'

print(tokens_to_forward)

