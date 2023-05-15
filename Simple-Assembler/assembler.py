def binary(n):
    s=""
    y=n
    while(y!=0):
        s+=str(y%2)
        y=y//2
    s=s[::-1]
    while(len(s)!=7):
        s="0"+s
    return s

def return_code(name):
    f1=open("{}".format(name),"r")
    x=f1.read().split("\n")
    # print(x)
    for i in range(len(x)):
        x[i]=x[i].strip()
    x_copy=x.copy()
    dict_of_code={}
    bin_dict_of_code={}
    for i in range(len(x_copy)):
        if(x_copy[i]==""):
            x.remove("")
    for i in range(len(x)):
        x[i]=x[i].split()
    # print(x)
    for i in range(len(x)):
        dict_of_code[i+1]=x[i]
    # print(dict_of_code)
    f1.close()
    binary_instructions={}
    count=0
    for i,j in dict_of_code.items():
        if(j[0]=="var"):
            count+=1
    for i,j in dict_of_code.items():
        if(j[0]=="var"):
            continue
        bin_dict_of_code[binary(i-count-1)]=j
    # print(bin_dict_of_code)
    return dict_of_code,bin_dict_of_code

def return_variableloc(name):
    f=open("{}".format(name),"r")
    x=list(return_code(name)[0].values())
    # print(x)
    vars_dict={}
    vars_list=[]
    labels_dict={}
    len_code=len(x)
    count=0 #counting how many variables are there
    for i in range(len(x)):
        if(x[i][0]=="var"):
            vars_list.append(x[i])
            count+=1
    only_program=len_code-count
    # print(only_program)
    for i in range(len(x)-only_program,len(x)):
        # print(x[i],i-count)
        if(":" in x[i][0]):
            labels_dict[binary(i-count)]=x[i][0]

    for i in range(len(vars_list)):
        vars_dict[binary(only_program+i)]=x[i][1]
    # print(vars_dict)
    # print(labels_dict)
    return vars_dict,labels_dict


