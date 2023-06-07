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

def ieee_to_decimal(number):
    bias = 3
    exponent_binary = number[:3]
    mantissa_binary = number[3:8]
    exponent_decimal = int(exponent_binary, 2)
    true_exponent = exponent_decimal - bias
    mantissa_decimal = int(mantissa_binary, 2)
    fractional_value_1 = 1 + (mantissa_decimal / (2 ** 5))
    fractional_value_2 = mantissa_decimal / (2 ** 5)
    if exponent_decimal == 0 and mantissa_decimal == 0:
        return 0
    else:
        if 1 <= exponent_decimal <= 6:
            decimal_conversion = fractional_value_1 * (2 ** true_exponent)
        else:
            decimal_conversion = fractional_value_2 * (2 ** (-2))
    return decimal_conversion

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

def opcode(s):
    return s[:5]

def flip(s):
    y=""
    for i in s:
        if(i=='0'):
            y+='1'
        else:
            y+='0'
    return y

def regout():
    s=""
    s+=(format(pc,"007b")+8*" ")
    for i in VALUES.values():
        if(type(i)==str):
            while(len(i)!=16):
                i="0"+i
            s+=i+" "
        else:
            s+=(format(i,"016b")+" ")
        # sys.stdout.write(format(i,"016b")+" ")
    # f1.write(s+"\n")
    sys.stdout.write(s+"\n")

# def regout2(reg1):
#     s=""
#     s+=(format(pc,"007b")+8*" ")
#     for i,j in VALUES:
#         if(type(j)==str):
#             while(len(j)!=16):
#                 j="0"+j
#             s+=j+" "
#         else:
#             s+=format(i,"016b")+" "
#     sys.stdout.write(s+"\n")

def reset():
    VALUES["FLAGS"]=0

