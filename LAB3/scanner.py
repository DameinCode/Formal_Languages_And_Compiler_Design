import re
from hashTable import HashTable

input_program = open("C:/Users/user/Documents/Semester#7/FLACT/LAB3/program.txt", "r")


dataTypes = {"int", "string", "float", "const", "char"}
keywords = {"for", "if", "else", "Add", "return", "print", "while", "main", "array"}
operators = {"+", "-", "%", "/", "*", "=", ">", "<", ">=", "<=", "==", "||", "&&"}
separators = {";", "[", "]", "{", "}", "(", ")", ","}
letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
digits = "1234567890"
special_quote = {"t", "n", "\\", '"'}


keywords1 = {} 
operators1 = {} 
separators1 = {} 
identifiers = HashTable()
constantas = HashTable()
errors = []
backslash  = []
comments = []
inx = 0
cnx = 0
for line in input_program:

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
                    temp_arr.append(temp_str)
                    line = line.replace(temp_str, '')
                    temp_str = ''
                elif(find_string_const2 == False):
                    find_string_const1 = True
            if (l == '"'):
                if(find_string_const2):
                    find_string_const2 = False
                    temp_str += l
                    temp_arr.append(temp_str)
                    line = line.replace(temp_str, '')
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

        for w in word: 
        
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

    for word in temp_arr:
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

        yes = True
        for w in word: 
            if ((w in digits or w in letters or w == "_")and word[0] in letters):
                continue
            yes = False
        if(yes and temp == True and word != ''):
            identifiers.insert(word, inx)
            inx += 1
        elif(yes and temp == False and word != ''):
            errors.append([word, 'What is that, a variable? '])
        elif(temp and yes == False and len(word) != 1 and isConst == False): 
            errors.append([word, 'Wrong name for variable, what is that'])
        elif(word and yes == False):
            if(re.match('^[0-9]*$', word) and word != ''): 
                constantas.insert(word, cnx)
                cnx += 1
            elif(word[1] == "\\"[0]):
                if(word[len(word)-2] in special_quote and len(word) == 4):
                    backslash.append(word)
                else:
                    errors.append([word, "Wrong usage of blackslash"])
            elif(word[0] == '"' or word[0] == "'"):
                constantas.insert(word, cnx)
                cnx += 1
            else:
                errors.append([word, 'Whats that?'])
        else:
            if(word != ''):
                errors.append([word, 'Wrong symbol, check'])

print('Constantas: ')
print(constantas.get_nodes())
print("\n")
print("--"*60)
print('Identifiers: ')
print(identifiers.get_nodes())

print("\n")
print("--"*60)
print("Keywords: ", keywords1)
print("Separators: ", separators1)
print("Operators: ", operators1)
# print('Errors: ', errors)
print('Blackslash: ', backslash)
print('Comments: ', comments)