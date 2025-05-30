from src.parser import Parser
import sys

filename = sys.argv[1]
translate = sys.argv[2] if len(sys.argv) > 2 else False
f = open(filename)
tp_script = f.read()
print("--------------Input---------------")
print(tp_script)

parser = Parser()
parser.parse(tp_script)

prg = parser.translate_program(return_prg=True)

if translate:
    print("----------Translation------------")
    print(prg)
print("------------Result---------------")
exec(prg)