# Software Design and Engineering — Travlr Getaways

**Original course:** CS 465, Full Stack Development
**Enhanced for:** CS 499, Computer Science Capstone
**Repository:** [cs465-fullstack](https://github.com/Ssjbankai12/cs465-fullstack)

---

## Description of the Artifact

Travlr Getaways is a full-stack MEAN (MongoDB, Express, Angular, Node.js) travel booking application, originally developed for CS 465: Full Stack Development. It consists of three layers:

- A **server-rendered public site** built with Express and Handlebars
- A **RESTful API** backed by a MongoDB database
- An **Angular single-page administrative application** that lets staff manage trip listings behind JWT-based authentication and role-based navigation

The original submission also included a Software Design Document with UML class diagrams and API endpoint documentation.

## Justification for Inclusion

I selected Travlr Getaways for the Software Engineering and Design category because it best demonstrates my ability to design and build a complete, multi-layer application rather than an isolated script or algorithm. The specific components that showcase this most clearly are:

- The **authentication flow**
- The **role-based access control middleware** protecting the trip-management endpoints
- The **RESTful trip API**

Together these require coordinating the front end, back end, and database layers around a consistent security and data model.

### What I enhanced

- **Extracted business logic into a dedicated service layer.** Logic that previously lived directly in the Express route handlers now lives in:
  - `authService.js` — input validation, user registration, password hashing, and JWT issuance
  - `tripsService.js` — all trip CRUD operations against MongoDB

  Controllers were refactored to call these services and translate the results into HTTP responses, cleanly separating business logic from request handling.

- **Added automated testing.** An 11-test suite using **Mocha**, **Chai**, and **Sinon**, covering registration and login validation, JWT generation, and all four trip CRUD operations.

- **Added continuous integration.** A **GitHub Actions** workflow runs the full test suite automatically on every push and pull request to `main`.

## Course Outcomes Coverage

In the Module One enhancement plan, I identified this artifact as an opportunity to demonstrate Course Outcomes 2, 3, and 4. All three were met as planned, with no changes to the original coverage plan:

| Outcome | How it was addressed |
|---|---|
| **Outcome 2** | This narrative and the accompanying code comments document the design decisions behind the refactor for both technical and non-technical readers. |
| **Outcome 3** | Evaluated the original design, identified the coupling between business logic and route handling as a weakness, and redesigned the code around a service layer that separates those concerns. |
| **Outcome 4** | Introduced automated testing and continuous integration — tools not part of the original coursework requirements — to deliver a more maintainable, verifiable solution. |

## Reflection on the Enhancement Process

Working through this enhancement reinforced how much easier code is to test and reason about once business logic is separated from the framework code around it. Once the trip and authentication logic lived in plain service functions instead of inside Express route handlers, writing tests became straightforward — they no longer needed to simulate HTTP requests and responses just to exercise a validation rule or a database call.

The main technical challenge was mocking Mongoose correctly. My first attempt at stubbing the `save` method failed because I was stubbing the wrong object: Mongoose document instance methods live on the model's *prototype*, not on the model constructor itself. Once I understood that distinction, I stubbed `User.prototype.save` and `Model.prototype.save` instead, and the rest of the service-layer tests came together quickly.

I also chose **not** to unit test the login route directly, since it delegates authentication to Passport's middleware — better suited to integration testing than isolated unit testing. Instead, I focused test coverage on the parts of the authentication flow I could cleanly extract into the service layer: input validation and registration.

Overall, this enhancement gave me practical experience with a refactor pattern — separating concerns into a service layer — that I expect to reuse in future backend work.

- [Travlr Getaways – Full Stack MEAN Application (CS 465)](https://github.com/Ssjbankai12/cs465-fullstack)
