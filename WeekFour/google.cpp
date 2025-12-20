
#include <iostream>
#include <vector>
#include <chrono>
#include <iomanip>

double calculate(int iterations, double param1, double param2) {
    double result = 1.0;
    // Using const for loop variables and loop-invariant calculations
    const double p1 = param1;
    const double p2 = param2;

    for (int i = 1; i <= iterations; ++i) {
        // Directly calculate j to reduce temporary variable usage
        double j1 = static_cast<double>(i) * p1 - p2;
        result -= (1.0 / j1);
        
        double j2 = static_cast<double>(i) * p1 + p2;
        result += (1.0 / j2);
    }
    return result;
}

int main() {
    // Use std::chrono for high-resolution timing
    auto start_time = std::chrono::high_resolution_clock::now();

    // Use double for all calculations to match Python's behavior with floats
    double result = calculate(200000000, 4.0, 1.0) * 4.0;

    auto end_time = std::chrono::high_resolution_clock::now();

    // Use std::fixed and std::setprecision for precise output formatting
    std::cout << std::fixed << std::setprecision(12) << "Result: " << result << std::endl;

    std::chrono::duration<double> elapsed = end_time - start_time;
    std::cout << std::fixed << std::setprecision(6) << "Execution Time: " << elapsed.count() << " seconds" << std::endl;

    return 0;
}
