from os import error
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
        result = self.A >> value
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

    def get_output(self):
        return ",".join([str(num) for num in self.output])


# 1. B = A % 8  (select the last 3 bits)
# 2. B = B ^ 110b (XOR these with 110b)
# 3. C = A >> B (Shift A with the result from 2)
# 4. B = B ^ C
# 5. B = B ^ 111b
# 6. A = A >> B
def calculate_output(A):
    B1 = A % 8
    B2 = B1 ^ 6
    C = A >> B2
    B3 = B2 ^ C
    B4 = B3 ^ 7
    return B4 % 8


options = [0]
for op in program[::-1]:
    valid_options = []
    for option in range(2**3):
        for prev_option in options:
            new_res = (prev_option << 3) ^ option
            op_res = calculate_output(new_res)
            if op_res == op:
                valid_options.append(new_res)

    if len(valid_options) == 0:
        raise ValueError(f"Panic no options for {op}")
    options = valid_options
print(min(options))
computer = Computer(min(options), register_b, register_c, program)
print(program)
while computer.cycle():
    continue
print(computer.output)

# Important truths:
# A = B ^ C -> B = A ^ C and C = A ^ B
# A = B ^ (B ^ C) = C (doing same XOR twice negates the result)

# A = B / (2^C) is same as shifting bits C positions to the right.
# .. A = B >> C

# A = B >> C
# A << C = B
# .... A * 2^C = B

# This program does a lot of things
# and then writes register B to the output.
# Finally it jumps to 0 IFF register A != 0.
# If register A = 0 it quits.

# Program:
# 1. B = A % 8  (select the last 3 bits)
# 2. B = B ^ 110b (XOR these with 110b)
# 3. C = A >> B (Shift A with the result from 2)
# 4. B = B ^ C
# 5. B = B ^ 111b
# 6. A = A >> B
# WRITE B TO REGISTER
# LOOP IF A != 0

# Out target program is 2,4,1,6,7,5,4,4,1,7,0,3,5,5,3,0
# So our first number that is written must be 2 = 010b
# 5. 010b = B ^ 111b -> 111b ^ 010b = 101b
# 4. 101b = B2 ^ C -> B2 = 101b ^ C
# 2. B2 = B1 ^ 110b, 101b ^ C = B1 ^ 110b -> 110b ^ 101b = C ^ B1 = 011b
# 1. C ^ 011b = A % 8 -> C = 011b ^ (A % 8)

# 3. 011b ^ (A % 8) = A >> (101b ^ (011b ^ (A % 8)))
# ... A = (011b ^ (A % 8)) << (101b ^ (011b ^ (A % 8)))
# ... A = (011b ^ (A % 8)) << (110 ^ (A % 8)))
# ... A = (3 ^ (A % 8)) << 6 ^ (A % 8))
# ... A = (3 ^ A % 8) * 2 ** (6 ^ A % 8)
# After calculating this means A grows in steps of 33

# for A in range(100000000):
#     # print(left, right)
#

#########
# 1. A is shifted right by B every iteration. (So first 2, then 4, then 1, ... etc.)
# ... Meaning 010100b >> 2 becomes 0101b.

# Given that the first printed B value must be 2, we can iterate on that.
