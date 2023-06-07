import sys

def elt(s):
    is_zero=True 
    for i in s:
        if i!='0':
            is_zero=False 
            break
    if is_zero==False:
        L=[]
        for i in s:
            L.append(i)
        x=-1
        while(L[x]!='1'):
            L.pop()
        y=""
        for i in L:
            y+=i 
        return y
    return ""

def float_binary(num):
    if(num<0):
        return 'error'
    ieee=""
    res=""
    integer=int(num)
    dec=num-integer 
    res+=bin(integer)[2:]+"."
    y=""
    while(dec!=0):
        dec=dec*2
        y+=str(int(dec))
        dec=dec-int(dec)
    if(y==""):
        res+='0'
    else:
        res+=y
    
    # print(res)
    
    if(float(res)==0):
        exp="000"
        mt="00000"

    elif(res[0:5]=="0.001"):
        exp="000"
        mt=res[4:]
        mt=elt(mt)

    else:
        ind=res.index(".")
        ind1=res.index("1")
        if(ind<ind1):
            expint=ind-ind1
            mt=res[ind1+1:]
        else:
            expint=ind-ind1-1
            mt=res[ind1+1:ind]+res[ind+1:]
        # print(expint)
        # print(mt)
        mt=elt(mt)
        # print(mt)
        exp=expint+3 #bias 3
        if(exp<0 or exp>6):
            return 'error'
        exp=format(exp,"003b")

    if(len(mt)>5):
        return 'error'
    elif(len(mt)<5):
        while(len(mt)!=5):
            mt+="0"
    ieee=exp+mt 
    return ieee

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

def return_code():
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

def return_variableloc():
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


def errorgen(x1):
    # print(x1)
    # f1=open("output{}.txt".format(k),"a")
    pcode={}
    # errcode={}
    # fullcode={}
    # # f=open("{}".format(name),"r")
    # # x=f.read().split("\n")
    for i in range(len(x1)):
        x1[i]=x1[i].strip()
    # print(x1)
    z=x1.copy()
    # # print(z)
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
    lst_lines=list(pcode.keys())
    lst_code=list(pcode.values())
    # print(lst_lines,"\n",lst_code)
    if(len(lst_code)>128):
        sys.stdout.write("ERROR: Number of instructions exceed 128.")
        return True

#     # print(pcode)
    
