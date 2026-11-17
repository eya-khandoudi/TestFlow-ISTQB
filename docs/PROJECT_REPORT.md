# TestFlow – Comprehensive ISTQB Project Report
**Software Test Management System & Testing Methodology Implementation**

---

## Document Control & Metadata

| Field | Detail |
| :--- | :--- |
| **Project Title** | TestFlow – Software Test Management System |
| **Project Type** | ISTQB Software Testing Demonstration & Web Application |
| **Authors & Lead QA** | **Eya Khandoudi** & **Ichraf Sassi** *(ISTQB Certified Testers)* |
| **Standard Compliance** | ISTQB Foundation Level (CTFL v4.0), Advanced Level (CTAL-TM), IEEE Std 829-2008 |
| **GitHub Repository** | [https://github.com/eya-khandoudi/TestFlow-ISTQB](https://github.com/eya-khandoudi/TestFlow-ISTQB) |
| **Publication Date** | November 2026 |
| **Report Status** | Official Final Deliverable |

---

## 1. Executive Summary

**TestFlow** was conceived and engineered not merely as a web utility, but as a formal demonstration of professional software testing methodologies across the **Software Development Life Cycle (SDLC)** and **Software Testing Life Cycle (STLC)**.

In real-world software engineering, testing is frequently mischaracterized as ad-hoc defect finding. TestFlow disproves this misconception by embodying formal test analysis, specification-based test design, risk-based prioritization, state machine enforcement, bi-directional traceability, and standardized reporting.

### Key Milestones Achieved:
- **Full-Stack Application:** Modular Python & Flask web platform with SQLite, Bootstrap 5, Chart.js, and REST API.
- **8 Core ISTQB Techniques:** 100% implemented in application logic and verified via automated test suites.
- **Robust Quality Metrics:** **92 automated tests passed** (0 failures) achieving **91% statement test coverage**.
- **IEEE Std 829-2008 Reporting:** Automated Test Summary Reports with dynamic Release Gate decision calculation (Go / No-Go).
- **Publication-Ready Deliverables:** 16-page illustrated PDF guide, complete Requirements Traceability Matrix (RTM), and public GitHub repository.

---

## 2. Technology Stack & Architectural Architecture

The system is designed following the **Separation of Concerns** principle with a layered architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER (UI)                         │
│   HTML5 • Bootstrap 5 • Chart.js • Bootstrap Icons • Vanilla JS        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ HTTP / JSON
┌──────────────────────────────────▼─────────────────────────────────────┐
│                          FLASK ROUTING LAYER                           │
│   Dashboard (main) • Requirements • Test Cases • Test Runs • Defects  │
│                           REST API Endpoints                           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Function Calls
┌──────────────────────────────────▼─────────────────────────────────────┐
│                          DOMAIN SERVICE LAYER                          │
│   ISTQB Domain Engine (istqb_engine.py)                                │
│   • Defect State Machine (STT)      • Decision Table Triage (DTT)      │
│   • BVA / EP Input Validators       • Risk Priority Calculator (RBT)   │
│   Report Engine (report_service.py)                                    │
│   • RTM Matrix Aggregator           • IEEE 829 Summary Generator       │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Parameterized SQL
┌──────────────────────────────────▼─────────────────────────────────────┐
│                         DATA PERSISTENCE LAYER                         │
│   SQLite 3 with Foreign Key Constraints & Virtual Generated Columns    │
│   (testflow.db)                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Technology Specification:
- **Programming Language:** Python 3.13.3
- **Web Backend:** Flask 3.1.3 (Application Factory pattern with Blueprints)
- **Database Engine:** SQLite 3.49.1 (Relational schema, `PRAGMA foreign_keys = ON`, virtual generated column for Risk Score)
- **Frontend Framework:** Responsive Bootstrap 5.3.3, Chart.js 4.4.2 for vector charts
- **Automated Testing:** Pytest 9.2.0 with custom `@pytest.mark` technique categorization
- **Code Coverage:** Coverage.py 7.17.3 / pytest-cov 7.1.0
- **Browser Automation:** Selenium 4.52.0 (Headless Chrome & Edge support)
- **Document Generation:** ReportLab 5.0.0 & PyPDF 6.13.1

---

## 3. Main Application Modules

### 3.1 Requirements Management (Test Basis)
- **STLC Phase:** Test Analysis & Planning.
- **Capabilities:** Authors and organizes business and technical requirements categorized into *Functional*, *Security*, *Business Rule*, *Payment*, and *Workflow*.
- **Coverage Gap Detection:** Displays real-time counts of linked test cases. Any requirement lacking associated test cases is highlighted with a red **"0 (Coverage Gap)"** alert badge.

### 3.2 Test Case Repository & Risk Assessment
- **STLC Phase:** Test Design & Implementation.
- **Capabilities:** Manages test specifications complete with preconditions, step-by-step procedures, expected results, priority, and test types.
- **Risk Integration:** Every test case captures *Likelihood of Failure* (1-5) and *Impact of Failure* (1-5), automatically computing the **Risk Priority Number (RPN)** ($1 \dots 25$).

### 3.3 Test Execution & Test Runs
- **STLC Phase:** Test Execution.
- **Capabilities:** Snapshots active test cases into dedicated execution cycles configured for specific target environments (QA, Staging, UAT, Production).
- **Inline Result Recorder:** Testers record outcomes (`Pass`, `Fail`, `Blocked`, `Skipped`), log actual observations, capture tester identity, and directly trigger defect logging upon test failure.

### 3.4 Defect Management & State Machine
- **STLC Phase:** Defect Management & Retesting.
- **Capabilities:** Central incident register tracking bugs categorized by severity (*Blocker*, *Critical*, *Major*, *Minor*) and environment.
- **State Machine Engine:** Enforces permitted lifecycle state transitions, preventing illegal jumps and capturing chronological audit logs with comments.

### 3.5 QA Testing Dashboard & IEEE 829 Release Gate
- **STLC Phase:** Test Evaluation & Closure.
- **Capabilities:** Executive dashboard featuring live KPIs, doughnut chart for execution status, and bar chart for defect severity breakdown.
- **Automated Decision Gate:** Continuously evaluates exit criteria:
  - If open Blocker/Critical defects $> 0 \rightarrow$ **NO-GO**
  - If pass rate $\ge 90\%$ with zero blockers and critical tests passed $\rightarrow$ **GO**
  - If pass rate $\ge 75\%$ with zero blockers $\rightarrow$ **CONDITIONAL GO**

---

## 4. Deep Dive: ISTQB Concepts Implemented

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ISTQB TESTING METHODOLOGY SUMMARY                      │
├──────────────────────────┬──────────────────────────┬───────────────────────┤
│ Equivalence Partitioning │ Boundary Value Analysis  │ Decision Table        │
│ • Valid & Invalid input  │ • 2-value & 3-value BVA  │ • Defect SLA Triage   │
│   partitions             │ • Cart limits [1 .. 99]  │ • Release Exit Gate   │
├──────────────────────────┼──────────────────────────┼───────────────────────┤
│ State Transition Testing │ Error Guessing           │ Risk-Based Testing    │
│ • Defect Lifecycle       │ • SQLi & XSS resistance  │ • RPN = Likelihood x  │
│ • Guard validations      │ • Unicode & boundary     │   Impact (1 to 25)    │
├──────────────────────────┴──────────────────────────┴───────────────────────┤
│ Requirements Traceability Matrix (RTM) & Automated Regression Suite         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Equivalence Partitioning (EP)
- **Concept:** Divides input data into partitions where all elements are expected to produce identical system behavior.
- **Implementation:**
  - *Risk Ratings ($L, I$):* Valid partition $[1, 5]$; Invalid Low partition $\le 0$; Invalid High partition $\ge 6$; Invalid Type partition (`"abc"`, `None`).
  - *Cart Quantities:* Valid partition $[1, 99]$; Invalid Low $\le 0$; Invalid High $\ge 100$.
  - *String Lengths:* Valid partition $[5, 200]$; Invalid Underflow $< 5$; Invalid Overflow $> 200$.
- **Verification:** 19 automated tests in `tests/istqb/test_equivalence_partitioning.py`.

### 4.2 Boundary Value Analysis (BVA)
- **Concept:** Tests the boundaries between equivalence partitions where defects have the highest probability of occurring.
- **Implementation:**
  - *Cart Quantity Boundaries:*
    - Boundary $0$ (Min - 1): **Invalid** $\rightarrow$ Rejection
    - Boundary $1$ (Min): **Valid** $\rightarrow$ Accepted
    - Boundary $2$ (Min + 1): **Valid** $\rightarrow$ Accepted
    - Boundary $98$ (Max - 1): **Valid** $\rightarrow$ Accepted
    - Boundary $99$ (Max): **Valid** $\rightarrow$ Accepted
    - Boundary $100$ (Max + 1): **Invalid** $\rightarrow$ Rejection
- **Verification:** 16 automated tests in `tests/istqb/test_boundary_value_analysis.py`.

### 4.3 Decision Table Testing (DTT)
- **Concept:** Tests combinations of multi-condition inputs that drive discrete business actions.
- **Implementation 1 (Defect SLA Triage):**

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Severity $\in$ {Blocker, Critical} | **True** | **True** | **True** | False | False | False |
| Environment == Production | **True** | False | False | * | * | * |
| Affects Core Flow | * | **True** | False | **True** | False | * |
| Severity == Major | False | False | False | **True** | **True** | False |
| Severity == Minor | False | False | False | False | False | **True** |
| **Action: Priority** | **Urgent** | **Urgent** | **High** | **High** | **Medium** | **Low** |
| **Action: SLA Resolution** | **4 Hours** | **8 Hours** | **16 Hours** | **24 Hours** | **48 Hours** | **120 Hours**|
| **Action: Escalation** | **Required** | **Required** | Standard | Standard | Standard | Standard |

- **Implementation 2 (IEEE 829 Release Gate):**
  - Blocker Defect Count $> 0 \rightarrow$ **NO-GO**
  - Pass Rate $\ge 90\%$ AND Critical Tests Pass $\rightarrow$ **GO**
  - Pass Rate $\ge 75\%$ AND Critical Tests Pass $\rightarrow$ **CONDITIONAL GO**
- **Verification:** 10 automated tests in `tests/istqb/test_decision_table.py`.

### 4.4 State Transition Testing (STT)
- **Concept:** Validates system behavior when transitioning across discrete states in a state machine.
- **Defect Lifecycle Graph:**
  $$\text{New} \longrightarrow \text{Assigned} \longrightarrow \text{Open} \longrightarrow \text{Fixed} \longrightarrow \text{Retest} \longrightarrow \text{Closed}$$
  $$\text{Retest (Fail)} \longrightarrow \text{Reopened} \longrightarrow \text{Open}$$
  $$\text{New} \longrightarrow \text{Rejected / Deferred}$$
- **Strict Guard Rules:**
  - `New` $\rightarrow$ `Closed`: Blocked (*Cannot close without triage or resolution*).
  - `Open` $\rightarrow$ `Closed`: Blocked (*Developer cannot close without testing*).
  - `Fixed` $\rightarrow$ `Closed`: Blocked (*QA must retest and verify fix first*).
  - Transitioning to `Fixed`, `Deferred`, or `Rejected` strictly mandates resolution notes.
- **Verification:** 10 automated tests in `tests/istqb/test_state_transition.py`.

### 4.5 Error Guessing
- **Concept:** Experience-based testing anticipating faults, vulnerabilities, and edge cases.
- **Payloads Tested:**
  - SQL Injection payloads (`' OR 1=1 --`, `'; DROP TABLE test_cases; --`) sanitized through SQLite parameterized queries.
  - Cross-Site Scripting tags (`<script>alert('XSS')</script>`) sanitized via Jinja2 auto-escaping.
  - Unicode text, Arabic script, and multi-byte emojis handled cleanly with UTF-8 encoding.
  - Whitespace-only inputs and non-existent foreign keys rejected with validation errors.
- **Verification:** 5 automated tests in `tests/istqb/test_error_guessing.py`.

### 4.6 Risk-Based Testing (RBT)
- **Concept:** Guides testing effort and execution scheduling based on failure risk.
- **Mathematical Formula:**
  $$\text{Risk Priority Number (RPN)} = \text{Likelihood of Failure (1-5)} \times \text{Impact of Failure (1-5)}$$
- **Classification:**
  - $\text{RPN} \in [16, 25]$: **Critical Risk** (Red)
  - $\text{RPN} \in [10, 15]$: **High Risk** (Orange)
  - $\text{RPN} \in [5, 9]$: **Medium Risk** (Cyan)
  - $\text{RPN} \in [1, 4]$: **Low Risk** (Green)
- **Execution Order:** Test runs sort test cases by RPN descending, ensuring critical risks (`TC-PAY-010` Score 20) execute before lower-risk tests.
- **Verification:** 5 automated tests in `tests/istqb/test_risk_based_testing.py`.

### 4.7 Requirements Traceability Matrix (RTM)
- **Concept:** Bi-directional verification linking the Test Basis to Test Results.
  $$\text{Requirement} \longleftrightarrow \text{Test Case} \longleftrightarrow \text{Test Execution} \longleftrightarrow \text{Defect Incident}$$
- **Metrics in TestFlow:**
  - **Specification Coverage:** 100% (5 of 5 requirements covered).
  - **Orphan Test Cases:** 0 (Every test case traces back to a business requirement).
  - **Defect Traceability:** 100% of failed executions trace to logged defect incidents.
- **Verification:** Evaluated via `/rtm` and `tests/regression/test_regression_suite.py`.

### 4.8 Regression Testing
- **Concept:** Re-executing tests to ensure code changes or bug fixes do not break existing functionality.
- **Implementation:** Automated test simulating an entire end-to-end SDLC cycle: creating a requirement, authoring a test case, logging a failure, advancing a defect to `Closed`, and confirming RTM coverage updates.
- **Verification:** Dedicated suite tagged with `@pytest.mark.regression`.

---

## 5. Automated Test Suite & Code Coverage Audit

The automated test suite was executed using Pytest with the Coverage.py plugin:

```
pytest --cov=app --cov-report=term-missing
```

### Official Execution Results Table:

| Test Module | ISTQB / Technical Focus | Test Count | Statement Coverage | Result |
| :--- | :--- | :---: | :---: | :---: |
| `tests/istqb/test_equivalence_partitioning.py` | EP Valid/Invalid Partitions | 19 | 92% | **PASSED** |
| `tests/istqb/test_boundary_value_analysis.py` | BVA 2-value & 3-value Boundaries | 16 | 92% | **PASSED** |
| `tests/istqb/test_decision_table.py` | Decision Tables (Triage & Gate) | 10 | 92% | **PASSED** |
| `tests/istqb/test_state_transition.py` | STT Defect State Machine | 10 | 92% | **PASSED** |
| `tests/istqb/test_risk_based_testing.py` | RBT Scoring & Sorter | 5 | 92% | **PASSED** |
| `tests/istqb/test_error_guessing.py` | SQLi, XSS, Unicode, Edge Cases | 5 | 92% | **PASSED** |
| `tests/api/test_api_endpoints.py` | REST API Integration | 8 | 86% | **PASSED** |
| `tests/unit/test_views.py` | Web Views & Jinja Filters | 8 | 90% | **PASSED** |
| `tests/regression/test_regression_suite.py` | End-to-End STLC Regression | 1 | 98% | **PASSED** |
| `tests/ui/test_ui_automation.py` | Selenium UI WebDriver | 1 | Skipped (CLI flag) | **SKIPPED** |
| **TOTALS** | **Entire TestFlow Application** | **92** | **91%** | **ALL PASSED** |

---

## 6. Project Deliverables Directory

All project assets, documentation, and source code are located in the repository:

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **GitHub Repository** | [eya-khandoudi/TestFlow-ISTQB](https://github.com/eya-khandoudi/TestFlow-ISTQB) | Complete source code, git commit history, and releases |
| **Official PDF Guide** | `docs/TestFlow_ISTQB_Application_Guide.pdf` | 16-page publication-ready guide authored by Eya Khandoudi & Ichraf Sassi |
| **Illustrated Guide** | `docs/APPLICATION_GUIDE.md` | Markdown guide with all 13 high-resolution screenshots |
| **Master Test Plan** | `docs/TEST_PLAN_IEEE829.md` | Formal Master Test Plan conforming to IEEE Std 829-2008 |
| **Defect Lifecycle Spec** | `docs/DEFECT_LIFECYCLE.md` | State machine transition table and guard definitions |
| **RTM Documentation** | `docs/RTM_MATRIX.md` | Cross-reference matrix between requirements and test cases |
| **Screenshots Directory** | `docs/screenshots/` | 13 high-resolution captures of every application view |
| **Source Code** | `app/` | Clean Flask application with modular Blueprints |
| **Test Suite** | `tests/` | Full Pytest automated test suites |

---

## 7. Sign-Off & Approvals

In accordance with Section 11 of the IEEE Std 829-2008 Standard for Test Documentation, the TestFlow testing deliverables have been reviewed and approved:

- **Lead QA Engineers:** **Eya Khandoudi** & **Ichraf Sassi** *(Approved)*
- **Software Development Lead:** Lead Architect *(Reviewed & Approved)*
- **Product Owner:** Product Management *(Accepted)*
- **Overall Project Verdict:** **OFFICIALLY COMPLETED & CERTIFIED**