def errorgen(name,k):
    f1=open("output{}.txt".format(k),"a")
    pcode={}
    errcode={}
    fullcode={}
    f=open("{}".format(name),"r")
    x=f.read().split("\n")
    for i in range(len(x)):
        x[i]=x[i].strip()
    z=x.copy()
    # print(z)
    for i in range(len(z)):
        z[i]=z[i].split()
    # print(z)
    m=len(z)-1
    while(z[m]==[]):
        z.pop()
        m-=1
    # print(z)
    for i in range(len(z)):
        if(z[i]==[]):
            continue
        pcode[i+1]=z[i]
    # print(pcode)
    # y=x.copy()
    # for i in range(len(y)):
    #     if(y[i]==""):
    #         x.remove("")
    # for i in range(len(x)):
    #     x[i]=x[i].split()
    # # print(x)
    # for i in range(len(x)):
    #     pcode[i+1]=x[i]
    # print(pcode)
    lst_lines=list(pcode.keys())
    lst_code=list(pcode.values())
    # print(lst_lines,"\n",lst_code)
    if(len(lst_code)>128):
        # print("ERROR: FILE: {}\nNumber of instructions exceed 128.".format(name))
        f1.write("ERROR: FILE: {}\nNumber of instructions exceed 128.".format(name))
        f1.close()
        return True

    # print(pcode)
    
    #VARIABLES AND CONVENTIONS RELATED ERRORS
    # print(pcode)
    j=0
    variables=[]
    while(lst_code[j][0]=="var"):
        if(len(lst_code[j])!=2):
            # print("ERROR: FILE: {}\n<line {}>: Illegal instruction for variable declaration.".format(name,lst_lines[j]))
            f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction for variable declaration.".format(name,lst_lines[j]))
            f1.close()
            return True
        if lst_code[j][1][0].isdigit()==True:
            # print("ERROR: FILE: {}\n<line {}>: Illegal variable name.".format(name,lst_lines[j]))
            f1.write("ERROR: FILE: {}\n<line {}>: Illegal variable name.".format(name,lst_lines[j]))
            f1.close()
            return True
        for k in lst_code[j][1]:
            if (k.isalnum()==False and k!="_"):
                # print("ERROR: FILE: {}\n<line {}>: Illegal variable name.".format(name,lst_lines[j]))
                f1.write("ERROR: FILE: {}\n<line {}>: Illegal variable name.".format(name,lst_lines[j]))
                f1.close()
                return True
        if(lst_code[j][1]) in variables:
            # print("ERROR: FILE: {}\n<line {}>: Two or more variables cannot have the same name.".format(name,lst_lines[j]))
            f1.write("ERROR: FILE: {}\n<line {}>: Two or more variables cannot have the same name.".format(name,lst_lines[j]))
            f1.close()
            return True
        if lst_code[j][1] in INSTRUCTIONS:
            # print("ERROR: FILE: {}\n<line {}>: Mnemonics of the instructions cannot be used as a variable name.".format(name,lst_lines[j]))
            f1.write("ERROR: FILE: {}\n<line {}>: Mnemonics of the instructions cannot be used as a variable name.".format(name,lst_lines[j]))
            f1.close()
            return True
        if lst_code[j][1] in REGISTERS:
            # print("ERROR: FILE: {}\n<line {}>: Register names cannot be used as a variable name.".format(name,lst_lines[j]))
            f1.write("ERROR: FILE: {}\n<line {}>: Register names cannot be used as a variable name.".format(name,lst_lines[j]))
            f1.close()
            return True

        variables.append(lst_code[j][1])
        # print(lst_code[j])
        j+=1

    k=j
    while(k!=len(lst_code)):
        if(lst_code[k][0]=="var"):
            # print("ERROR: FILE: {}\n<line {}>: All variables should be declared in the beginning.".format(name,lst_lines[k]))
            f1.write("ERROR: FILE: {}\n<line {}>: All variables should be declared in the beginning.".format(name,lst_lines[k]))
            f1.close()
            return True
        k+=1
    
    # print(variables)

    #LABELS NAME AND DUPLICACY RELATED ERRORS
    # print(pcode)
    labels={}
    for i,j in pcode.items():
        if j[0][-1]==":":
            if(j[0][:-1] in variables):
                # print("ERROR: FILE: {}\n<line {}>: Variables and labels cannot have the same name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Variables and labels cannot have the same name.".format(name,i))
                f1.close()
                return True
            if j[0][0].isdigit()==True:
                # print("ERROR: FILE: {}\n<line {}>: Illegal label name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Illegal label name.".format(name,i))
                f1.close()
                return True
            for k in j[0][:-1]:
                if (k.isalnum()==False and k!="_"):
                    # print("ERROR: FILE: {}\n<line {}>: Illegal label name.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal label name.".format(name,i))
                    f1.close()
                    return True

            if j[0] in list(labels.values()):
                # print("ERROR: FILE: {}\n<line {}>: Two or more labels cannot have the same name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Two or more labels cannot have the same name.".format(name,i))
                f1.close()
                return True

            if j[0][:-1] in INSTRUCTIONS:
                # print("ERROR: FILE: {}\n<line {}>: Mnemonics of the instructions cannot be used as a label name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Mnemonics of the instructions cannot be used as a label name.".format(name,i))
                f1.close()
                return True
            if j[0][:-1] in REGISTERS:
                # print("ERROR: FILE: {}\n<line {}>: Register names cannot be used as a label name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Register names cannot be used as a label name.".format(name,i))
                f1.close()
                return True
                
            labels[i]=j[0]
    
    # print(labels)
    # print(variables)

    #HALT STATEMENT RELATED ERRORS
    for i in range(len(lst_code)-1):
        # print(lst_code[i])
        for j in lst_code[i]:
            if(j=="hlt"):
                # print("ERROR: FILE: {}\n<line {}>: Hlt not the last instruction.".format(name,lst_lines[i]))
                f1.write("ERROR: FILE: {}\n<line {}>: Hlt not the last instruction.".format(name,lst_lines[i]))
                f1.close()
                return True
    
    for j in (lst_code[len(lst_code)-1][:-1]):
        # print(j)
        if(j=="hlt"):
            # print("ERROR: FILE: {}\n<line {}>: Hlt not the last instruction.".format(name,lst_lines[-1]))
            f1.write("ERROR: FILE: {}\n<line {}>: Hlt not the last instruction.".format(name,lst_lines[-1]))
            f1.close()
            return True
    
    if(lst_code[-1][-1]!="hlt"):
        # print("ERROR: FILE: {}\n<line {}>: Missing hlt statement.".format(name,lst_lines[-1]))
        f1.write("ERROR: FILE: {}\n<line {}>: Missing hlt statement.".format(name,lst_lines[-1]))
        f1.close()
        return True


    #GENERAL INSTRUCTION ERRORS
    # print(pcode)
    for i,j in pcode.items():
        if j[0] in labels.values():
            if(len(j)==1):
                continue
            if(j[1] not in INSTRUCTIONS):
                # print("ERROR: FILE: {}\n<line {}>: Illegal instruction name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction name.".format(name,i))
                f1.close()
                return True
        else:
            if(j[0] not in INSTRUCTIONS):
                # print("ERROR: FILE: {}\n<line {}>: Illegal instruction name.".format(name,i))
                f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction name.".format(name,i))
                f1.close()
                return True

    #TYPE-A ERROR GENERATION
    # print(pcode)
    lst_A=[]
    for i,j in pcode.items():
        # print(i,j)
        try:
            if j[0] in labels.values():
                if j[1] in TYPE_A:
                    if len(j)!=5:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-A instruction".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-A instruction".format(name,i))
                        f1.close()
                        return True
                    if "FLAGS" in j:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.close()
                        return True
                    if(j[2] not in REGISTERS or j[3] not in REGISTERS or j[4] not in REGISTERS):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-A instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-A instruction.".format(name,i))
                        f1.close()
                        return True
                    lst_A.append(j)

            if j[0] in TYPE_A:
                if len(j)!=4:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal Type-A instruction".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal Type-A instruction".format(name,i))
                    f1.close()
                    return True
                if "FLAGS" in j:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.close()
                        return True
                if(j[1] not in REGISTERS or j[2] not in REGISTERS or j[3] not in REGISTERS):
                    # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-A instruction.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-A instruction.".format(name,i))
                    f1.close()
                    return True
                lst_A.append(j)                
        except:
            continue
    
    #TYPE-B ERROR GENERATION
    lst_B=[]
    # print(pcode)
    for i,j in pcode.items():
        try:
            if(j[0] in labels.values()):
                if(j[1] in TYPE_B and j[1]!="mov"):
                    if len(j)!=4:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    if("FLAGS" in j):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.close()
                        return True
                    if(j[2] not in list(REGISTERS.keys())[:-1]):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    if(j[3][0]!="$"):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    if(j[3][0]=="$"):
                        if(j[3]=="$"):
                            # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            f1.write("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            f1.close()
                            return True
                        for k in j[3][1:]:
                            if k.isdigit()==False:
                                # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                                f1.write("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                                f1.close()
                                return True
                        imm=int(j[3][1:])
                        if(imm<0 or imm>127):
                            # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                            f1.write("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                            f1.close()
                            return True
                    lst_B.append(j)

            if(j[0] in TYPE_B and j[0]!="mov"):
                    if len(j)!=3:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    if("FLAGS" in j):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        f1.close()
                        return True
                    if(j[1] not in list(REGISTERS.keys())[:-1]):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    if(j[2][0]!="$"):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    if(j[2][0]=="$"):
                        if(j[2]=="$"):
                            # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            f1.write("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            f1.close()
                            return True
                        for k in j[2][1:]:
                            if k.isdigit()==False:
                                # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                                f1.write("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                                f1.close()
                                return True
                        imm=int(j[2][1:])
                        if(imm<0 or imm>127):
                            # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                            f1.write("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                            f1.close()
                            return True
                    lst_B.append(j)
        except:
            continue   

    lst_C=[]
    
    # print(pcode)
    for i,j in pcode.items():
        try:
            if j[0] in labels.values() and j[1]=="mov":
                if len(j)!=4:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.close()
                    return True 
                if j[2]=="FLAGS":
                    # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    f1.close()
                    return True 
                if j[3][0]!="$" and j[3] not in REGISTERS:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.close()
                    return True 
                if j[3][0]=="$":
                    if j[2] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction for Type-B.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction for Type-B.".format(name,i))
                        f1.close()
                        return True 
                    if j[3]=="$":
                        # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                        f1.close()
                        return True 
                    for k in j[3][1:]:
                        if k.isdigit()==False:
                            # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                            f1.write("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                            f1.close()
                            return True
                    imm=int(j[3][1:])
                    if(imm<0 or imm>127):
                        # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    lst_B.append(j)
                else:
                    if j[3] not in REGISTERS or j[2] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        f1.close()
                        return True
                    lst_C.append(j)

            if j[0]=="mov":
                if len(j)!=3:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.close()
                    return True 
                if j[1]=="FLAGS":
                    # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    f1.close()
                    return True 
                if j[2][0]!="$" and j[2] not in REGISTERS:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    f1.close()
                    return True 
                if j[2][0]=="$":
                    if j[1] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        f1.close()
                        return True 
                    if j[2]=="$":
                        # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                        f1.close()
                        return True 
                    for k in j[2][1:]:
                        if k.isdigit()==False:
                            # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                            f1.write("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                            f1.close()
                            return True
                    imm=int(j[2][1:])
                    if(imm<0 or imm>127):
                        # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                        f1.close()
                        return True
                    lst_B.append(j)
                else:
                    if j[2] not in REGISTERS or j[1] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        f1.write("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        f1.close()
                        return True
                    lst_C.append(j)

        except:
            continue


def main():
    global R0,R1,R2,R3,R4,R5,R6,R7,FLAGS
    global REGISTERS,INSTRUCTIONS,variables_locations,labels_locations,TYPE_A,TYPE_B,TYPE_C,TYPE_D,TYPE_E,TYPE_F,type_A,type_B,type_C
    global type_D,type_E,type_F
    
    TYPE_A={"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100"}
    # type_A=[]

    TYPE_B={"mov":"00010","rs":"01000","ls":"01001"}
    # type_B=[]

    TYPE_C={"mov":"00011","div":"00111","not":"01101","cmp":"01110"}
    # type_C=[]

    TYPE_D={"ld":"00100","st":"00101"}
    # type_D=[]

    TYPE_E={"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"}
    # type_E=[]

    TYPE_F={"hlt":"11010"}
    # type_F=[]

    INSTRUCTIONS= ['add','sub','mul','xor','or','and','rs','ls','mov','div','not','cmp','ld','st','jmp','jlt','jgt','je','hlt','var']
    REGISTERS={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

    testcases=[r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase1.txt",r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase2.txt",
    r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase3.txt",r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase4.txt",
    r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase5.txt",r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase6.txt",
    r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase7.txt",r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase8.txt",
    r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase9.txt",r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\testcase10.txt"
    ]
    
    for k in range(len(testcases)):
        f1=open("output{}.txt".format(k+1),"w")
        f1.close()
        y=errorgen(testcases[k],k+1)
        if(y==False):
            program_code={}    # line and code
            binary_code={}  #binary
            variables_locations={} # memory for variables
            labels_locations={} #labels
            type_A=[]
            type_B=[]
            type_C=[]
            type_D=[]
            type_E=[]
            type_F=[]
            program_code,binary_code=return_code(testcases[k])
            variables_locations,labels_locations=return_variableloc(testcases[k])
            # print(program_code)
            # # print()
            # print(binary_code)
            # # # print()
            # print(variables_locations)
            # print(labels_locations)     
            # print(k,y)
            
main()

