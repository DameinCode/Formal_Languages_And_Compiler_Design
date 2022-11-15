# This is crazy

# Q : Finite set of states.
# Σ : set of Input Symbols.
# q : Initial state.
# F : set of Final States.
# δ : Transition Function.

import re

# Function to check if everything is okay 
def checkFunc(curState, inx):
    if(inx == len(strToCheck)):
        if(isFinal(curState)):
            print("Accepted!")
            exit(0)
        return
    if((curState, strToCheck[inx]) in transition):
        for i in transition[(curState, strToCheck[inx])]:
            checkFunc(i, inx+1)
    else: 
        return 

def isFinal(state):
    for i in finals:
        if(state == i):
            return True
    return False

finiteAutomata = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/LAB5/String_FA/FA.txt", "r")

states = []
alphabet = []
finals = []
transition = {}

initial = 0

for line in finiteAutomata: 
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
        # _ . $ # ! % ^ & * - = / ~ ' " ` 
        temp = re.findall("[a-zA-Z]+", line)
        for i in range(0, len(temp), 3):
            if((temp[i], temp[i+1]) in transition):
                transition[(temp[i], temp[i+1])].append(temp[i+2])
                continue
            transition[(temp[i], temp[i+1])] = [temp[i+2]]

# print(initial)
# print(states)
# print(finals)
# print(alphabet)
# print(transition)
# for i in transition:
#     print(i, transition[i])

strToCheck = input("Input the string: ")

current_state = initial
checkFunc(current_state, 0)
print("Not accepted! Failed")
