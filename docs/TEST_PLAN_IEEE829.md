# Master Test Plan (IEEE 829-2008 Standard)
## Project: TestFlow – Software Test Management System

---

### 1. Test Plan Identifier
`MTP-TF-2026-V1.0`

### 2. References
- ISTQB Certified Tester Foundation Level Syllabus (v4.0)
- IEEE Standard for Software and System Test Documentation (IEEE Std 829-2008)
- TestFlow Functional Requirements Specification (`REQ-AUTH-01` through `REQ-ORD-05`)

### 3. Introduction & Objectives
The primary purpose of this test plan is to establish a rigorous, repeatable software testing framework for TestFlow. The project demonstrates full STLC execution:
- Requirements Analysis and Test Basis derivation
- Test Design via formal specification-based techniques (EP, BVA, Decision Tables, State Transitions)
- Test Execution tracking with actual vs. expected results
- Incident/Defect tracking through standardized state transitions
- Exit Criteria assessment for release sign-off

### 4. Test Items (Software Under Test)
1. **Authentication & Session Manager (`REQ-AUTH-01`)**
2. **Shopping Cart Item Limit & Validation Engine (`REQ-CART-02`)**
3. **Discount Voucher Engine (`REQ-DISC-03`)**
4. **Payment Gateway Integration Interface (`REQ-PAY-04`)**
5. **Order Lifecycle & Inventory Management (`REQ-ORD-05`)**
6. **Defect Lifecycle State Transition Engine**
7. **Requirements Traceability Matrix (RTM) Aggregator**

### 5. Features to be Tested & Features Not to be Tested
- **In Scope:**
  - Functional testing of cart quantity boundaries [1, 99].
  - Boundary value testing on coupon codes and order thresholds ($100).
  - Decision table evaluation for defect triage SLA prioritization.
  - State machine enforcement for defect transitions.
  - API endpoints for test runs, execution recording, and metrics.
  - SQL injection and XSS input sanitization.
- **Out of Scope:**
  - Multi-datacenter database replication (single SQLite/PostgreSQL instance assumed).
  - External credit card payment processing (mock gateway sandbox utilized).

### 6. Approach & Testing Strategies
- **Component / Unit Testing:** Pytest unit tests for domain services and input validators (`tests/unit/`).
- **Specification-Based Testing:**
  - Equivalence Partitioning (`tests/istqb/test_equivalence_partitioning.py`)
  - Boundary Value Analysis (`tests/istqb/test_boundary_value_analysis.py`)
  - Decision Table Testing (`tests/istqb/test_decision_table.py`)
  - State Transition Testing (`tests/istqb/test_state_transition.py`)
- **Experience-Based Testing:** Error Guessing (`tests/istqb/test_error_guessing.py`).
- **Risk-Based Testing:** RPN prioritization ($Likelihood \times Impact$).
- **Regression Testing:** Automated end-to-end regression cycle (`tests/regression/test_regression_suite.py`).
- **API Automation:** Integration test suite (`tests/api/test_api_endpoints.py`).

### 7. Item Pass/Fail Criteria
- **Individual Test Case Pass:** Actual result strictly matches expected result with no unhandled exceptions.
- **Test Run Pass Criteria:**
  - 100% of Critical and High priority tests executed.
  - Overall pass rate $\ge 90.0\%$.
  - Zero open Blocker or Critical defects.

### 8. Suspension and Resumption Criteria
- **Suspension:** A Blocker defect in payment or authentication preventing more than 30% of scheduled tests from executing.
- **Resumption:** Deployment of a verified fix to the QA environment and successful execution of the Smoke test suite.

### 9. Test Deliverables
1. Master Test Plan (this document)
2. Requirements Traceability Matrix (`/rtm`)
3. Automated Test Suite (90+ Pytest automated tests)
4. Defect Incident Reports (`/defects`)
5. IEEE 829 Test Summary Report (`/report/<run_id>`)

### 10. Environmental Needs
- Python 3.10+ runtime environment
- Flask application server running on `http://127.0.0.1:5000`
- SQLite / PostgreSQL relational database
- Headless Google Chrome / Microsoft Edge for UI automated testing

### 11. Approvals
- **Lead QA Engineers:** Eya Khandoudi & Ichraf Sassi (Approved)
- **Lead Software Architect:** Approved
- **Product Owner:** Approved
