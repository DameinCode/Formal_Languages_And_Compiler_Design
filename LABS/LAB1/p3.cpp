#include <iostream>
#include <cmath> 

// 2nd order equation
using namespace std;

int main() {
    // ax^2 + bx + c = 0
    int a = 1, b = -2, c = -24;
    float D = b*b - 4*a*c; 
    cout << "First: " << (((-1)*b + sqrt(D))/2*a) << "\n";
    cout << "Second: " <<  (((-1)*b - sqrt(D))/2*a) << "\n";
    return 0;
}