// Benchmark.cpp
// Standalone utility that generates a large synthetic set of keys and
// times lookups against the LinearKeyStore vs. the HashKeyStore to
// demonstrate the real-world performance difference between the two
// approaches as the number of stored keys grows.
//
// A fixed number of lookups is sampled per key-count size (rather than
// looking up every stored key) so the linear-scan case stays runnable
// even at large sizes; the per-lookup cost still grows with store size
// for the linear store, which is exactly the trend being measured.
//
// Build:  g++ -O2 -std=c++17 Benchmark.cpp -o benchmark
// Run:    ./benchmark

#include "KeyStore.h"
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>

// Generates `count` unique synthetic key IDs
std::vector<std::string> generateKeyIds(size_t count)
{
    std::vector<std::string> ids;
    ids.reserve(count);
    for (size_t i = 0; i < count; ++i)
    {
        ids.push_back("key-" + std::to_string(i));
    }
    return ids;
}

// Picks `sampleCount` random ids out of the full population to look up.
// Sampling keeps the benchmark runnable at large store sizes, since
// looking up every key would make the linear-scan case scale as O(n^2).
std::vector<std::string> sampleLookupIds(const std::vector<std::string>& ids, size_t sampleCount, std::mt19937& rng)
{
    std::uniform_int_distribution<size_t> dist(0, ids.size() - 1);
    std::vector<std::string> sample;
    sample.reserve(sampleCount);
    for (size_t i = 0; i < sampleCount; ++i)
    {
        sample.push_back(ids[dist(rng)]);
    }
    return sample;
}

// Times looking up every id in `lookupIds` using the provided store,
// returning elapsed time in milliseconds.
double timeLookups(const KeyStore& store, const std::vector<std::string>& lookupIds)
{
    auto start = std::chrono::high_resolution_clock::now();

    volatile size_t foundCount = 0; // volatile so the compiler cannot optimize the loop away
    for (const auto& id : lookupIds)
    {
        std::string value;
        if (store.findKey(id, value))
        {
            ++foundCount;
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(end - start).count();
}

int main()
{
    std::vector<size_t> sizes = { 100, 1000, 10000, 50000, 100000 };
    const size_t sampleCount = 2000; // number of lookups timed per size

    std::mt19937 rng(42); // fixed seed for reproducible results

    std::cout << std::left
        << std::setw(12) << "Key Count"
        << std::setw(18) << "Linear (ms)"
        << std::setw(18) << "Hash Map (ms)"
        << "Speedup" << std::endl;
    std::cout << std::string(60, '-') << std::endl;

    for (size_t size : sizes)
    {
        LinearKeyStore linear;
        HashKeyStore hashed;

        auto ids = generateKeyIds(size);
        for (const auto& id : ids)
        {
            linear.addKey(id, "value-" + id);
            hashed.addKey(id, "value-" + id);
        }

        auto lookupIds = sampleLookupIds(ids, sampleCount, rng);

        double linearMs = timeLookups(linear, lookupIds);
        double hashMs = timeLookups(hashed, lookupIds);
        double speedup = linearMs / hashMs;

        std::cout << std::left
            << std::setw(12) << size
            << std::setw(18) << std::fixed << std::setprecision(3) << linearMs
            << std::setw(18) << std::fixed << std::setprecision(3) << hashMs
            << std::fixed << std::setprecision(1) << speedup << "x"
            << std::endl;
    }

    std::cout << "\n(" << sampleCount << " randomly sampled lookups timed per key-count size)" << std::endl;

    return 0;
}
