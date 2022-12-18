# LL(1)
# Output - determines that given string can be produced by given grammar(parsing table) or not, if not then it produces an error.
from array import *
import grammar
import parseTableClass
import re
from tabulate import tabulate

output_file = open("C:/Users/user/Documents/Semester#7/FLACT/LABS/Parser/Data/output.txt", "a")
scanner = None
input_string = ""
what_to_parse = int(input("Which file you want to parse? "))
if(what_to_parse == 2):
    import scanner
    input_string = scanner.program_stream

work_stack = ["$", grammar.starting_symbol] # stack containing S (starting symbol)
if(what_to_parse != 2):
    input_string = input("Input string: ")
# input_string += "$" # $ is used for the end of string.
input_stack = input_string.split(" ")
input_stack.append("$")
firstSet = {}
followSet = {}
parse_table_from_class = parseTableClass.ParseTable()
parseTable = []

def FIRST(nonterminal, leftSide, temp):
    firstSetForNonterminal = set({})
    if(nonterminal in firstSet):
        return firstSet[nonterminal]
    for production in grammar.productionForGivenNonterminal(nonterminal):
        for leftSides in production.getRightHandSide():
            firstRule = leftSides[0]
            if (firstRule == "epsilon"):
                if(temp >= len(leftSide)):
                    pass
                elif(leftSide[temp] in grammar.terminals):
                    firstSetForNonterminal.add(leftSide[temp])
                else: 
                    firstSetForNonterminal.update(FIRST(leftSide[temp], leftSide, temp+1))
                firstSetForNonterminal.add(firstRule)
            elif(firstRule in grammar.terminals):
                firstSetForNonterminal.add(firstRule)
            else: # If first symbol in nonterminal
                firstSetForNonterminal.update(FIRST(firstRule, leftSides, temp+1)) 
    return firstSetForNonterminal


def FOLLOW(nonterminal, conflict_rules):
    followSetForNonterminal = set({})
    if(nonterminal in followSet):
        return followSet[nonterminal]
    if(nonterminal == grammar.starting_symbol):
        followSetForNonterminal.add("$")
    for production in grammar.productionsThatContainNonTerminal(nonterminal):
        initialLeftHandSide = production.getLeftHandSide().strip()
        for rules in production.getRightHandSide():
            if(nonterminal in rules):
                for inx, rule in enumerate(rules):
                    if(rule != nonterminal):
                        continue
                    # inx = rules.index(nonterminal) # index of the non terminal in the list of the rules
                    if(inx >= len(rules)-1):
                        if(initialLeftHandSide in conflict_rules):
                            conflict_rules.remove(initialLeftHandSide)
                        else:
                            conflict_rules.append(initialLeftHandSide)
                            followSetForNonterminal.update(FOLLOW(initialLeftHandSide, conflict_rules))
                    elif(rules[inx+1] in grammar.terminals):
                        followSetForNonterminal.add(rules[inx+1])
                    elif(rules[inx+1] in grammar.nonterminals):
                        inx += 1 
                        cont = True   
                        while(inx < len(rules) and cont):
                            if(rules[inx] in grammar.terminals):
                                cont = False
                                followSetForNonterminal.add(rules[inx])
                                break
                            elif("epsilon" in firstSet[rules[inx]]):
                                followSetForNonterminal.update(x for x in firstSet[rules[inx]] if x != "epsilon")
                            else:
                                followSetForNonterminal.update(firstSet[rules[inx]]) 
                                cont = False
                                break
                            inx += 1 
                        if(inx == len(rules) and cont):
                            if(initialLeftHandSide in conflict_rules):
                                conflict_rules.remove(initialLeftHandSide) 
                            else:
                                conflict_rules.append(initialLeftHandSide)
                                followSetForNonterminal.update(FOLLOW(initialLeftHandSide, conflict_rules))

    return followSetForNonterminal
    

def generateFirstSet():
    for nonterminal in grammar.nonterminals:
        firstSet[nonterminal] = FIRST(nonterminal, [], 0)


def generateFollowSet():
    for nonterminal in grammar.nonterminals:
        followSet[nonterminal] = FOLLOW(nonterminal, [nonterminal])

