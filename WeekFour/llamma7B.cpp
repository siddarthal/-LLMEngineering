Here's a possible implementation of the `calculate` function in C++ with as few changes as possible to achieve a similar performance to the original Python code:
c++
#include <iostream>
#include <chrono>

double calculate(int iterations, double param1, double param2) {
    double result = 1.0;
    for (int i = 1; i <= iterations + 1; ++i) {
        const double j = i * param1 - param2;
        result -= 1 / j;
        result += 1 / (i * param1 + param2);
    }
    return result;
}

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();
    double result = calculate(200'000'000, 4, 1) * 4;
    auto end_time = std::chrono::high_resolution_clock::now();

    std::cout << "Result: " << std::fixed << std::setprecision(12) << result << std::endl;
    std::cout << "Execution Time: " << std::chrono::duration<double>(end_time - start_time).count() << " seconds" << std::endl;

    return 0;
}
