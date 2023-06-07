#### GROUP B29
#### NAMAN BIRLA - 2022310
#### PRANAV JAIN - 2022365
#### RITIKA THAKUR - 2022408
#### MUTHURAJ VAIRAMUTHU - 2022307

Computer Organization - CSE112 Winter semester 2023 Project

Project Guidlines: 

This project consists of three compulsory parts
1. Designing and Implementing the assembler.
2. Designing and Implementing the simulator.
3. Extending the functionality of the assembler-simulator set-up to handle simple floating-point computations.
4. Bonus question to include five more instructions in the ISA and update the assembler and the simulator.


A. ASSEMBLER
The main.py file in "Simple-Assembler" folder consists of the code for the assembler. The assembler follows the virtual ISA given in the 
assignment.
The assembler reads from stdin and outputs to stdout.
Go to the automated-testing folder and run the command "./run --no-sim" to evaluate the assembler.

B. SIMULATOR
The simulator.py file in "SimpleSimulator" folder consists of the code for the simulator. The simulator tracks each line of the assmebly code and gives the output of each register along with the program counter. It ends with the memory dump where the memory used during the program run is printed.
The simulator ouputs to stdout.
Go to the automated-testing folder and run the command "./run --no-asm" to evaluate the simulator.

To evaluate both the components, run the command "./run" in the automated-testing directory.

C. FLOATING POINT ARITHMETIC
Representation: No sign bit + 3 exponent bits + 5 mantissa bits
The assembler and the simulator are modified to incorporate the floating point arithmetic according to the given representation.

D. BONUS QUESTION:
The ISA is updated to handle five new instructions, whose descriptions are as follows.
floating_multiply:     |  11110   | mulf  reg1 reg2 reg3   |   TYPE-A   |     Performs reg1 = reg2 * reg3 for floating point.
                                                                          if the result overflows, the overflow flag is set and value of reg1 is set to 0.

multiply immediate:    |  11000    |muli  reg1 $imm        |   TYPE-B    |    Performs reg1 = reg1 * $imm 
                                                                          If the result overflows, the overflow flag is set and value of reg1 is set to 0.

decriment immediate:   |  11001    |decri reg1 $imm        |   TYPE-B    |    Performs reg1 = reg1 - $imm
                                                                          if reg1 = 0, the oveflow flag is set.

incriment immediate:   |  10111    | incri reg1 $imm       |    TYPE-B    |    Performs reg1 = reg1 + $imm.
                                                                          If the result overflows, the overflow bit is set and value of reg1 is set to 0.

power             :   |   11011    |pow   reg1 reg2 reg3    |  TYPE-A     |   Performs reg1 = reg2 ^ reg3 
                                                                          If the result overflows, the overflow flag is set and the value of reg1 is set to 0.

mulf: mulf is a Type A instruction. Performs reg1 = reg2 * reg3

muli: muli is a Type B instruction. Performs reg1 = reg1 * $Imm where Imm is a 7 bit value.

decri: decri is a Type B instruction. Performs reg1 = reg1 - $Imm where Imm is a 7 bit value.

incri: incri is a Type B instruction. Performs reg1 = reg1 + $Imm where Imm is a 7 bit value.

pow: pow is a Type A instruction. Performs reg1 = reg2 ^ reg3



CREDITS:
All the members of the group have equally contributed to the making of this code.