#     #VARIABLES AND CONVENTIONS RELATED ERRORS
#     # print(pcode)
    # print(lst_code)
    j=0
    variables=[]
    while(j<len(lst_code) and lst_code[j][0]=="var"):
        if(len(lst_code[j])!=2):
            sys.stdout.write("ERROR: <line {}>: Illegal instruction for variable declaration.".format(lst_lines[j]))
            return True
        if lst_code[j][1][0].isdigit()==True:
            sys.stdout.write("ERROR: <line {}>: Illegal variable name.".format(lst_lines[j]))
            return True
        for k in lst_code[j][1]:
            if (k.isalnum()==False and k!="_"):
                sys.stdout.write("ERROR: <line {}>: Illegal variable name.".format(lst_lines[j]))
                return True
        if(lst_code[j][1]) in variables:
            sys.stdout.write("ERROR: <line {}>: Two or more variables cannot have the same name.".format(lst_lines[j]))
            return True
        if lst_code[j][1] in INSTRUCTIONS:
            sys.stdout.write("ERROR: <line {}>: Mnemonics of the instructions cannot be used as a variable name.".format(lst_lines[j]))
            return True
        if lst_code[j][1] in REGISTERS:
            sys.stdout.write("ERROR: <line {}>: Register names cannot be used as a variable name.".format(lst_lines[j]))
            return True

        variables.append(lst_code[j][1])
        # print(lst_code[j])
        j+=1

    k=j
    while(k!=len(lst_code)):
        if(lst_code[k][0]=="var"):
            sys.stdout.write("ERROR: <line {}>: All variables should be declared in the beginning.".format(lst_lines[k]))
            return True
        k+=1
    
    # print(variables)

    #LABELS NAME AND DUPLICACY RELATED ERRORS
    # print(pcode)
    labels={}
    for i,j in pcode.items():
        if j[0][-1]==":":
            if(j[0][:-1] in variables):
                sys.stdout.write("ERROR: <line {}>: Variables and labels cannot have the same name.".format(i))
                return True
            if j[0][0].isdigit()==True:
                sys.stdout.write("ERROR: <line {}>: Illegal label name.".format(i))
                return True
            for k in j[0][:-1]:
                if (k.isalnum()==False and k!="_"):
                    sys.stdout.write("ERROR: <line {}>: Illegal label name.".format(i))
                    return True

            if j[0] in list(labels.values()):
                sys.stdout.write("ERROR: <line {}>: Two or more labels cannot have the same name.".format(i))
                return True

            if j[0][:-1] in INSTRUCTIONS:
                sys.stdout.write("ERROR: <line {}>: Mnemonics of the instructions cannot be used as a label name.".format(i))
                return True
            if j[0][:-1] in REGISTERS:
                sys.stdout.write("ERROR: <line {}>: Register names cannot be used as a label name.".format(i))
                return True
        
            labels[i]=j[0]
    
    # print(labels)
    # print(variables)

    #HALT STATEMENT RELATED ERRORS
    for i in range(len(lst_code)-1):
        # print(lst_code[i])
        for j in lst_code[i]:
            if(j=="hlt"):
                sys.stdout.write("ERROR: <line {}>: Hlt not the last instruction.".format(lst_lines[i]))

                return True
    
    for j in (lst_code[len(lst_code)-1][:-1]):
        # print(j)
        if(j=="hlt"):
            sys.stdout.write("ERROR: <line {}>: Hlt not the last instruction.".format(lst_lines[-1]))
            return True
    
    if(lst_code[-1][-1]!="hlt"):
        sys.stdout.write("ERROR: <line {}>: Missing hlt statement.".format(lst_lines[-1]))
        return True

    #GENERAL INSTRUCTION ERRORS
    # print(pcode)
    for i,j in pcode.items():
        if j[0] in labels.values():
            if(len(j)==1):
                continue
            if(j[1] not in INSTRUCTIONS):
                sys.stdout.write("ERROR: <line {}>: Illegal instruction name.".format(i))
            
                return True
        else:
            if(j[0] not in INSTRUCTIONS):
                sys.stdout.write("ERROR: <line {}>: Illegal instruction name.".format(i))
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
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-A instruction".format(i))
                        return True
                    if "FLAGS" in j:
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                        return True
                    if(j[2] not in REGISTERS or j[3] not in REGISTERS or j[4] not in REGISTERS):
                        sys.stdout.write("ERROR: <line {}>: Illegal Register name in Type-A instruction.".format(i))
                        return True
                    lst_A.append(j)

            if j[0] in TYPE_A:
                if len(j)!=4:
                    sys.stdout.write("ERROR: <line {}>: Illegal Type-A instruction".format(i))
                
                    return True
                if "FLAGS" in j:
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))  
                        return True
                if(j[1] not in REGISTERS or j[2] not in REGISTERS or j[3] not in REGISTERS):
                    sys.stdout.write("ERROR: <line {}>: Illegal Register name in Type-A instruction.".format(i))
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
                if(j[1] in TYPE_B and j[1]!="mov" and j[1]!="movf"):
                    if len(j)!=4:
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-B instruction.".format(i))
                        return True
                    if("FLAGS" in j):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                        return True
                    if(j[2] not in list(REGISTERS.keys())[:-1]):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal Register name in Type-B instruction.".format(i))  
                        return True
                    if(j[3][0]!="$"):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal syntax for immediate value in Type-B instruction.".format(i))
                        return True
                    if(j[3][0]=="$"):
                        if(j[3]=="$"):
                            # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: No immediate value given in Type-B instruction.".format(i))
                            return True
                        for k in j[3][1:]:
                            if k.isdigit()==False:
                                # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                                sys.stdout.write("ERROR: <line {}>: Illegal immediate value in Type-B instruction.".format(i))
                                return True
                        imm=int(j[3][1:])
                        if(imm<0 or imm>127):
                            # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(i))
                            return True
                    lst_B.append(j)
                
                if(j[1] in TYPE_B and j[1]!="mov" and j[1]=="movf"):
                    if len(j)!=4:
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-B instruction.".format(i))
                        return True
                    if("FLAGS" in j):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                        return True
                    if(j[2] not in list(REGISTERS.keys())[:-1]):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal Register name in Type-B instruction.".format(i))  
                        return True
                    if(j[3][0]!="$"):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal syntax for immediate value in Type-B instruction.".format(i))
                        return True
                    if(j[3][0]=="$"):
                        if(j[3]=="$"):
                            # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: No immediate value given in Type-B instruction.".format(i))
                            return True
                        try:
                            t=float(j[3][1:])
                        except:
                            sys.stdout.write("ERROR: <line {}>: Illegal immediate value in Type-B instruction.".format(i))
                            return True
                        if(float_binary(t)=='error'):
                            sys.stdout.write("ERROR: <line {}>: Immediate value cannot be represented in the given format.".format(i))
                            return True
                    lst_B.append(j)

            if(j[0] in TYPE_B and j[0]!="mov" and j[0]!="movf"):
                    if len(j)!=3:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-B instruction.".format(i))
                        return True
                    if("FLAGS" in j):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                        return True
                    if(j[1] not in list(REGISTERS.keys())[:-1]):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal Register name in Type-B instruction.".format(i))
                        return True
                    if(j[2][0]!="$"):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal syntax for immediate value in Type-B instruction.".format(i))
                        return True
                    if(j[2][0]=="$"):
                        if(j[2]=="$"):
                            # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: No immediate value given in Type-B instruction.".format(i))
                            return True
                        for k in j[2][1:]:
                            if k.isdigit()==False:
                                # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                                sys.stdout.write("ERROR: <line {}>: Illegal immediate value in Type-B instruction.".format(i))
                                return True
                        imm=int(j[2][1:])
                        if(imm<0 or imm>127):
                            # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(i))
                            return True
                    lst_B.append(j)

            if(j[0] in TYPE_B and j[0]!="mov" and j[0]=="movf"):
                    if len(j)!=3:
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-B instruction.".format(i))
                        return True
                    if("FLAGS" in j):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                        return True
                    if(j[1] not in list(REGISTERS.keys())[:-1]):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal Register name in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal Register name in Type-B instruction.".format(i))  
                        return True
                    if(j[2][0]!="$"):
                        # print("ERROR: FILE: {}\n<line {}>: Illegal syntax for immediate value in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal syntax for immediate value in Type-B instruction.".format(i))
                        return True
                    if(j[2][0]=="$"):
                        if(j[2]=="$"):
                            # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: No immediate value given in Type-B instruction.".format(i))
                            return True
                        try:
                            t=float(j[2][1:])
                        except:
                            sys.stdout.write("ERROR: <line {}>: Illegal immediate value in Type-B instruction.".format(i))
                            return True
                        if(float_binary(t)=='error'):
                            sys.stdout.write("ERROR: <line {}>: Immediate value cannot be represented in the given format.".format(i))
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
                    sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))
                    return True 
                if j[2]=="FLAGS":
                    # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                    return True 
                if j[3][0]!="$" and j[3] not in REGISTERS:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))
                    return True 
                if j[3][0]=="$":
                    if j[2] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction for Type-B.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction for Type-B.".format(i))
                        return True 
                    if j[3]=="$":
                        # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: No immediate value given in Type-B instruction.".format(i))
                        return True 
                    for k in j[3][1:]:
                        if k.isdigit()==False:
                            # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: Illegal immediate value in Type-B instruction.".format(i))
                            return True
                    imm=int(j[3][1:])
                    if(imm<0 or imm>127):
                        # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(i))
                        return True
                    lst_B.append(j)
                else:
                    if j[3] not in REGISTERS or j[2] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))   
                        return True
                    lst_C.append(j)

            if j[0]=="mov":
                if len(j)!=3:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))    
                    return True 
                if j[1]=="FLAGS":
                    # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                    return True 
                if j[2][0]!="$" and j[2] not in REGISTERS:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))
                    return True 
                if j[2][0]=="$":
                    if j[1] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))
                        return True 
                    if j[2]=="$":
                        # print("ERROR: FILE: {}\n<line {}>: No immediate value given in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: No immediate value given in Type-B instruction.".format(i))
                        return True 
                    for k in j[2][1:]:
                        if k.isdigit()==False:
                            # print("ERROR: FILE: {}\n<line {}>: Illegal immediate value in Type-B instruction.".format(name,i))
                            sys.stdout.write("ERROR: <line {}>: Illegal immediate value in Type-B instruction.".format(i))
                            return True
                    imm=int(j[2][1:])
                    if(imm<0 or imm>127):
                        # print("ERROR: FILE: {}\n<line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Overflow immediate value(<0 or >127) in Type-B instruction.".format(i))      
                        return True
                    lst_B.append(j)
                else:
                    if j[2] not in REGISTERS or j[1] not in REGISTERS:
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format.".format(i))  
                        return True
                    lst_C.append(j)

        except:
            continue
        
    # print(lst_C)
    #TYPE-C ERROR GENERATION
    # print(pcode)
    for i,j in pcode.items():
        try:
            if j[0] in labels.values():
                if j[1] in TYPE_C and j[1]!="mov":
                    if len(j)!=4:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-C instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-C instruction.".format(i))
                    
                        return True
                    if j[2]=="FLAGS" or j[3]=="FLAGS":
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                    
                        return True
                    if j[2] not in REGISTERS or j[3] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal register name in Type-C instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal register name in Type-C instruction.".format(i))
                    
                        return True
                    lst_C.append(j)

            if j[0] in TYPE_C and j[0]!="mov":
                if len(j)!=3:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-C instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-C instruction.".format(i))
                    
                        return True
                if j[1]=="FLAGS" or j[2]=="FLAGS":
                    # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                
                    return True
                if j[1] not in REGISTERS or j[2] not in REGISTERS:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal register name in Type-C instruction.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal register name in Type-C instruction.".format(i))
                
                    return True
                lst_C.append(j)

        except:
            continue
        
    # print(lst_C)

    #TYPE-D ERROR GENERATION
    lst_D=[]
    for i,j in pcode.items():
        try:
            if j[0] in labels.values():
                if j[1] in TYPE_D:
                    if len(j)!=4:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-D instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-D instruction.".format(i))
                    
                        return True
                    if "FLAGS" in j:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                    
                        return True    
                    if j[2] not in REGISTERS:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal register name for Type-D instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal register name for Type-D instruction.".format(i))
                    
                        return True
                    if (j[3]+":" in labels.values()):
                        # print("ERROR: FILE: {}\n<line {}>: Labels cannot be used as variables.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Labels cannot be used as variables.".format(i))
                    
                        return True
                    if j[3].isdigit()==True:
                        # print("ERROR: FILE: {}\n<line {}>: Numerical value cannot be interpreted as a variable.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Numerical value cannot be interpreted as a variable.".format(i))
                    
                        return True
                    if j[3] not in variables:
                        # print("ERROR: FILE: {}\n<line {}>: Use of undefined variable.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Use of undefined variable.".format(i))
                    
                        return True
                    lst_D.append(j)
                
            if j[0] in TYPE_D:
                if len(j)!=3:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-D instruction.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-D instruction.".format(i))
                
                    return True
                if "FLAGS" in j:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal use of FLAGS register.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal use of FLAGS register.".format(i))
                
                    return True    
                if j[1] not in REGISTERS:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal register name for Type-D instruction.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal register name for Type-D instruction.".format(i))
                
                    return True
                if (j[2]+":" in labels.values()):
                    # print("ERROR: FILE: {}\n<line {}>: Labels cannot be used as variables.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Labels cannot be used as variables.".format(i))
                
                    return True
                if j[2].isdigit()==True:
                    # print("ERROR: FILE: {}\n<line {}>: Numerical value cannot be interpreted as a variable.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Numerical value cannot be interpreted as a variable.".format(i))
                
                    return True
                if j[2] not in variables:
                    # print("ERROR: FILE: {}\n<line {}>: Use of undefined variable.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Use of undefined variable.".format(i))
                
                    return True
                lst_D.append(j)
        
        except:
            continue

    # print(lst_D)

    #TYPE-E ERROR GENERATION
    lst_E=[]
    for i,j in pcode.items():
        try:
            if j[0] in labels.values():
                if j[1] in TYPE_E:
                    if len(j)!=3:
                        # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-E instruction.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-E instruction.".format(i))
                    
                        return True
                    if j[2] in variables:
                        # print("ERROR: FILE: {}\n<line {}>: Variables cannot be used as labels.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Variables cannot be used as labels.".format(i))
                    
                        return True
                    if(j[2]+":" not in labels.values()):
                        # print("ERROR: FILE: {}\n<line {}>: Use of undefined labels.".format(name,i))
                        sys.stdout.write("ERROR: <line {}>: Use of undefined labels.".format(i))
                    
                        return True 
                    lst_E.append(j)

            if j[0] in TYPE_E:
                if len(j)!=2:
                    # print("ERROR: FILE: {}\n<line {}>: Illegal instruction format for Type-E instruction.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Illegal instruction format for Type-E instruction.".format(i))
                
                    return True
                if j[1] in variables:
                    # print("ERROR: FILE: {}\n<line {}>: Variables cannot be used as labels.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Variables cannot be used as labels.".format(i))
                
                    return True
                if(j[1]+":" not in labels.values()):
                    # print("ERROR: FILE: {}\n<line {}>: Use of undefined labels.".format(name,i))
                    sys.stdout.write("ERROR: <line {}>: Use of undefined labels.".format(i))
                
                    return True 
                lst_E.append(j)

        except:
            continue

    # print(lst_E)
    # print(lst_A,"\n",lst_B,"\n",lst_C,"\n",lst_D,"\n",lst_E)

    return False