def main():
    global pc,TYPE_A,TYPE_B,TYPE_C,TYPE_D,TYPE_E,TYPE_F,VALUES,REGISTERS,f1
    pc=0

    REGISTERS={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
    
    VALUES={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":0}

    TYPE_A=["00000","00001","00110","01010","01011","01100","10000","10001"]
    type_A=[]

    TYPE_B=["00010","01000","01001","10010"]
    type_B=[]

    TYPE_C=["00011","00111","01101","01110"]
    type_C=[]

    TYPE_D=["00100","00101"]
    type_D=[]

    TYPE_E=["01111","11100","11101","11111"]
    type_E=[]

    TYPE_F=["11010"]
    type_F=[]

    memory={}
    # f1=open("out.txt","w")
    # f=open(r"C:\Users\user\OneDrive\Desktop\DSA and C\CO-B29\Simulator\code.txt","r")
    x=sys.stdin.read().splitlines()
    # sys.stdout.write(x)
    for j in range(len(x)):
        memory[format(j,"007b")]=x[j] #append to memory
    # sys.stdout.write(memory)
    mem_key=list(memory.keys())
    mem_code=list(memory.values())
    # sys.stdout.write(mem_code,mem_key)
    while(opcode(mem_code[pc])!="11010"):  #while not halted
        instruction=mem_code[pc] #fetch instruction from memory
        # sys.stdout.write(type(instruction))

        # type A
        if(opcode(instruction)in TYPE_A):
            r1=int(instruction[7:10],2)
            r2=int(instruction[10:13],2)
            r3=int(instruction[13:16],2)
            if(opcode(instruction)=="00000"): #add
                VALUES["R{}".format(r1)]=VALUES["R{}".format(r2)]+VALUES["R{}".format(r3)]
                #overflow FLAG
                if(VALUES["R{}".format(r1)]>65535):
                    VALUES["R{}".format(r1)]=0
                    VALUES["FLAGS"]=8
                else:
                    reset()
                regout()
                pc+=1
            
            elif(opcode(instruction)=="00001"): #sub
                VALUES["R{}".format(r1)]=VALUES["R{}".format(r2)]-VALUES["R{}".format(r3)]
                #overflow FLAG
                if(VALUES["R{}".format(r1)]<0):
                    VALUES["R{}".format(r1)]=0
                    VALUES["FLAGS"]=8
                else:
                    reset()
                regout()
                pc+=1


            elif(opcode(instruction)=="00110"): #mul
                VALUES["R{}".format(r1)]=VALUES["R{}".format(r2)]*VALUES["R{}".format(r3)]
                #overflow FLAG
                if(VALUES["R{}".format(r1)]>65536):
                    VALUES["R{}".format(r1)]=0
                    VALUES["FLAGS"]=8
                else:
                    reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="10000"): #addf
                val2=VALUES["R{}".format(r2)]
                val3=VALUES["R{}".format(r3)]
                if(type(val2)==str and type(val3)==str):    
                    val1=ieee_to_decimal(val2)+ieee_to_decimal(val3)
                    if(float_binary(val1)=='error'):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                elif(type(val2)==int and type(val3)==str):
                    val1=val2+ieee_to_decimal(val3)
                    if(float_binary(val1)=='error'):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                elif(type(val2)==str and type(val3)==int):
                    val1=ieee_to_decimal(val2)+val3
                    if(float_binary(val1)=='error'):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                elif(type(val2)==int and type(val3)==int):
                    val1=val2+val3
                    if(float_binary(val1)=='error'):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="10001"): #subf
                val2=VALUES["R{}".format(r2)]
                val3=VALUES["R{}".format(r3)]
                if(type(val2)==str and type(val3)==str):    
                    val1=ieee_to_decimal(val2)-ieee_to_decimal(val3)
                    if(float_binary(val1)=='error'or val1<0):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                elif(type(val2)==int and type(val3)==str):
                    val1=val2-ieee_to_decimal(val3)
                    if(float_binary(val1)=='error'or val1<0):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                elif(type(val2)==str and type(val3)==int):
                    val1=ieee_to_decimal(val2)-val3
                    if(float_binary(val1)=='error'or val1<0):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                elif(type(val2)==int and type(val3)==int):
                    val1=val2-val3
                    if(float_binary(val1)=='error'or val1<0):
                        VALUES["R{}".format(r1)]="00000000"
                        VALUES["FLAGS"]=8
                    else:
                        VALUES["R{}".format(r1)]=float_binary(val1)
                        reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="01010"): #bitwise xor
                VALUES["R{}".format(r1)]=VALUES["R{}".format(r2)]^VALUES["R{}".format(r3)]
                reset()
                regout()
                pc+=1
 
            elif(opcode(instruction)=="01011"):  #bitwise or
                VALUES["R{}".format(r1)]=VALUES["R{}".format(r2)]|VALUES["R{}".format(r3)]
                reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="01100"):  #bitwise and
                VALUES["R{}".format(r1)]=VALUES["R{}".format(r2)]&VALUES["R{}".format(r3)]
                reset()
                regout()
                pc+=1


        #Type B
        elif(opcode(instruction) in TYPE_B):
            if(opcode(instruction)=="10010"):
                r=int(instruction[5:8],2)
                imm=(instruction[8:])
                VALUES["R{}".format(r)]=imm
                reset()
                regout()
                pc+=1
            
            else:
                r=int(instruction[6:9],2)
                imm=int(instruction[9:16],2)

                if(opcode(instruction)=="00010"): #mov immediate
                    VALUES["R{}".format(r)]=imm
                    reset()
                    regout()
                    pc+=1
                
                elif(opcode(instruction)=="01000"): #right shift
                    VALUES["R{}".format(r)]=VALUES["R{}".format(r)]>>imm
                    reset()
                    regout()
                    pc+=1

                elif(opcode(instruction)=="01000"): #left shift
                    VALUES["R{}".format(r)]=VALUES["R{}".format(r)]<<imm
                    reset()
                    regout()
                    pc+=1

        #Type C
        elif(opcode(instruction) in TYPE_C):
            r1=int(instruction[10:13],2)
            r2=int(instruction[13:16],2)
            if(r2==7):
                r_2="FLAGS"
            else:
                r_2="R{}".format(r2)

            if(opcode(instruction)=="00011"): #mov reg1 reg2
                VALUES["R{}".format(r1)]=VALUES[r_2]
                reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="00111"): #div
                if(VALUES["R{}".format(r2)]==0):
                    VALUES["FLAGS"]=8
                    VALUES["R0"]=0
                    VALUES["R1"]=0
                    regout()
                    pc+=1
                else:
                    VALUES["R0"]=VALUES["R{}".format(r1)]//VALUES["R{}".format(r2)]
                    VALUES["R1"]=VALUES["R{}".format(r1)]%VALUES["R{}".format(r2)]
                    reset()
                    regout()
                    pc+=1
            
            elif(opcode(instruction)=="01101"): #not
                a=VALUES["R{}".format(r2)]
                s=format(a,"016b")
                s=flip(s)
                y=int(s,2)
                VALUES["R{}".format(r1)]=y
                reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="01110"): #cmp
                val1=VALUES["R{}".format(r1)]
                val2=VALUES["R{}".format(r2)]
                if(type(val1)==str and type(val2)==str):
                    if(val1==val2):
                        VALUES["FLAGS"]=1
                    elif(ieee_to_decimal(val1)>ieee_to_decimal(val2)):
                        VALUES["FLAGS"]=2
                    elif(ieee_to_decimal(val1)<ieee_to_decimal(val2)):
                        VALUES["FLAGS"]=4
                elif(type(val1)==int and type(val2)==str):
                    val2=ieee_to_decimal(val2)
                    if(val1==val2):
                        VALUES["FLAGS"]=1
                    elif(val1>val2):
                        VALUES["FLAGS"]=2
                    elif(val1<val2):
                        VALUES["FLAGS"]=4
                elif(type(val1)==str and type(val2)==int):
                    val1=ieee_to_decimal(val1)
                    if(val1==val2):
                        VALUES["FLAGS"]=1
                    elif(val1>val2):
                        VALUES["FLAGS"]=2
                    elif(val1<val2):
                        VALUES["FLAGS"]=4
                else:
                    if(val1==val2):
                        VALUES["FLAGS"]=1
                    elif(val1>val2):
                        VALUES["FLAGS"]=2
                    elif(val1<val2):
                        VALUES["FLAGS"]=4

                regout()
                pc+=1

        #Type-D
        elif(opcode(instruction) in TYPE_D):
            r1=int(instruction[6:9],2)
            addr=instruction[9:16]

            if(opcode(instruction)=="00100"): #load
                if(addr not in memory.keys()):
                    VALUES["R{}".format(r1)]=0
                else:
                    VALUES["R{}".format(r1)]=int(memory[addr],2)
                reset()
                regout()
                pc+=1

            elif(opcode(instruction)=="00101"): #store
                if(type(VALUES["R{}".format(r1)])==str):
                    memory[addr]=VALUES["R{}".format(r1)]
                    while(len(memory[addr])!=16):
                        memory[addr]="0"+memory[addr]
                else:
                    memory[addr]=format(VALUES["R{}".format(r1)],"016b")
                reset()
                regout()
                pc+=1

        #Type-E
        elif(opcode(instruction) in TYPE_E): 
            mem=instruction[9:16]
            if(opcode(instruction)=="01111"): #unconditional jump
                reset()
                regout()
                pc=mem_key.index(mem)

            elif(opcode(instruction)=="11100"): #jump less than
                if(VALUES["FLAGS"]==4):
                    reset()
                    regout()
                    pc=mem_key.index(mem)
                else:
                    reset()
                    regout()
                    pc+=1
            
            elif(opcode(instruction)=="11101"): #jump if greater than
                if(VALUES["FLAGS"]==2):
                    reset()
                    regout()
                    pc=mem_key.index(mem)
                
                else:
                    reset()
                    regout()
                    pc+=1 
            
            elif(opcode(instruction)=="11111"): #jump if equal
                if(VALUES["FLAGS"]==1):
                    reset()
                    regout()
                    pc=mem_key.index(mem)
                else:
                    reset()
                    regout()
                    pc+=1

    reset()
    regout()


    for i in memory.values():
        sys.stdout.write(i+"\n")

    for i in range(128-len(memory)):
        sys.stdout.write("0"*16+"\n")

main()