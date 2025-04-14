# Introduction

This grammar is inspired by Toki Pona, a conlang by Sonja Lang. Toki Pona features, depending 
on the source, 120-140 words, and the main philosophy of the language is simplicity, in
pronounciation, vocab, and grammar. 

See [a toki pona cheat-sheet](https://jansa-tp.github.io/tpcheatsheet/Toki%20Pona%20Cheat%20Sheet%20v2.pdf)

## Basic sentence structure:

``(en*) subject (en subject2) li verb (e object) (e object2).``

or

``(en*) subject (en subject2) li adjective.``

The first subject marker ``en*`` is omitted always, but in theory, it is there. The copula li is omitted if subject is ``mi`` (me), ``sina`` (you).

## Modifiers: 

Modifiers come after the word they are modifying

``jan lili`` : ``jan`` human, ``lili`` small, together small human, or a child.

Negation ``ala`` works the same;

``jan ala li toki``: no person is talking

With more than one modifier ``pi`` can be used. It can also be thought that ``pi`` is just omitted in the above examples.

## Context / if

``la`` is used to describe "in the context of" and works like if, but can also be used in the more general sense.

``mi lape la ali li pona`` In the context of me sleeping, everything is good == Everything will be better if I sleep.

``tempo pini la mi lape`` In the context of past, I sleep == I slept.


# Thinking part

what features we want?

- simplicity: negation does a lot, but only applies to keywords. e.g. subtraction is negation+summing
- numeric: only binary accepted
- basic types: int, float, string/char, array, bool, dict, None
    - boolean: Not needed, really? you can make xor with + and modulo, and that with negation is enough

keywords
- summation: is multiplication just summation many times
    - same for exponents :D
- if, then else
    - as toki pona does not have the context of "else", thus we must check if (condition) then ... done if negative (contidition) then ... done
    - <id> la <expression> pini
    - <id> ala la <expression> pini
- assignment: nimi value li variable 
- loops: nasin <id> la, <block> pini!

```python
def add_one(x):
    return x+1

x = 5
y = [x,1,1]
for i in y:
    if i > 2:
        print(i)
    else:
        x = add_one(x)
print(x)
```

```
ilo add_one li pali e x,
    pana +(x,1).    # or x+1
pini!

nimi 101 li x.
nimi en(x,1,1) li y.   # or x en 1 en 1
i lon nasin y la,
    i pi sama mute 10 la,
        o toki i.
    pini.
    i pi sama mute ala 10 la,
        o ante x kepeken add_one.
    pini.
pini.
```
```
funtion add_one acts on x,
    return +(x,1).
Done.

Let x be 5.
Let y be (x,1,1)
i in list,
    if i > 0:
        print i.
    Done.
    if i<=0:
        Modify i with function add_one.
    Done.
Done.

```

# Grammar

```bnf

<program> ::= <statementlist>

<statementlist> ::= <statement> <statementlist>
                  | ε

<statement> ::= <definitionstatement>
              | <executionstatement>

<definitionstatement> ::= "function" <identifier> "acts on" <operatorlist> "," <statementlist> [ "return" <operatorlist> "." ] "Done."


<executionstatement> ::= <assignmentstatement>
                       | <printstatement>
                       | <whilestatement>
                       | <loopstatement>
                       | <ifstatement>
                       | <functioncallstatement>

<assignmentstatement> ::= "Let" <identifier> "be" <expression> "."
<printstatement> ::= "Print" <operatorlist> "."
<whilestatement> ::= "While" <expression> "is true," <statementlist> "Done."
<loopstatement> ::= "For" <identifier> "in list" <operatorlist|identifier> "," <statementlist> "Done."
<ifstatement> ::= "If" <expression> "is true," <statementlist> "Done."
<functioncallstatement> ::= "Modify" <operatorlist> "with function" <identifier> "."

<expression> ::= <term> <expression_tail>
<term> ::= <functioncallstatement>
         | <operatorlist>
         | <operant>
<expression_tail> ::= <operator> <term> <expression_tail>
                    | ε

<operatorlist> ::= <operant> <operator> <operatorlist>
                 | <operant>
                 | <operator> <commaidlist> 

<commalist> ::= "(" <operant> "," <commaidlist> ")"
              | <operant> 
<operant> :: <literal> | <identifier | <functioncallstatement>

<operator> ::= "+" | "-" | "*" | "/" | "&" | "|" | "==" | ">" | "<" | "and" 
<identifier> ::= [a-zA-Z][a-zA-Z0-9_]*
<intval> ::= [0-9]+
<floatval> ::= [0-9]+"."[0-9]+
<stringval> ::= "\"" .*? "\""
<literal> ::= <intval> | <floatval> | <stringval>

```


## Ideas

    #<expressionlist> ::= <expression> "and" <expressionslist>
    #                   | <expression>






