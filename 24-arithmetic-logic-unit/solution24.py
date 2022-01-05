# Solution to day 24 of AOC 2021, Arithmetic Logic Unit
# https://adventofcode.com/2021/day/24

class ALU:

    def __init__(self, instructions: list, inputs: list):
        self.instructions = instructions.copy()     # Pass parm list by value, not reference.
        self.inputs = inputs.copy()

        # It has integer variables w, x, y, and z. These variables all start with the value 0.
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def is_variable(self, t1: str) -> bool:
        return t1 in ['w', 'x', 'y', 'z']

    def getter(self, variable) -> int:
        if variable == 'w':
            return self.w
        elif variable == 'x':
            return self.x
        elif variable == 'y':
            return self.y
        return self.z

    def setter(self, variable, value: int):
        if variable == 'w':
            self.w = value
        elif variable == 'x':
            self.x = value
        elif variable == 'y':
            self.y = value
        else:
            self.z = value

    def parse_instruction(self):
        instruction = self.instructions.pop(0)
        # print(instruction)
        pieces = instruction.split(' ')

        if pieces[0] == 'inp':
            # print(self.z)
            this_input = self.inputs.pop(0)
            self.setter(pieces[1], this_input)

        else:
            t1_int = self.getter(pieces[1])

            if self.is_variable(pieces[2]):
                t2_int = self.getter(pieces[2])
            else:
                t2_int = int(pieces[2])

            if pieces[0] == 'add':
                self.setter(pieces[1], t1_int + t2_int)
            elif pieces[0] == 'mul':
                self.setter(pieces[1], t1_int * t2_int)
            elif pieces[0] == 'div':
                self.setter(pieces[1], t1_int // t2_int)
            elif pieces[0] == 'mod':
                self.setter(pieces[1], t1_int % t2_int)
            elif pieces[0] == 'eql':
                if t1_int == t2_int:
                    self.setter(pieces[1], 1)
                else:
                    self.setter(pieces[1], 0)

    def run(self):
        while len(self.instructions) != 0:
            self.parse_instruction()


# Here is an ALU program which takes an input number, negates it, and stores it in x.
test_program1 = """inp x
mul x -1""".split('\n')
alu1 = ALU(test_program1, [5])
alu1.run()
assert alu1.x == -5

# Here is an ALU program which takes two input numbers, then sets z to 1 if the second input number is three times
# larger than the first input number, or sets z to 0 otherwise:
test_program2 = """inp z
inp x
mul z 3
eql z x""".split('\n')
alu2 = ALU(test_program2, [-5, -15])
alu2.run()
assert alu2.z == 1
alu3 = ALU(test_program2, [7, 22])
alu3.run()
assert alu3.z == 0

# Here is an ALU program which takes a non-negative integer as input, converts it into binary, and stores the lowest
# (1's) bit in z, the second-lowest (2's) bit in y, the third-lowest (4's) bit in x,
# and the fourth-lowest (8's) bit in w:
test_program3 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""".split('\n')
alu4 = ALU(test_program3, [7])
alu4.run()
assert alu4.w == 0 and alu4.x == 1 and alu4.y == 1 and alu4.z == 1

f = open('input.txt')
t = f.read()
f.close()
loc = t.split('\n')

# To test a solution.
digits = [2, 9, 9, 8, 9, 2, 9, 7, 9, 4, 9, 5, 1, 9]
alu = ALU(loc, digits)
alu.run()
print(digits, alu.z)

divisor_so_far = 1
divisor_left = {}
for depth in range(13, 0 - 1, -1):
    this_program = loc[depth * 18: 18 + depth * 18]
    divisor_so_far *= int((this_program[4].split())[2])     # 4th line of code, 2nd term.
    divisor_left[depth] = divisor_so_far

lowest_z = 999999999999


def solutions(depth: int, z_so_far: int, digits_so_far: list):
    global lowest_z

    if depth == 14:
        if z_so_far == 0:
            print('!!! Solution:', digits_so_far)
        if z_so_far <= lowest_z:
            print(depth, z_so_far, digits_so_far)
            lowest_z = z_so_far
        return

    # This is a viable sequence so far!
    this_program = loc[depth * 18: 18 + depth * 18]
    for try_digit in range(9, 1 - 1, -1):
        digits_to_here = digits_so_far.copy()
        digits_to_here.append(try_digit)
        alu = ALU(this_program, [try_digit])
        alu.z = z_so_far
        alu.run()

        if alu.z // divisor_left[depth] > 0:       # Not enough division left to get Z down to 0 by end.
            return

        solutions(depth=depth + 1,z_so_far=alu.z,digits_so_far=digits_to_here)


solutions(depth=0, z_so_far=0, digits_so_far=[])
