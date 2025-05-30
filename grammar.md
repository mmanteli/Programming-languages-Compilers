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

In the implementation, keywords are in English for ease. 


# Features

Just a couple highlights:

- negative numbers only as 0-1 = -1.
- "Polish notation" for operations, i.e. 3+4 == +(3,4).
- Functions can only modify arguments, all arguments are returned.
- Lists are represented as "x and y and z" and can be also noted in the Polish way and(x,y,z).


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


## AI disclaimer

I used ChatGPT to make a list of tokens of the lexer etc. things where a long dictionaries had to be created.





