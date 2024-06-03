# Computer Organization Project: Assembler, Simulator, and Floating Point Arithmetic

## Group B29
- Naman Birla - 2022310
- Pranav Jain - 2022365
- Ritika Thakur - 2022408
- Muthuraj Vairamuthu - 2022307

## Overview
This project for the Computer Organization course (CSE112, Winter Semester 2023) consists of three compulsory parts: designing and implementing the assembler, designing and implementing the simulator, and extending the functionality of the assembler-simulator setup to handle simple floating-point computations. Additionally, a bonus question involves including five more instructions in the ISA and updating the assembler and simulator accordingly.

## Parts of the Project

### A. Assembler
The `main.py` file in the "Simple-Assembler" folder contains the code for the assembler, following the virtual ISA given in the assignment. It reads from stdin and outputs to stdout. To evaluate the assembler, navigate to the "automated-testing" folder and run the command `./run --no-sim`.

### B. Simulator
The `simulator.py` file in the "SimpleSimulator" folder contains the code for the simulator. It tracks each line of the assembly code and provides output for each register along with the program counter. It concludes with a memory dump displaying the memory used during program execution. To evaluate the simulator, navigate to the "automated-testing" folder and run the command `./run --no-asm`.

### C. Floating Point Arithmetic
Floating-point arithmetic representation: No sign bit + 3 exponent bits + 5 mantissa bits. The assembler and simulator are modified to incorporate floating-point arithmetic based on this representation.

### D. Bonus Question: Additional Instructions
The ISA is updated to handle five new instructions:
1. floating_multiply: Performs floating-point multiplication.
2. multiply_immediate: Performs multiplication with immediate values.
3. decrement_immediate: Decrements register with immediate value.
4. increment_immediate: Increments register with immediate value.
5. power: Performs exponentiation.

## Bonus Question Instructions
- floating_multiply: Type A instruction.
- multiply_immediate, decrement_immediate, increment_immediate: Type B instructions.
- power: Type A instruction.

## Credits
All group members contributed equally to the development of this project.
