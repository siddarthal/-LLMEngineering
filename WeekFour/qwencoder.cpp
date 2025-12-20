
#include <iostream>

double calculate(int iterations, int param1, int param2) {
    double result = 0.0;
    for (int i = 1; i <= iterations; ++i) {
        int j = i * param1 - param2;
        result -= 1.0 / j;
        j = i * param1 + param2;
        result += 1.0 / j;
    }
    return result;
}

int main() {
    const int iterations = 200'000'000;
    const int param1 = 4;
    const int param2 = 1;

    auto start = std::chrono::high_resolution_clock::now();
    double result = calculate(iterations, param1, param2) * 4;
    auto end = std::chrono::high_resolution_clock::now();

    std::cout << "Result: " << result << std::endl;
    std::cout << "Execution Time: " << std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1'000'000.0 << " microseconds" << std::endl;

    return 0;
}
