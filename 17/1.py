import re
from enum import Enum

input_file = "data.txt"
with open(input_file, "r") as file:
    text = file.read()
    register_a = int(re.search(r"Register A: (\d+)", text).group(1))
    register_b = int(re.search(r"Register B: (\d+)", text).group(1))
    register_c = int(re.search(r"Register C: (\d+)", text).group(1))
    program = [
        int(el) for el in re.search(r"Program: ([\d,]+)", text).group(1).split(",")
    ]


class OpCode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Computer:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program
        self.pointer = 0
        self.output = []

    def cycle(self):
        if self.pointer + 1 >= len(self.program):
            return False

        literal = self.program[self.pointer + 1]
        combo = self.fetch_combo(literal)
        self.operation(OpCode(self.program[self.pointer]), combo, literal)
        return True

    def fetch_combo(self, value):
        if value < 4:
            return value
        if value >= 7:
            return None
        return [self.A, self.B, self.C][value - 4]

    def dv(self, register_index, value):
        numerator = self.A
        divisor = 2**value
        result = numerator / divisor
        match register_index:
            case 0:
                self.A = int(result)
            case 1:
                self.B = int(result)
            case _:
                self.C = int(result)
        self.pointer += 2

    def bxl(self, value):
        self.B ^= value
        self.pointer += 2

    def bst(self, value):
        self.B = value % 8
        self.pointer += 2

    def jnz(self, value):
        self.pointer += 2
        if self.A != 0:
            self.pointer = value

    def bxc(self):
        self.B = self.B ^ self.C
        self.pointer += 2

    def out(self, value):
        self.output.append(value % 8)
        self.pointer += 2

    def operation(self, op: OpCode, combo, literal):
        match op:
            case OpCode.ADV:
                return self.dv(0, combo)
            case OpCode.BXL:
                return self.bxl(literal)
            case OpCode.BST:
                return self.bst(combo)
            case OpCode.JNZ:
                return self.jnz(literal)
            case OpCode.BXC:
                return self.bxc()
            case OpCode.OUT:
                return self.out(combo)
            case OpCode.BDV:
                return self.dv(1, combo)
            case OpCode.CDV:
                return self.dv(2, combo)


computer = Computer(register_a, register_b, register_c, program)
print(computer.program)
print(computer.pointer)

while computer.cycle():
    print(f"{computer.pointer}")

print(",".join([str(num) for num in computer.output]))
