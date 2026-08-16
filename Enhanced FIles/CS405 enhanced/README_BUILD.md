# Building and Running

## Main program (encryption/decryption)
    g++ -O2 -std=c++17 Encryption.cpp -o encryption_app
    ./encryption_app

Reads inputdatafile.txt, encrypts it using the "default" key from the
HashKeyStore, writes encrypteddatafile.txt, decrypts it, and writes
decrytpteddatafile.txt.

## Benchmark (LinearKeyStore vs. HashKeyStore)
    g++ -O2 -std=c++17 Benchmark.cpp -o benchmark
    ./benchmark

Generates synthetic key sets of increasing size, times a fixed number
of sampled lookups against both key store implementations, and prints
a comparison table with the measured speedup.