def A(i):
    # f=open("output{}.txt".format(j),"a")
    unused="00"
    if(i[0] in list(labels_locations.values())):
        s=(TYPE_A[i[1]]+unused+REGISTERS[i[2]]+REGISTERS[i[3]]+REGISTERS[i[4]])
    else:
        s=(TYPE_A[i[0]]+unused+REGISTERS[i[1]]+REGISTERS[i[2]]+REGISTERS[i[3]])
    # print(s)
    sys.stdout.write(s+"\n")
    # f.close()

def B(i):
    # f=open("output{}.txt".format(j),"a")
    unused="0"
    if(i[0] in list(labels_locations.values())):
        if(TYPE_B[i[1]]!="10010"):
            s=(TYPE_B[i[1]]+"0"+REGISTERS[i[2]]+binary(int(i[3][1::])))
        else:
            s=(TYPE_B[i[1]]+REGISTERS[i[2]]+float_binary(float(i[3][1:])))
    else:
        if(TYPE_B[i[0]]!="10010"):
            s=(TYPE_B[i[0]]+"0"+REGISTERS[i[1]]+binary(int(i[2][1::])))
        else:
            s=(TYPE_B[i[0]]+REGISTERS[i[1]]+float_binary(float(i[2][1:])))
    # print(s)
    sys.stdout.write(s+"\n")
    # f.close()

