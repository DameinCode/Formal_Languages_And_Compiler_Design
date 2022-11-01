import re
from hashTable import HashTable
import pandas as pd


input_program = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB4/program.txt", "r")
tokens = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB4/token.txt", "r")
symbol_table = "C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB4/symboltable.txt"

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
for line in input_program:
    lepe += 1
    temp = False
    isConst = False
    temp_arr = []
    find_string_const1 = False
    find_string_const2 = False
    temp_str = ""
    if(line.find("//") != -1):
        comments.append(line[line.find("//"):-1])
    line = line[:line.find("//")]

    if(line):
        for l in line:
            if (l == "'"): 
                if(find_string_const1):
                    find_string_const1 = False
                    temp_str += l
                    strings.append(temp_str)
                    line = line.replace(temp_str, '~'*len(temp_str))
                    temp_str = ''
                elif(find_string_const2 == False):
                    find_string_const1 = True
            if (l == '"'):
                if(find_string_const2):
                    find_string_const2 = False
                    temp_str += l
                    strings.append(temp_str)
                    line = line.replace(temp_str, '~'*len(temp_str))
                    temp_str = ''
                elif(find_string_const1 == False):
                    find_string_const2 = True
            if (find_string_const1 or find_string_const2):
                temp_str += l
                continue
   
    words = re.split("\s", line)
    words = filter(lambda x: x != "", words)

    for word in list(words): 
        str = ""
        d = ''
        cnt = 0 
        isStr = False

        for w in word: 
 
            if(w == '~'):
                cnt += 1 
                isStr = True
                continue

            if(isStr):
                if(cnt == len(strings[0])):
                    # print("yes", strings[0])
                    temp_arr.append(strings[0])
                    strings.pop()
                    cnt = 0
                    isStr = False 
        
            if (w in separators and w != '' ):
                if(str != ''):
                    temp_arr.append(str)
                temp_arr.append(w)

                w = ''
                str = ""
            
            if (w in operators and w != ''):
                if(str != ''):
                    temp_arr.append(str)
                temp_arr.append(w)
                w = ''
                str = ""

            str += w
            
        temp_arr.append(str)
        # strings.append(str)

    
    # print(temp_arr)
    
    for word in temp_arr:
        if(word in tokender):
            pif.append({word: tokender[word], 'ans': "-1"})
        if (word in dataTypes):
            if(word in keywords1):
                keywords1[word] += 1
            else:     
                keywords1[word] = 1
            temp = True 
            continue
        if (word in keywords):
            if(word in keywords1):
                keywords1[word] += 1
            else:     
                keywords1[word] = 1
            continue

        if(word in separators):
            if(word in separators1):
                separators1[word] += 1
            else:
                separators1[word] = 1
            continue

        if(word in operators):
            isConst = True
            if(word in operators1):
                operators1[word] += 1
            else:
                operators1[word] = 1
            continue

        yes = True # is acceptable name for variable?
        for w in word: 
            if ((w in digits or w in letters or w == "_" or w == ".")and word[0] in letters):
                continue
            yes = False # Name is not acceptable for variable, maybe it is a const?
        if(yes and temp == True and word != ''):
            if (identifiers.insert(word, inx)):
                pif.append({word: 2, 'ans': inx})
                inx += 1
        elif(identifiers.find(word) and word != ''): 
            pif.append({word: 2, 'ans': identifiers.get_value(word)})
        elif(yes and temp == False and word != ''):
            errors.append([word, 'What is that, a variable? Line', lepe])
        elif(temp and yes == False and len(word) != 1 and isConst == False): 
            errors.append([word, 'Wrong name for variable, what is that Line', lepe])
        
        elif(word and yes == False):
            if(re.match('^[0-9]*$', word) and word != ''):
                if (constantas.find(word) == False): 
                    constantas.insert(word, cnx)
                    pif.append({word: 3, 'ans': cnx})
                    cnx += 1
                else:
                    pif.append({word: 3, 'ans': constantas.get_value(word)})
            elif(word[1] == "\\"[0]):
                if(word[len(word)-2] in special_quote and len(word) == 4):
                    backslash.append(word)
                else:
                    errors.append([word, "Backslash error Line", lepe])
            elif(word[0] == '"' or word[0] == "'"):
                if (constantas.find(word) == False): 
                    constantas.insert(word, cnx)
                    pif.append({word: 3, 'ans': cnx})
                    cnx += 1
                else:
                    pif.append({word: 3, 'ans': constantas.get_value(word)})
            else:
                errors.append([word, "Line",  lepe])
        else:
            if(word != ''):
                errors.append([word, "Line", lepe])


# with open(symbol_table, 'a') as st:
#     st.write('Const symbol Table\n')
#     st.write('-------------------')
#     for i in constantas.get_nodes():
#         st.write("\n")
#         st.write(i)
#     st.write("\n\n\n")
#     st.write('Identifier symbol Table\n')
#     st.write('-----------------------')
#     for i in identifiers.get_nodes():
#         st.write("\n")
#         st.write(i)
    

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
