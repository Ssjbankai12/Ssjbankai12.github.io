# Ssjbankai12.github.io

# Kevin Korb — Computer Science ePortfolio

Welcome to my ePortfolio. I'm a Computer Science student at Southern New Hampshire University with a concentration in cybersecurity. This repository hosts my CS 499 Capstone ePortfolio, showcasing three artifacts I enhanced across the three core areas of computer science: **software design and engineering**, **algorithms and data structures**, and **databases**.

The live site ([ssjbankai12.github.io](https://ssjbankai12.github.io)) leads with my full **Professional Self-Assessment**, followed by the enhancement narrative for each artifact below. This README gives a technical overview of the projects themselves.

---

## Projects

### Travlr Getaways — Full-Stack MEAN Application (CS 465)

**Repository:** [cs465-fullstack](https://github.com/Ssjbankai12/cs465-fullstack) · **Category:** Software Design and Engineering · **Full narrative:** [travlr-getaways.md](travlr-getaways.md)

A full-stack travel booking platform originally built for CS 465: Full Stack Development, using the MEAN stack — **MongoDB, Express, Angular, and Node.js**. The application is split into a server-rendered public site (Express + Handlebars) and an Angular single-page admin application that lets staff manage trip listings behind **JWT-based authentication** and **role-based access control**.

For my CS 499 enhancement, I refactored the business logic that originally lived directly inside the Express route handlers into a dedicated service layer — `authService.js` for registration, password hashing, and JWT issuance, and `tripsService.js` for all trip CRUD operations — so controllers now simply call these services and translate the results into HTTP responses. I backed this with an 11-test **Mocha/Chai/Sinon** suite covering authentication and all four trip CRUD operations, and wired a **GitHub Actions** workflow so the full suite runs automatically on every push and pull request to `main`.

**Tech stack:** MongoDB · Express.js · Angular · Node.js · Mongoose · Passport.js · JWT · Bootstrap · Handlebars · Mocha/Chai/Sinon · GitHub Actions

---

### Rescue-Dog Dashboard — Client-Server Development (CS 340)

**Repository:** [CS-340-Client-Server-Development](https://github.com/Ssjbankai12/CS-340-Client-Server-Development) · **Category:** Databases · **Full narrative:** [rescue-dog-dashboard.md](rescue-dog-dashboard.md)

An interactive dashboard built for CS 340: Client-Server Development, connecting a Python CRUD module (`CRUD_Python_Module.py`) to a **MongoDB** database of Austin Animal Center shelter outcome records. A **Dash** front end lets users filter animals by rescue type (water rescue, mountain/wilderness rescue, disaster and individual tracking), browse results in a sortable table, view a breed-distribution pie chart, and see a selected animal's location on a map.

My CS 499 enhancement focused entirely on the database layer, inside the `AnimalShelter` class. I added `create_indexes()`, a compound index on `breed`, `sex_upon_outcome`, and `age_upon_outcome_in_weeks` matching the fields every filter query already uses, so MongoDB can locate matches directly instead of scanning the full collection. I added `get_breed_outcome_stats()`, an aggregation pipeline that computes adoption rate, average age, and count per breed, surfaced as a new bar-chart panel on the dashboard. Finally, I added `apply_schema_validation()`, a MongoDB `$jsonSchema` validator that rejects malformed or incomplete records at the database level rather than relying on application-side assumptions. I validated the indexing and aggregation logic with an automated test suite against **mongomock** (an in-memory MongoDB emulator), since a live MongoDB instance wasn't available during development.

**Tech stack:** Python · MongoDB · PyMongo · Dash · Plotly · Dash Leaflet · Jupyter · mongomock

---

### Secure Coding Encryption Project (CS 405)

**Repository:** [CS_405_Secure_Coding](https://github.com/Ssjbankai12/CS_405_Secure_Coding) · **Category:** Algorithms and Data Structures · **Full narrative:** [encryption-keystore.md](encryption-keystore.md)

A C++ encryption/decryption program originally built for CS 405: Secure Coding, applying a repeating-key XOR transformation to encrypt and decrypt a text file and confirm the round trip. The original version relied on a single hardcoded key with no key management logic at all.

My CS 499 enhancement introduced a `KeyStore` interface with two implementations: a `LinearKeyStore` (vector-backed, O(n) lookup) and a `HashKeyStore` (unordered_map-backed, average O(1) lookup), with the hash-based version wired into the working program. To justify that choice with evidence rather than intuition, I built a standalone benchmark harness that timed lookups against both stores at key-set sizes from 100 to 100,000 — the hash map was 3.5x faster at 100 keys and 566x faster at 100,000, confirming the expected O(n) vs. O(1) trade-off. The project also includes a **CppCheck** static analysis review and an accompanying **DevSecOps security policy document** covering coding standards, risk assessment, and encryption policy.

**Tech stack:** C++ · CppCheck · custom benchmarking harness

---

## Emerging Technology Focus

As part of the capstone, I researched two disruptive technologies most relevant to where I want to take my career — the intersection of software development and security:

- **Generative AI** — its growing role in software development workflows and the new categories of risk it introduces to secure coding practices.
- **Quantum computing and post-quantum cryptography** — the eventual threat quantum computing poses to current encryption standards, and the cryptographic approaches being developed to stay ahead of it.

Both topics connect directly to the security mindset behind all three artifacts in this portfolio, particularly the key-management work in the encryption project above.

---

## Running the Projects Locally

Each linked repository contains its own source code. `node_modules` is excluded from the Travlr Getaways repo (standard practice — it's regenerated from `package.json`), so after cloning:

```bash
npm install        # from the project root
cd app_admin && npm install   # for the Angular admin app
```

---

## Contact

Kevin Korb
Southern New Hampshire University — B.S. Computer Science, Cybersecurity Concentration
