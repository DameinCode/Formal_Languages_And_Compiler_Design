from asyncio import constants
import re
input_program = open("C:/Users/user/Documents/Semester#7/FLACT/LAB2/program.txt", "r")
tokens = open("C:/Users/user/Documents/Semester#7/FLACT/LAB2/tokens.txt", "w")


dataTypes = {"int", "string", "float", "const", "char"}
keywords = {"for", "if", "else", "Add", "return", "print", "while", "main"}
operators = {"+", "-", "%", "/", "*", "=", ">", "<", ">=", "<=", "==", "||", "&&"}
separators = {";", "[", "]", "{", "}", "(", ")"}
letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
digits = "1234567890"
s_symbols = "_"

tester = [operators, separators]

keywords1 = [] 
operators1 = [] 
separators1 = [] 
s_symbols1 = []
lexical_errors = {}
identifiers = {}
constantas = []
errors = []

def checkForConst(word):
    if(word[0] in digits):
        for w in word: 
            if (w in digits):
                continue
            errors.append(word)
            return False
        constantas.append(word) # integer
        return True
    if(word.find('.') != -1):
        if((word[:word.find('.')] + word[word.find('.')+1:]).isnumeric()):
            constantas.append(word) # it means that it is float  
            return True
    if(word[0] == "'" or  word[0] == '"'):
        constantas.append(word) # string or char
        return True     

def checkForReserve(word):
    if (word in keywords):
        keywords1.append(word)
        return True
        # i += len(word)
    elif (word in dataTypes):
        keywords1.append(word)
        return True
        # temp = True
        # i += len(word)
    return False
# 


def checkForID(word, temp):
    if(word[0] in digits or word[0] == "'" or  word[0] == '"'):
        return checkForConst(word)
    if(word in identifiers):
        return True
    if(temp):
        for w in word:
            if (w in digits or w in letters):
                continue
            errors.append(word)
            return False
        identifiers[word] = word
        return True
    errors.append(word)
    return False


for line in input_program:

    words = re.split("\s", line)
    words = filter(lambda x: x != "", words)
    temp = False
    jst_str = []
    i = 0
   
    for word in list(words):
        if (word in keywords):
            keywords1.append(word)
            i += len(word)
        elif (word in dataTypes):
            keywords1.append(word)
            temp = True
            i += len(word)

    word = re.sub(" ", "", line)
    # word = word[i:len(word)-1]
    for data in dataTypes: 
        if(word.find("for("+ str(data)) != -1):
            keywords1.append("for")
            keywords1.append(data)
            temp = True
            i += len("for("+ str(data))

    word = word[i:len(word)-1]
    for w in range(0, len(word)):
        if (word[w] in separators or word[w] in operators):
            jst_str.append(w)
        
    if (jst_str):
        first = word[:jst_str[0]]
        second = word[jst_str[len(jst_str)-1]+1:]

        for i in range(1, len(jst_str), 1):
            if(word[jst_str[i-1]+1:jst_str[i]]):
                if(checkForReserve(word[jst_str[i-1]+1:jst_str[i]]) == False):
                    checkForID(word[jst_str[i-1]+1:jst_str[i]], temp)
                # print(word[jst_str[i-1]+1:jst_str[i]])
        if(first):
            if (checkForReserve(first) == False):
                checkForID(first, temp)
        if(second):
            if (checkForReserve(second) == False):
                checkForID(second, temp)

    else:
        if (word):
            checkForReserve(word)
            checkForID(word, temp)

print(keywords1)
print(identifiers)
print(constantas)
print(errors)