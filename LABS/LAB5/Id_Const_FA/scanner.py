import re
from hashTable import HashTable
import pandas as pd



# Functions:
def isFinal(state, finals):
    for i in finals:
        if(state == i):
            return True
    return False


def checkFAID(curState, inx, strToCheck):
    if(inx == len(strToCheck)):
        return isFinal(curState, finals_id)
    labada = strToCheck[inx].lower()
    if((curState, labada) in transition_id):
        for i in transition_id[(curState, labada)]:
            return checkFAID(i, inx+1, strToCheck)
    else: 
        return False

def checkFAConst(curState, inx, strToCheck):
    if(inx == len(strToCheck)):
        if(isFinal(curState, finals_const)):
            return True
        else:
            return False
    labada = strToCheck[inx].lower()
    if(strToCheck[inx] == " " or strToCheck[inx] == ')' or strToCheck[inx] == '('):
        labada = "a"
    if((curState, labada) in transition_const):
        for i in transition_const[(curState, labada)]:
            return checkFAConst(i, inx+1, strToCheck)
    else: 
        return False

def FA_identifiers_Const(finiteAutomata): 
    transition = {}
    states = []
    finals = []
    initial = ''
    alphabet = []
    if(finiteAutomata == "id"):
        fileToOpen = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB5/Id_Const_FA/Identifiers.txt", "r")
    else:
        fileToOpen = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB5/Id_Const_FA/ConstFA.txt", "r")
    for line in fileToOpen: 
        words = re.split("\s", line)
        if(words[0] == "states"):
            states = list(filter(lambda x: x != "", (re.split("\s", line[line.find("=")+1:]))))
        elif(words[0] == "alphabet"):
            alphabet = list(filter(lambda x: x != "", (re.split("\s", line[line.find("=")+1:]))))
        elif(words[0] == "initial"):
            initial = re.split("\s", line[line.find("=")+1:])[1]
        elif(words[0] == "final"):
            finals = list(filter(lambda x: x != "", (re.split("\s", line[line.find("=")+1:]))))
        else: 
            line = line[line.find("[")+1:-2]
            temp = re.findall("[a-zA-Z]|[0-9]|_|\.|\#+|\%|\$|\@|\!|\~|\+|\*|\^|\'|\"|\`|\-|\/|&|\:", line)
            for i in range(0, len(temp), 3):
                if((temp[i], temp[i+1]) in transition):
                    transition[(temp[i], temp[i+1])].append(temp[i+2])
                    continue
                transition[(temp[i], temp[i+1])] = [temp[i+2]]
    return states, alphabet, initial, finals, transition


input_program = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB4/program.txt", "r")
tokens = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB4/token.txt", "r")


dataTypes = {"int", "string", "float", "const", "char"}
keywords = {"for", "if", "else", "Add", "return", "print", "while", "main", "array"}
operators = {"+", "-", "%", "/", "*", "=", ">", "<", ">=", "<=", "==", "||", "&&"}
separators = {";", "[", "]", "{", "}", "(", ")", ","}
letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
digits = "1234567890"
special_quote = {"t", "n", "\\", '"'}

tokender = {}

for line in tokens:
    toks = re.split("\s", line)
    if(toks):
        tokender[toks[0]] = toks[1]

pif = []

keywords1 = {} 
operators1 = {} 
separators1 = {} 
identifiers = HashTable()
constantas = HashTable()
errors = []
backslash  = []
comments = []
strings = []
inx = 0
cnx = 0
lepe = 0

states_id, alphabet_id, initial_id, finals_id, transition_id = FA_identifiers_Const("id")
states_const, alphabet_const, initial_const, finals_const, transition_const = FA_identifiers_Const("const")

