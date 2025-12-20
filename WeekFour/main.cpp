


#include <iostream>
#include <cmath>
#include <vector>

using namespace std;

double calculate(int iterations, int param1, int param2) {;
    double result = 0.0;

    for (int i=1; i<=iterations ;i++) {
        int j = i * param1 - param2;
        result -= (1 / j);
        j = i * param1 + param2;
        result += (1 / j);
    }
    return result;
}

int main () {
	long long start_time;
	long long end_time;
	start_time = time(0);
	double result = calculate(200_000_000, 4, 1) * 4;
	end_time = time(0);

	cout << "Result: " << fixed << setprecision(12) << result << endl;
	cout << "Execution Time: " << fixed << setprecision(6) << (end_time - start_time) / 1e3;
}

