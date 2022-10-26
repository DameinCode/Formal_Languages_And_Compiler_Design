#include <iostream>
#include <cmath>

// find the gcd of 2 numbers

using namespace std; 

int main() {
    int num1 = 10, num2 = 90, res = 1;
    
    if (num1 > num2) {
        for(int i = 2; i <= sqrt(num1)+1; i++) {
            if(num1%i == 0 && num2%i == 0) {
                res = i;
            }
        }
    } else {
        for(int i = 2; i <= sqrt(num2)+1; i++) {
            if(num1%i == 0 && num2%i == 0) {
                res = i;
            }
        }
    }
    cout << res;

    return 0;
}