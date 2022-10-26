#include <iostream>
#include <cmath>


using namespace std;

int main() {
    int isPrime = 9039;

    for(int i = 2; i <= sqrt(isPrime)+1; i++ ) {
        if(isPrime%i == 0) {
            cout << "Not prime:(";
            return 0;
        } 
    } 

    cout << "Prime number!";

    return 0;
}