def C(i):
    # f=open("output{}.txt".format(j),"a");
    unused="00000"
    if(i[0] in list(labels_locations.values())):
        s=(TYPE_C[i[1]]+unused+REGISTERS[i[2]]+REGISTERS[i[3]])
    else:
        s=(TYPE_C[i[0]]+unused+REGISTERS[i[1]]+REGISTERS[i[2]])
    # print(s)
    sys.stdout.write(s+"\n")
    # f.close()

def D(i):
    unused="0"
    # f=open("output{}.txt".format(j),"a");
    if(i[0] in list(labels_locations.values())):
        if(i[3] in list(variables_locations.values())):
            s=(TYPE_D[i[1]]+unused+REGISTERS[i[2]]+list(variables_locations.keys())[(list(variables_locations.values())).index(i[3])])
        elif(i[3]+":" in list(labels_locations.values())):
            s=(TYPE_D[i[1]]+unused+REGISTERS[i[2]]+list(labels_locations.keys())[(list(labels_locations.values())).index(i[3]+":")])
    else:
        if(i[2] in list(variables_locations.values())):
            s=(TYPE_D[i[0]]+unused+REGISTERS[i[1]]+list(variables_locations.keys())[(list(variables_locations.values())).index(i[2])])
        elif(i[2]+":" in list(labels_locations.values())):
            s=(TYPE_D[i[0]]+unused+REGISTERS[i[1]]+list(labels_locations.keys())[(list(labels_locations.values())).index(i[2]+":")])
    # print(s)
    sys.stdout.write(s+"\n")
    # f.close()

