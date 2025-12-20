#include <iostream>
#include <iomanip>
#include <chrono>

static inline double calculate(int iterations, int param1, int param2) {
    double result = 1.0;
    const double p1 = static_cast<double>(param1);
    const double p2 = static_cast<double>(param2);
    double base = p1; // corresponds to i*param1 for i=1

    int i = 1;
    const int n = iterations;

    // Manual unrolling by 8 to reduce loop overhead and help hide divide latency,
    // while strictly preserving the sequential update order for identical rounding.
    for (; i <= n - 7; i += 8) {
        double b = base;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);
        b += p1;

        result -= 1.0 / (b - p2);
        result += 1.0 / (b + p2);

        base += p1 * 8.0;
    }

    for (; i <= n; ++i) {
        result -= 1.0 / (base - p2);
        result += 1.0 / (base + p2);
        base += p1;
    }

    return result;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    auto start_time = std::chrono::steady_clock::now();
    double result = calculate(200000000, 4, 1) * 4.0;
    auto end_time = std::chrono::steady_clock::now();

    double elapsed = std::chrono::duration<double>(end_time - start_time).count();

    std::cout.setf(std::ios::fixed);
    std::cout << "Result: " << std::setprecision(12) << result << '\n';
    std::cout << "Execution Time: " << std::setprecision(6) << elapsed << " seconds\n";
    return 0;
} 