def getParseTable():
    parseTable.append(grammar.nonterminals)
    parseTable.append(grammar.terminals)
    parseTable[1].append("$")
    for nonterminal in parseTable[0]:
        temps = [("err", "-1")]*len(parseTable[1])
        productions = grammar.productionForGivenNonterminal(nonterminal)
        for production in productions:
            for rightSides in production.getRightHandSide():
                firstLeft = rightSides[0]
                if(firstLeft in grammar.terminals):
                    if(firstLeft in temps):
                        if(temps.index(firstLeft) != -1):
                            print("There is a conflict in follow")
                            exit(0)
                        else:
                           temps[parseTable[1].index(firstLeft)] = (" ".join(rightSides), str(production.getIndex()))
                    else:
                        temps[parseTable[1].index(firstLeft)] = (" ".join(rightSides), str(production.getIndex()))
                elif(firstLeft in grammar.nonterminals):
                    for firsts in firstSet[firstLeft]:
                        if(firsts in temps):
                            if(temps.index(firsts) != -1): 
                                print("There is a conflict in first")
                                exit(0)
                            else:
                                temps[parseTable[1].index(firsts)] = (" ".join(rightSides), str(production.getIndex()))
                        elif(firsts == "epsilon"):
                            pass
                        else:
                            temps[parseTable[1].index(firsts)] = (" ".join(rightSides), str(production.getIndex()))
                else: # If production goes to epsilon 
                    for follows in followSet[production.getLeftHandSide().strip()]: # Adding to the table also follows
                        if(follows in temps):
                            if(temps.index(follows) != -1):
                                print("There is a conflict with follow")
                                exit(0)
                            else:
                                temps[parseTable[1].index(follows)] = (" ".join(rightSides), str(production.getIndex()))
                        else:
                            temps[parseTable[1].index(follows)] = (" ".join(rightSides), str(production.getIndex()))
        
        parseTable.append(temps)

    for terminals in parseTable[1]: # Adding non terminals to the end of the table rows where pop methods are included
        parseTable[0].append(terminals)
        temps = [("err", "-1")]*len(parseTable[1])
        for terminsl2_nd in range(0, len(parseTable[1])):
            if(parseTable[1][terminsl2_nd] == terminals):
                if(terminals == "$"):
                    temps[terminsl2_nd] = ("acc", "100") 
                else:
                    temps[terminsl2_nd] = ("pop", "0")  
        parseTable.append(temps)

def getTableFromList(): # Parse table class 
    for i in range(0, len(parseTable[0])):
        for j in range(0, len(parseTable[1])):
            parse_table_from_class.put(parseTable[0][i], parseTable[1][j], parseTable[i+2][j])

def getConvParseTable(): # formatting table to write in a file
    parse_temp = parseTable[2:]
    parseTable1 = []
    heads = ["NTS"]
    heads.extend(grammar.terminals)
    for i in range(0, len(parseTable[0])):
        temp = []
        temp.append(parseTable[0][i])
        temp.extend(parse_temp[i])
        parseTable1.append(temp)

    output_file.write(tabulate(parseTable1, headers=[i for i in heads]))        


def parseSequence():
    parsedTeble = parse_table_from_class.getParseTable()
    output_stack = []
    
    while(True):
        # print(input_stack)
        # print(work_stack)
        if ((work_stack[len(work_stack)-1], input_stack[0]) in parsedTeble):
            # print(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])])
            # print("--"*60)
            if(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])][0] == "pop"):
                output_stack.append(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])][1])
                input_stack.pop(0)
                work_stack.pop(-1)
            elif(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])][0] == "acc"):
                print("Accepted. Syntax correct")
                print(output_stack)
                break
            elif(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])][0] == "err"):
                print(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])])
                print((work_stack[len(work_stack)-1], input_stack[0]))
                print("Error occured in location: ", input_stack[0], input_stack[1])
                break
            else:
                output_stack.append(parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])][1])
                temp = work_stack.pop(len(work_stack)-1)
                # parsedTeble[(work_stack[len(work_stack)-1], input_stack[0])][0][::-1]
                for values in parsedTeble[(temp, input_stack[0])][0].split(" ")[::-1]: 
                    # print(values)
                    if(values == "epsilon"):
                        # print("IS epsilon")
                        continue
                    work_stack.append(values)
        else:
            print((work_stack[len(work_stack)-1], input_stack[0]))
            print("Error: wrong input") 
            break

def getEXCELparsetable():
    pass

generateFirstSet()
generateFollowSet()
getParseTable()
getTableFromList()
parseSequence()
getEXCELparsetable()

# print(parse_table_from_class)
# Writing to file the follow and first set: 

output_file.write("                                   FOLLOW SET: \n")
for i in followSet:
    output_file.write(str(i) + " <---> [ ")
    output_file.write(", ".join(followSet[i]))
    output_file.write(" ]")
    output_file.write("\n")
output_file.write("\n\n\n\n")

output_file.write("                                    FIRST SET: \n")
for i in firstSet:
    output_file.write(str(i) + " <---> [ ")
    output_file.write(", ".join(firstSet[i]))
    output_file.write(" ]")
    output_file.write("\n")
output_file.write("\n\n\n\n")

output_file.write("                                    PARSE TABLE: \n")
# print(tabulate())
getConvParseTable()