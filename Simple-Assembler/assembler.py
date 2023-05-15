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

main()