for line in input_program:
    lepe += 1
    temp = False
    isConst = False
    temp_arr = []
    find_string_const1 = False
    find_string_const2 = False
    temp_str = ""
    if(line.find("//") != -1):
        comments.append(line[line.find("//"):-1]) # adding comment to the comment list
    line = line[:line.find("//")]  # comment finding 
   
    words = re.split("\s", line) 
    words = filter(lambda x: x != "", words) # getting lines of program code as a list 


    stringChecking = False
    checkStr = ''
    checkIdentifier = False
    for word in list(words): 
        str = ""
        d = ''
        cnt = 0 
        for w in word: 
            if (w in separators and w != '' and stringChecking == False):
                if(str != ''):
                    temp_arr.append(str)
                temp_arr.append(w)

                w = ''
                str = ""
            
            if (w in operators and w != '' and stringChecking == False):
                if(str != ''):
                    temp_arr.append(str)
                temp_arr.append(w)

                w = ''
                str = ""

            str += w
        temp_arr.append(str)

    # print(temp_arr)    
    for word in temp_arr:
        if (word == ''):
            continue
        if(word in tokender):
            pif.append({word: tokender[word], 'ans': "-1"})
        if (word in dataTypes and stringChecking == False):
            if(word in keywords1):
                keywords1[word] += 1
            else:     
                keywords1[word] = 1
            temp = True 
            continue
        if (word in keywords and stringChecking == False):
            if(word in keywords1):
                keywords1[word] += 1
            else:     
                keywords1[word] = 1
            continue

        if(word in separators and stringChecking == False):
            if(word in separators1):
                separators1[word] += 1
            else:
                separators1[word] = 1
            continue

        if(word in operators and stringChecking == False):
            isConst = True
            if(word in operators1):
                operators1[word] += 1
            else:
                operators1[word] = 1
            continue

        
        checkIdentifier = checkFAID(initial_id, 0, word) # check for identifier name if acceptable or not by FA
        if(checkIdentifier == True and temp == True and word != ''): #check if name is acceptable for identifier
            if (identifiers.insert(word, inx)): 
                pif.append({word: 2, 'ans': inx})
                inx += 1
        elif(identifiers.find(word) and word != '' and stringChecking == False): 
            pif.append({word: 2, 'ans': identifiers.get_value(word)})
        elif(checkIdentifier == True and temp == False and word != '' and stringChecking == False):
            errors.append([word, 'What is that, a variable? Line', lepe])
        elif(temp and checkIdentifier == False and len(word) != 1 and isConst == False): # 
            errors.append([word, 'Wrong name for variable, what is that Line', lepe])
        
        # elif(checkIdentifier == False): 
            # maybe it is a const? Check for acceptance by FA
        else:
            if(checkFAConst(initial_const, 0, word) and stringChecking == False):
                if (constantas.find(word) == False): 
                    constantas.insert(word, cnx)
                    pif.append({word: 3, 'ans': cnx})
                    cnx += 1
                else:
                    pif.append({word: 3, 'ans': constantas.get_value(word)})
        #       
            if(len(word) >= 2):
                if(word[1] == "\\"[0] and stringChecking == False):
                    if(word[len(word)-2] in special_quote and len(word) == 4):
                        backslash.append(word)
                    else:
                        errors.append([word, "Backslash error Line", lepe])
            if(word != '' and constantas.find(word) == False):
                checkStr = checkStr + word + " "
                stringChecking = True
                if(constantas.find(checkStr[:-1]) == True):
                    pif.append({checkStr[:-1]: 3, 'ans': constantas.get_value(checkStr[:-1])})
                    checkStr = ''
                    stringChecking = False
                if(checkFAConst(initial_const, 0, checkStr[:-1])): 
                    constantas.insert(checkStr[:-1], cnx)
                    pif.append({checkStr: 3, 'ans': cnx})
                    cnx += 1
                    checkStr = ''
                    stringChecking = False
                else: 
                    continue
            else:
                if(checkStr != ''):
                    errors.append([checkStr, "Line",  lepe])


indexx = []

iden = identifiers.get_nodes()
con = constantas.get_nodes()

writer = pd.ExcelWriter('output.xlsx', engine='openpyxl') 
wb  = writer.book
dataframe_id = pd.DataFrame({'Identifiers: ': [i for i in iden[::2]], 
                          'Token': [i for i in iden[1:(len(iden)):2]]
                          })

dataframe_const = pd.DataFrame({ 'Const: ': [i for i in con[::2]],
                            'Token': [i for i in con[1:(len(con)):2]]
                            })

dataframe_pif = pd.DataFrame({'Token': [j for i in pif for j in i if j != 'ans'],
                            'Index': [i[j] for i in pif for j in i if j != 'ans'],
                            'Idk': [i[j] for i in pif for j in i if j == 'ans']
                            })

identify = pd.DataFrame({"Identifiers: ": []})
constify = pd.DataFrame({"Const: ": []})

identify.to_excel(writer, index = False, startrow=0) 
dataframe_id.to_excel(writer, index=False, startrow = 2)
constify.to_excel(writer, index=False, startcol = 4, startrow=0)
dataframe_const.to_excel(writer, index=False, startrow=2, startcol=4)
dataframe_pif.to_excel(writer, index=False, startrow=18, startcol = 2)

wb.save('output.xlsx')

print('Errors: ', errors)
print('Blackslash: ', backslash)
print('Comments: ', comments)
