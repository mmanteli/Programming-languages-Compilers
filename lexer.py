import re
import sys


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
Let x be 5.
Let y be (x,1,1).
Let z be "hiya".

For i in list,
    if i > 1,
        print i.
    Done.
    if i<1 or i==1,
        Modify i with function add_one.
    Done.
Done.
"""

print(ordered_token_names[37-1])

def analyze_tuple(t):
    non_empty_indices = [i for i, val in enumerate(t) if val != ""]
    count = len(non_empty_indices)
    index = non_empty_indices[0] if count == 1 else None
    if count == 1:
        value = [val for i, val in enumerate(t) if val != ""][0]
    else:
        value = None
    return count, index, value

line_in_code = 0
last_index_covered = 0

tokens_to_forward = []
for i in matcher.finditer(test_snippet):
    matched_segment, location, token = i.group(),i.span(), i.lastgroup
    print(matched_segment, location, token)

    # check for errors
    # unrecognized segment was found:
    assert location[0] == last_index_covered, f'Syntax error on line {line_in_code}, segment "{test_snippet[last_index_covered:location[0]]}" not recognized.'
    last_index_covered = location[1]

    if token not in ["WHITESPACE", "COMMENT"]:
        tokens_to_forward.append(dict(token=token, value=matched_segment, span=location, line=line_in_code))

    if matched_segment == "\n":
        line_in_code +=1
    #print(f"NOW IN INDEX {last_index_covered}")
    #print(matched_segment, location, token)

    #count, index, value = analyze_tuple(i)
    #assert count==1, "Syntax error at NOT IMPLEMENTED"
    #print(ordered_token_names[index], value)

#for k, v, r in zip(TOKENS.keys(), ordered_token_names, token_regex.split("|")):
#    print(k, v, r)

print(tokens_to_forward)

