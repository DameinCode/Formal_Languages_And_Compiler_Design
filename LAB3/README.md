# Formal_Languages_And_Compiler_Design
Lab 3

## Collision   
Chaining is a technique used for avoiding collisions in hash tables. Used chaining techniwue to avoid collision. For that, I checked the hash of the element 2 times(2 different formulas). Like if a and b gives the same hash like 0. I added these elements to the 0-th list in hash table and checked for 2 time to get the index to place in the sublist. [[a,b], [...], ...];

## Symbol Table 
2 different symol tables: Identifiers and Consts. 

## Сonsidered 
First Header  | Second Header 
------------- | ------------------------------------------------------------------------------------------
Comments      | Scan the comment and add it to comments list
a=2 and a = 2 | Wors fine, scanner can scan both situation and add "a" to iden and "2" to const hash table

To analyze the identifiers and consts without space I looked at the operators. And devide them to identifier and const depending on in which side is operators. Found operator and the left is identifier, the right is const(if operator is: = ). If operators are: + - * % or etc. then it is const 

### Files 
Program.txt cpntains the "mini-programming-language" code. The scanner.py takes as input program.txt, that scan the code to get lexical analyze. The output: "Keywords", "Separators", "Operators", "Blackslash" "Comments". 

## Input(Example):   
int main() {  
    int isPrime = 9039  
// test program  
    for(int i=2; i <= math.sqrt(isPrime)+1; i++) {  
        if(isPrime%i == 0) {  
           print("Not prime:(")  
            return 0  
        }   
    }   

    print("Prime number!", "\n")  
    return 0  
}  

## Output(Example):   
Constantas:  
2  
1  
9039  
"Prime number!"  
0  
"Not prime:("  
None  

--------------------------------------------------------------------------------------------  
Identifiers:  
i  
isPrime  
None  
    
--------------------------------------------------------------------------------------------  
Keywords:  {'int': 3, 'main': 1, 'for': 1, 'if': 1, 'print': 2, 'return': 2}    
Separators:  {'(': 6, ')': 6, '{': 3, ';': 2, '}': 3, ',': 1}  
Operators:  {'=': 5, '<': 1, '+': 3, '%': 1}  
Blackslash:  ['"\\n"']  
Comments:  ['// test program']  
