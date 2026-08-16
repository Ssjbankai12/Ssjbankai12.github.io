#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <utility>

// Common interface so the linear and hash-map implementations
// can be swapped in and benchmarked against each other.
class KeyStore
{
public:
    virtual ~KeyStore() = default;
    virtual void addKey(const std::string& keyId, const std::string& keyValue) = 0;
    virtual bool findKey(const std::string& keyId, std::string& outValue) const = 0;
};

// Original-style approach: keys stored in an unsorted vector.
// Lookup requires scanning every entry until a match is found - O(n).
class LinearKeyStore : public KeyStore
{
public:
    void addKey(const std::string& keyId, const std::string& keyValue) override
    {
        entries.emplace_back(keyId, keyValue);
    }

    bool findKey(const std::string& keyId, std::string& outValue) const override
    {
        for (const auto& entry : entries)
        {
            if (entry.first == keyId)
            {
                outValue = entry.second;
                return true;
            }
        }
        return false;
    }

private:
    std::vector<std::pair<std::string, std::string>> entries;
};

// Enhanced approach: keys stored in a hash map.
// Lookup is average-case O(1) regardless of how many keys are stored.
class HashKeyStore : public KeyStore
{
public:
    void addKey(const std::string& keyId, const std::string& keyValue) override
    {
        entries[keyId] = keyValue;
    }

    bool findKey(const std::string& keyId, std::string& outValue) const override
    {
        auto it = entries.find(keyId);
        if (it != entries.end())
        {
            outValue = it->second;
            return true;
        }
        return false;
    }

private:
    std::unordered_map<std::string, std::string> entries;
};
