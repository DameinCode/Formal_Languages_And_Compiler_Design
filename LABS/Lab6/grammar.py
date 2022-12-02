import production
from collections import deque

grammar = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/Lab5_grammar/g2.txt", "r")

nonterminals = {}
terminals = {}
starting_symbol = ''
productions = []
productions_with_terminals = {}

# Reading from file
for i, line in enumerate(grammar): #index and line
    if(i == 0): #It is non terminal set
        nonterminals = line.split(" ")
        nonterminals[len(nonterminals)-1] = nonterminals[len(nonterminals)-1].strip()
    elif(i == 1): #Terminals 
        terminals = line.split(" ")
        terminals[len(terminals)-1] = terminals[len(terminals)-1].strip()
    elif(i == 2): #starting symbol
        starting_symbol = line.strip()
    else:
        temp = line.split("->") # splitting to get start and 
        production_rules = temp[1].split("|")
        temp_rules = []
        for rules in production_rules: 
            for rule in(rules.split("|")):
                temp_temp = []
                for smth in (rules.split(" ")):
                    if(smth.strip() != ""):
                        temp_temp.append(smth.strip())
                temp_rules.append(temp_temp)
        productions.append(production.Production(temp[0], temp_rules))
    

def isCFG(): #checking grammar 
    is_ok = False 
    for production in productions: 
        if(production.getLeftHandSide().strip() == starting_symbol.strip()):
            is_ok = True
            break 

    if(is_ok == False):
        return False
    
    for production in productions:
        right_hand_side = production.getRightHandSide()
        left_hand_side = production.getLeftHandSide()
        if (left_hand_side in nonterminals == False):
            return False
        for rules in right_hand_side: 
            for rule in rules:
                if(rule in nonterminals or rule in terminals or rule == "epsilon"):
                    continue
                return False
    return True

print("--"*40, "\n")
print("Non terminals: ", "\n", nonterminals, "\n")
print("--"*40, "\n")
print("Terminals: ", "\n", terminals, "\n")
print("--"*40, "\n")
print("Starting symbol: ", starting_symbol, "\n")
print("--"*40, "\n")
print("Productions: ")
for production in productions:
    print(production)
print("--"*40, "\n")
print("Is grammar context-free ?")
# isCFG()
print("-->", isCFG())
