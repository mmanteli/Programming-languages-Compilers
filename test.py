from src.parser import Parser
import sys

filename = sys.argv[1]
f = open(filename)
tp_script = f.read()
print("--------------Input---------------")
print(tp_script)

parser = Parser()
parser.parse(tp_script)

prg = parser.translate_program(return_prg=True)

print("----------Translation------------")
print(prg)
print("------------Result---------------")
exec(prg)