# Introduction

This grammar is inspired by Toki Pona, a conlang by Sonja Lang. Toki Pona features, depending 
on the source, 120-140 words, and the main philosophy of the language is simplicity, in
pronounciation, vocab, and grammar. 

See [this reddit post for a cheat-sheet](https://www.reddit.com/media?url=https%3A%2F%2Fpreview.redd.it%2F1ofg1vaukc941.png%3Fwidth%3D2481%26format%3Dpng%26auto%3Dwebp%26s%3D13b7f8806cd887953fb91bacb86ab5fb589836ea).

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

    <program> ::=  <statementlist>
    <statementlist> ::= <statement> <statementlist>
                        | ε
    <statement> ::= <definitionstatement>
                    | <executionstatement>
    <definitionstatement> ::= "function" <identifier> "acts on" <identifierlist> "," <statementlist>, "Done."
                            | "function" <identifier> "acts on" <identifierlist> "," <statementlist>, "return <identifierlist>." "Done."
                            | "function" <identifier> "acts on" <identifierlist> "," <statementlist>, "return <operatorlist>." "Done."
    <executionstatement> ::= <assignmentstatement>
                           | <printstatement>
                           | <whilestatement>
                           | <loopstatement>
                           | <ifstatement>
                           | <functioncallstatement>
    <assignmentstatement> ::= "Let" <identifier> "be" <value> "."
    <printstatement> ::= "Print" <identifierlist> "."
    <whilestatement> ::= "While" <expression> "is true," <statementlist> "Done."
    <loopstatement> ::= "<identifier> "in list" <identifier> "," <statementlist> "Done."
    <functioncallstatement> ::= "Modify" <identifierlist> "with function" <identifier> "."
    <ifstatement> :: "If" <expression> "is true," <statementlist> "Done".
    
    <expression> ::= <identifier> <operator> <identifier> 
    		| <identifier>
                    | <intval>
    		| <floatval>
    		| <stringval>
    <identifierlist> ::= <identifier> "and" <identifierlist>
                       | <identifier>
                       | "and" "(" <commaidlist>")
    <operatorlist> ::= <identifier> <operator> <operatorlist>
                       | <identifier>
                       | <operator> "(" <commaidlist> ")"
    <commaidlist> ::= <commaidlist> "," <identifier>
                       | <identifier>
    <identifier> ::= [a-zA-Z]+
    <intval> ::= [0-9]*
    <floatval> ::= [0-9]*+\.[0-9]+
    <stringval> ::= ".*?"




## Ideas

#<expressionlist> ::= <expression> "and" <expressionslist>
#                   | <expression>






