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



CREDITS:
All the members of the group have equally contributed to the making of this code.