def E(i):
    # print(i[0],i[1])
    # f=open("output{}.txt".format(j),"a")
    unused="0000"
    if(i[0] in list(labels_locations.values())):
        if(i[2] in list(variables_locations.values())):
            s=(TYPE_E[i[1]]+unused+list(variables_locations.keys())[(list(variables_locations.values())).index(i[2])])
        elif(i[2]+":" in list(labels_locations.values())):
            s=(TYPE_E[i[1]]+unused+list(labels_locations.keys())[(list(labels_locations.values())).index(i[2]+":")])
        
    else:
        if(i[1] in list(variables_locations.values())):
            s=(TYPE_E[i[0]]+unused+list(variables_locations.keys())[(list(variables_locations.values())).index(i[1])])
        elif(i[1]+":" in list(labels_locations.values())):
            s=(TYPE_E[i[0]]+unused+list(labels_locations.keys())[(list(labels_locations.values())).index(i[1]+":")])
    # print(s)
    sys.stdout.write(s+"\n")
    # f.close()

def F(i):
    # f=open("output{}.txt".format(j),"a");
    unused="00000000000"
    if (i[0] in list(labels_locations.values())):
        s=(TYPE_F[i[1]]+unused)
    else:
        s=(TYPE_F[i[0]] + unused)
    # print(s)
    sys.stdout.write(s+"\n")
    


