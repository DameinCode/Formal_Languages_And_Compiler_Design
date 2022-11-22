import re
from hashTable import HashTable
import pandas as pd

programCode = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/lab5/Id_Const_FA/program.txt", "r")
tokens = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/lab5/Id_Const_FA/token.txt", "r")


code_arrayOfLine = []
operators = {"+", "-", "%", "/", "*", "=", ">", "<", ">=", "<=", "==", "||", "&&"}
separators = {";", "[", "]", "{", "}", "(", ")", ","} 
dataTypes = {"int", "string", "float", "const", "char"}
keywords = {"for", "if", "else", "Add", "return", "print", "while", "main", "array"}
special_quote = {"t", "n", "\\", '"'}

tokender = {}
pif = []
comments = []
errors = []
backslash = []

identifiers = HashTable()
constantas = HashTable()

for line in tokens:
    toks = re.split("\s", line)
    if(toks):
        tokender[toks[0]] = toks[1]


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

def get_codes_array():

    for line in programCode:
        if(line.find("//") != -1):
            comments.append(line[line.find("//"):-1]) # adding comment to the comment list
        line = line[:line.find("//")]
        strtemp = ""
        comingStr2 = False
        comingStr1 = False
        temp_arr = []
        for i in range(0, len(line)): 
            if(line[i] == '"' and comingStr1 == False and comingStr2 == False):
                comingStr1 = True
                if(strtemp != ''):
                    temp_arr.append(strtemp)
                strtemp = ""
            elif(line[i] == '"' and comingStr1 == True): 
                strtemp += line[i]
                temp_arr.append(strtemp)
                strtemp = ''
                comingStr1 = False
                continue
            elif(line[i] == "'" and comingStr2 == False and comingStr1 == False):
                comingStr2 = True
                if(strtemp != ''):
                    temp_arr.append(strtemp)
                strtemp = ""
            elif(line[i] == "'" and comingStr2 == True): 
                strtemp += line[i]
                temp_arr.append(strtemp)
                comingStr2 = False
                strtemp = ""
                continue
            if((line[i] in separators or line[i] in operators) and comingStr2 == False and comingStr1 == False):
                if(strtemp != '' and strtemp != " "):
                    temp_arr.append(strtemp)
                temp_arr.append(line[i])
                strtemp = ""
                continue

            if((line[i] == " " or i == len(line)-1) and comingStr2 == False and comingStr1 == False):
                if(strtemp != '' and strtemp != " "):
                    if(line[i] != " "):
                        temp_arr.append(strtemp+line[i])
                    else:
                        temp_arr.append(strtemp)
                elif(line[i] != " "):
                    temp_arr.append(strtemp+line[i])
                strtemp = ""
                continue
            strtemp += line[i]

        if(len(temp_arr) != 0):
            code_arrayOfLine.append(temp_arr)

def main_operations():
    inx = 0
    cnx = 0
    for line in code_arrayOfLine:
        isOkInit = False
        for word in line:
            if(word in tokender):
                pif.append({word: tokender[word], 'ans': "-1"})
            if ((word in dataTypes) or word == "Add"):
                isOkInit = True
                continue
            if (word in keywords):
                continue
            if(word in operators):
                isOkInit = False
                continue
            if(word in separators):
                continue
            checkIdentifier = checkFAID(initial_id, 0, word)
            if(checkIdentifier == True and isOkInit == True and word != '' or word.find(".") != -1): #check if name is acceptable for identifier
                if (identifiers.insert(word, inx)): 
                    pif.append({word: 2, 'ans': inx})
                    inx += 1
            elif(identifiers.find(word) and word != ''): # Identifier already in a hash table we just add it to pif 
                pif.append({word: 2, 'ans': identifiers.get_value(word)})
            elif(checkIdentifier == True and isOkInit == False and word != ''): # Name acceptable for an identifier but not correct because data type wasn;t initialized (syntax error)
                errors.append([word, 'What is that, a variable? You seemed not initialized it. Line:', code_arrayOfLine.index(line)])
            elif(isOkInit and checkIdentifier == False and len(word) != 1): # Name is not acceptable, but data type was mentioned. Then we do not add it to identifier hash table because name is not acceptable 
                errors.append([word, 'Wrong name for variable, what is that? Line:', code_arrayOfLine.index(line)])
            else:
                if(len(word) >= 2):
                    if(word[1] == "\\"[0]):
                        if(word[len(word)-2] in special_quote and len(word) == 4):
                            backslash.append(word)
                            continue
                        else:
                            errors.append([word, "Backslash error. Line:", code_arrayOfLine.index(line)])

                if(checkFAConst(initial_const, 0, word)):
                    if (constantas.find(word) == False): 
                        constantas.insert(word, cnx)
                        pif.append({word: 3, 'ans': cnx})
                        cnx += 1
                    else:
                        pif.append({word: 3, 'ans': constantas.get_value(word)})
                else:
                    errors.append([word, "Error appeared. Non clear word-element. Line:", code_arrayOfLine.index(line)])
                
            
states_id, alphabet_id, initial_id, finals_id, transition_id = FA_identifiers_Const("id")
states_const, alphabet_const, initial_const, finals_const, transition_const = FA_identifiers_Const("const")
get_codes_array()
main_operations()



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
