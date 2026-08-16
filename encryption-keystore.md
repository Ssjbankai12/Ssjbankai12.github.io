# Algorithms and Data Structures — Encryption/Decryption KeyStore

**Original course:** CS 405, Secure Coding
**Enhanced for:** CS 499, Computer Science Capstone
**Repository:** [CS_450_Secure_Coding](https://github.com/Ssjbankai12/CS_450_Secure_Coding)

---

## Description of the Artifact

This artifact is an encryption and decryption program written in C++, originally developed for CS 405: Secure Coding. The program reads a text file, applies a repeating-key XOR transformation to encrypt it, writes the encrypted output to disk, then decrypts it back and writes a second file to confirm the round trip. The original version used a single hardcoded key string for this transformation.

## Justification for Inclusion

I selected this artifact for the Algorithms and Data Structures category because the original design offered a genuine opportunity to introduce and evaluate a data structure trade-off, rather than simply cleaning up existing code. The original program had no key management logic at all — just one fixed, hardcoded key. My enhancement added that capability and produced a concrete before-and-after comparison between two classic approaches to key lookup.

### What I built

I designed a **`KeyStore`** interface with two implementations:

- **`LinearKeyStore`** — stores keys in a `vector`; finds a requested key by scanning entries one at a time (**O(n)**)
- **`HashKeyStore`** — stores keys in an `unordered_map`; finds a requested key in average-case **O(1)** time regardless of how many keys are stored

The main program was updated to build a `HashKeyStore` holding several named keys and look up the active key by name, rather than relying on a hardcoded string. Choosing an appropriate data structure for a lookup-heavy operation, and justifying that choice with evidence rather than intuition, is the specific skill this component demonstrates.

### Benchmarking the trade-off

To generate that evidence, I built a standalone benchmark utility that populates both key stores with synthetic key sets of increasing size (100, 1,000, 10,000, 50,000, and 100,000 keys) and times a fixed number of randomly sampled lookups against each. The results confirmed the expected O(n) vs. O(1) behavior:

- At **100 keys**, the hash map was already **3.5x faster** than the linear scan
- At **100,000 keys**, the hash map was **566x faster**
- The hash map's lookup time barely changed across all five sizes, while the linear store's lookup time grew in direct proportion to the number of stored keys

## Course Outcomes Coverage

In the Module One enhancement plan, I identified this enhancement as an opportunity to demonstrate Course Outcomes 3, 4, and 5. I met all three:

| Outcome | How it was addressed |
|---|---|
| **Outcome 3** | Evaluated the original artifact's lack of any key management structure, designed a `KeyStore` abstraction, and implemented and compared two different data structure approaches to the same lookup problem. |
| **Outcome 4** | Built a working benchmark harness — an addition beyond the original coursework requirements — that produces concrete, reproducible performance measurements rather than a purely theoretical claim. |
| **Outcome 5** | Replaced a single key hardcoded in source with multiple named keys managed through a dedicated component, a more security-conscious foundation to build on. |

> **Note on the plan revision:** My Module One plan assumed the original program already managed a list of keys and that the enhancement would replace a linear search with a hash map. When I returned to the actual source for this milestone, I found the original used only a single hardcoded key with no key list or lookup logic at all. I adjusted accordingly — introducing key management as a new capability, implementing it with both a linear and a hash-based approach, and using the benchmark to justify the hash-based version as the one integrated into the working program. This preserves the original intent (evaluating a data structure trade-off for key lookup) while accurately reflecting the artifact as it existed.

## Reflection on the Enhancement Process

This enhancement gave me hands-on experience designing a small abstraction — the `KeyStore` interface — specifically so two different implementations could be compared fairly under identical conditions. Writing the `LinearKeyStore` alongside the `HashKeyStore`, rather than only writing the improved version, turned out to be valuable, since it forced me to think carefully about what a fair comparison requires.

The main technical challenge was designing a benchmark that would actually finish running. My first version timed a lookup for *every* key in the store, which meant the linear-scan benchmark scaled as O(n²) once key counts reached the tens of thousands — the run didn't complete in a reasonable amount of time. I resolved this by sampling a fixed number of lookups per key-count size instead of scaling the number of lookups with the size of the store. This kept the benchmark fast at every size while still measuring exactly the trend I needed: how the average cost of a single lookup changes as the underlying data structure grows.

I also had to replace a Windows-specific function call, `localtime_s`, with a portable alternative so the program would compile and run outside of Visual Studio — a useful reminder that platform-specific APIs can quietly limit where code can be tested and verified.

Overall, this milestone reinforced that a data structure choice is only as convincing as the evidence behind it. Producing the actual timing numbers, rather than simply asserting that a hash map would be faster, made the enhancement feel like a real engineering decision rather than a textbook exercise.

- [Secure Coding Encryption Project (CS 405)](https://github.com/Ssjbankai12/CS_450_Secure_Coding)
