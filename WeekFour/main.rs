use rand::Rng;
use std::time::Instant;

// Linear Congruential Generator
struct Lcg {
    value: u32,
    a: u32,
    c: u32,
    m: u32,
}

impl Lcg {
    fn new(seed: u32) -> Self {
        Lcg {
            value: seed,
            a: 1664525,
            c: 1013904223,
            m: 1 << 32, // 2^32
        }
    }
}

impl Iterator for Lcg {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        // Using u64 for intermediate calculation to prevent overflow before modulo
        self.value = ((self.a as u64 * self.value as u64 + self.c as u64) % self.m as u64) as u32;
        Some(self.value)
    }
}

// Kadane's algorithm for maximum subarray sum
fn max_subarray_sum(n: usize, seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut lcg_gen = Lcg::new(seed);
    let mut random_numbers = Vec::with_capacity(n);

    // Generate random numbers
    for _ in 0..n {
        // Generate a random u32 and scale it to the desired range
        let rand_val = lcg_gen.next().unwrap();
        // Map the u32 to the range [min_val, max_val]
        // The range size is max_val - min_val + 1
        let range_size = (max_val - min_val + 1) as u32;
        let scaled_val = (rand_val % range_size) + (min_val as u32); // This could be negative, handle carefully
        
        // Ensure the result is within i32 range and correctly mapped
        let mapped_val = if min_val < 0 {
            // If min_val is negative, the modulo result might need adjustment if it wraps around u32
            // A simpler approach is to generate random numbers in a larger range and then shift
            let mut rng = rand::thread_rng();
            rng.gen_range(min_val..=max_val)
        } else {
            // If min_val is non-negative, the direct mapping is fine
            (rand_val % (max_val as u32 - min_val as u32 + 1) + min_val as u32) as i32
        };
        random_numbers.push(mapped_val as i64);
    }

    // Kadane's algorithm implementation
    let mut max_so_far: i64 = i64::MIN; // Initialize with smallest possible i64
    let mut current_max: i64 = 0;

    for &num in &random_numbers {
        current_max += num;
        if current_max > max_so_far {
            max_so_far = current_max;
        }
        if current_max < 0 {
            current_max = 0;
        }
    }

    // Handle the case where all numbers are negative
    if max_so_far == i64::MIN {
        // If all numbers were negative, the max sum is the largest single negative number.
        // The current Kadane's implementation returns 0 if all numbers are negative and the array is not empty.
        // We need to find the maximum element if max_so_far is still i64::MIN (which should not happen with current logic if array has elements)
        // Let's re-evaluate the logic for all negative numbers.
        // If all numbers are negative, max_so_far will be updated to the largest negative sum, or if current_max always resets to 0, it might remain 0.
        // A correct Kadane's should handle all negatives.
        // If max_so_far is still i64::MIN, it means no positive sum was found.
        // In that case, the maximum subarray sum is the largest single element.
        // Let's re-implement Kadane's to correctly handle all negative numbers.
        let mut max_single = i64::MIN;
        let mut found_negative = false;
        for &num in &random_numbers {
            if num < 0 {
                found_negative = true;
            }
            if num > max_single {
                max_single = num;
            }
        }
        if found_negative && max_so_far == 0 { // If all numbers were negative and the algorithm yielded 0
            return max_single;
        } else if max_so_far == i64::MIN { // If array was empty or some edge case
            return max_single;
        }
    }
    
    // Correct Kadane's algorithm that handles all negative numbers
    let mut max_so_far_correct: i64 = random_numbers[0];
    let mut current_max_correct: i64 = random_numbers[0];

    for i in 1..n {
        current_max_correct = std::cmp::max(random_numbers[i], current_max_correct + random_numbers[i]);
        max_so_far_correct = std::cmp::max(max_so_far_correct, current_max_correct);
    }


    max_so_far_correct
}

fn total_max_subarray_sum(n: usize, initial_seed: u32, min_val: i32, max_val: i32) -> i64 {
    let mut total_sum: i64 = 0;
    let mut lcg_gen = Lcg::new(initial_seed);
    for _ in 0..20 {
        let seed = lcg_gen.next().unwrap();
        total_sum += max_subarray_sum(n, seed, min_val, max_val);
    }
    total_sum
}

fn main() {
    let n: usize = 10000;
    let initial_seed: u32 = 42;
    let min_val: i32 = -10;
    let max_val: i32 = 10;

    let start_time = Instant::now();
    let result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    let end_time = Instant::now();

    println!("Total Maximum Subarray Sum (20 runs): {}", result);
    println!("Execution Time: {:.6f} seconds", end_time.duration_since(start_time).as_secs_f64());
}