def main():
    global R0,R1,R2,R3,R4,R5,R6,R7,FLAGS
    global REGISTERS,INSTRUCTIONS,variables_locations,labels_locations,TYPE_A,TYPE_B,TYPE_C,TYPE_D,TYPE_E,TYPE_F,type_A,type_B,type_C
    global type_D,type_E,type_F
    global x
    TYPE_A={"add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100","addf":"10000","subf":"10001"}
    # type_A=[]

    TYPE_B={"mov":"00010","rs":"01000","ls":"01001","movf":"10010"}
    # type_B=[]

    TYPE_C={"mov":"00011","div":"00111","not":"01101","cmp":"01110"}
    # type_C=[]

    TYPE_D={"ld":"00100","st":"00101"}
    # type_D=[]

    TYPE_E={"jmp":"01111","jlt":"11100","jgt":"11101","je":"11111"}
    # type_E=[]

    TYPE_F={"hlt":"11010"}
    # type_F=[]

    INSTRUCTIONS= ['add','sub','mul','xor','or','and','rs','ls','mov','div','not','cmp','ld','st','jmp','jlt','jgt','je','hlt','var','addf','subf','movf']
    REGISTERS={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}

    x=sys.stdin.read().splitlines()
    x1=x.copy()
    # print(x1)
    # for k in range(len(testcases)):
    # f1=open("output.txt","w")
    y=errorgen(x1)
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
        program_code,binary_code=return_code()
        variables_locations,labels_locations=return_variableloc()
        # print(x)
        # print(program_code)
        # print()
        # print(binary_code)
        # # print()
        # print(variables_locations)
        # print(labels_locations)     
        # print(k,y)
        for i in list(binary_code.values()):
            # print(i)
            try:
                if((i[0] in list(labels_locations.values()) and i[1] in TYPE_A and i[2] in REGISTERS and i[3] in REGISTERS and i[4] in REGISTERS and len(i)==5) or (i[0] in TYPE_A and i[1] in REGISTERS and i[2] in REGISTERS and i[3] in REGISTERS and len(i)==4)):
                    type_A.append(i)
            except:
                pass
            try:
                if((i[0] in list(labels_locations.values()) and i[1] in TYPE_C and i[2] in REGISTERS and i[3] in REGISTERS and len(i)==4 )or (i[0] in TYPE_C and i[1] in REGISTERS and i[2] in REGISTERS and len(i)==3)):
                    type_C.append(i)
            except:
                pass
            # print(i[0] in list(labels_locations.values()))
            try:
                if((i[0] in list(labels_locations.values()) and i[1] in TYPE_F.keys()) or i[0] in TYPE_F or i[-1]=="hlt"):
                    type_F.append(i)
            except:
                pass
            try:
                if((i[0] in list(labels_locations.values()) and i[1] in TYPE_D and i[2] in REGISTERS and (i[3] in list(variables_locations.values()) or i[3]+":" in list(labels_locations.values()))) and len(i)==4) or (i[0] in TYPE_D and i[1] in REGISTERS and (i[2]+":" in list(labels_locations.values()) or i[2] in list(variables_locations.values()))):
                    type_D.append(i)
            except:
                pass
            try:
                if((i[0] in list(labels_locations.values()) and i[1] in TYPE_B and "$" in i[-1] and i[2] in REGISTERS)or (i[0] in TYPE_B and  i[1] in REGISTERS and "$" in i[-1])):
                    type_B.append(i)
            except:
                pass
            try:
                if((i[0] in list(labels_locations.values()) and i[1] in TYPE_E and (i[2]+":" in list(labels_locations.values()) or i[2] in list(variables_locations.values() ))) or (i[0] in TYPE_E and (i[1]+":" in list(labels_locations.values()) or i[1] in list(variables_locations.values())))):
                    type_E.append(i)
            except:
                pass

        # print(type_A)
        # print(type_B)
        # print(type_C)
        # print(type_D)
        # print(type_E)
        # print(type_F)
            
        for j in list(binary_code.values()):
            # print(j,j in type_E)
            if j in type_A:
                A(j)
            elif j in type_B:
                B(j)
            elif j in type_C:
                C(j)
            elif j in type_D:
                D(j)
            elif j in type_E:
                E(j)
            elif j in type_F:
                F(j)
                
main()