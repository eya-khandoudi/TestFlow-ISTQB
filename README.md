# TestFlow – Software Test Management System
### A Python & Flask Application for Professional ISTQB Software Testing Demonstration

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey.svg)](https://palletsprojects.com/p/flask/)
[![Pytest](https://img.shields.io/badge/Tests-92%20Passed-brightgreen.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-91%25-green.svg)](https://coverage.readthedocs.io/)
[![ISTQB Standard](https://img.shields.io/badge/Standard-ISTQB%20CTFL%20%2F%20IEEE%20829-orange.svg)](https://www.istqb.org/)

---

## 1. Project Overview

**TestFlow** is a full-featured web application specifically designed to demonstrate the end-to-end application of **ISTQB (International Software Testing Qualifications Board)** methodologies throughout the **SDLC (Software Development Life Cycle)** and **STLC (Software Testing Life Cycle)**.

QA engineers and development teams can manage requirements, design test cases with formal black-box techniques, execute test cycles, report bugs with strict state-transition lifecycles, and automatically generate **IEEE 829 Test Summary Reports** and **Requirements Traceability Matrices (RTM)**.

---

## 2. Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Clean, modular backend architecture |
| **Backend Framework** | Flask 3.x | Blueprint-based modular microservices pattern |
| **Frontend** | HTML5, Bootstrap 5, Chart.js, JS | Modern responsive UI with live metric visualizations |
| **Database** | SQLite 3 | Portable, zero-configuration relational storage with foreign keys |
| **Unit & Integration Testing** | Pytest 8.x / 9.x | 92 comprehensive automated tests with custom ISTQB markers |
| **Code Coverage** | Coverage.py / pytest-cov | 91% code coverage across all core modules |
| **UI Automation** | Selenium WebDriver | Headless Chrome/Edge end-to-end browser automation |
| **Standards** | ISTQB CTFL / IEEE 829-2008 | Master Test Plan, Defect Lifecycle, RTM, and Test Summary Reports |

---

## 3. ISTQB Methodologies Implemented

TestFlow is built around the fundamental testing techniques defined in the ISTQB syllabus:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ISTQB METHODOLOGIES IN TESTFLOW                       │
├──────────────────────────┬──────────────────────────┬───────────────────────┤
│ Equivalence Partitioning │ Boundary Value Analysis  │ Decision Table        │
│ • Valid/Invalid classes  │ • 2-value & 3-value BVA  │ • Defect SLA Triage   │
│ • Input validation       │ • Cart boundaries [1,99] │ • Release Gate (Go/No)│
├──────────────────────────┼──────────────────────────┼───────────────────────┤
│ State Transition Testing │ Error Guessing           │ Risk-Based Testing    │
│ • Defect Lifecycle       │ • SQLi & XSS resistance  │ • RPN = Likelihood x  │
│ • Illegal transition blk │ • Edge case resilience   │   Impact (1 to 25)    │
├──────────────────────────┴──────────────────────────┴───────────────────────┤
│ Requirements Traceability Matrix (RTM) & IEEE 829 Test Summary Report       │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Equivalence Partitioning (EP):** Input domains (ratings, email, quantities) split into valid and invalid partitions.
2. **Boundary Value Analysis (BVA):** Explicitly verifies minimum, maximum, and out-of-boundary values (e.g., cart quantity: 0, 1, 2, 98, 99, 100).
3. **Decision Table Testing (DTT):** Evaluates complex business combinations to determine defect SLA priority and release go/no-go verdicts.
4. **State Transition Testing (STT):** Implements the standardized ISTQB Defect Lifecycle:
   $$\text{New} \rightarrow \text{Assigned} \rightarrow \text{Open} \rightarrow \text{Fixed} \rightarrow \text{Retest} \rightarrow \text{Closed}$$
   *(Illegal jumps like `New` $\rightarrow$ `Closed` or closing without retest are strictly rejected by the engine).*
5. **Error Guessing (EG):** Probing resilience against SQL injection, XSS script tags, emojis, and unhandled boundary inputs.
6. **Risk-Based Testing (RBT):** Calculates Risk Priority Number ($RPN = Likelihood \times Impact$) to sort and execute the highest risk test cases first.
7. **Traceability (RTM):** Bi-directional matrix mapping Requirements $\leftrightarrow$ Test Cases $\leftrightarrow$ Executions $\leftrightarrow$ Defects.
8. **Regression Testing:** Automated regression suite verifying system integrity after modifications.

---

## 4. Main Application Features

### 4.1 Testing Dashboard & KPI Health
- Real-time pass/fail rates, execution doughnut chart, and defect severity breakdown.
- **IEEE 829 Release Gate Decision:** Automatically calculates whether the release meets exit criteria (Zero open blockers, $\ge 90\%$ pass rate, and $100\%$ critical tests passed).

### 4.2 Requirements Management & Traceability (RTM)
- Create and organize functional, security, performance, and workflow requirements.
- Full bi-directional traceability with coverage percentages and orphaned test case detection.

### 4.3 Test Case Repository & Risk Assessment
- Design test cases specifying preconditions, execution steps, expected results, priority, and test types.
- Dynamic Risk Priority Number ($RPN$) calculation with color-coded risk category badges.

### 4.4 Test Run Execution
- Snapshot active test suites into dedicated test cycles across environments (QA, Staging, UAT, Production).
- Test execution modal to log actual outcomes, status (Pass, Fail, Blocked, Skipped), and direct one-click defect creation.

### 4.5 Defect Management & State Machine
- Report incidents with automated triage suggestions powered by the ISTQB Decision Table.
- Transition defects through permitted lifecycle states with complete audit trails.

### 4.6 IEEE 829 Test Summary Report
- Formatted, printable test summary report containing executive summary, residual defects analysis, and formal sign-off approvals.

---

## 5. Documentation & Deliverables

- **Official Full Project Report (PDF):** [TestFlow_Full_Project_Report.pdf](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/TestFlow_Full_Project_Report.pdf) *(Master ISTQB Software Testing Final Report, IEEE 829 Test Plan & Coverage Evaluation by Eya Khandoudi & Ichraf Sassi)*
- **Illustrated Application Guide (PDF):** [TestFlow_ISTQB_Application_Guide.pdf](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/TestFlow_ISTQB_Application_Guide.pdf) *(16-page visual guide with high-resolution screenshots & UI breakdown)*
- **Illustrated Markdown Guide:** [APPLICATION_GUIDE.md](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/APPLICATION_GUIDE.md)
- **ISTQB Methodology Guide:** [ISTQB_METHODOLOGY.md](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/ISTQB_METHODOLOGY.md)
- **IEEE 829 Master Test Plan:** [TEST_PLAN_IEEE829.md](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/TEST_PLAN_IEEE829.md)
- **Defect Lifecycle Specification:** [DEFECT_LIFECYCLE.md](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/DEFECT_LIFECYCLE.md)
- **Requirements Traceability Matrix:** [RTM_MATRIX.md](file:///c:/Users/Eya%20Khandoudi/Downloads/istqb/ISTQB/docs/RTM_MATRIX.md)

---

## 6. Quickstart & Installation

### Step 1: Clone or Navigate to Project
```bash
cd "c:\Users\Eya Khandoudi\Downloads\istqb\ISTQB"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 6. Running the Automated Test Suites

The test suite contains **92 automated tests** covering all ISTQB techniques and application routes:

### Run All Tests
```bash
pytest
```

### Run Tests with Code Coverage Analysis (91% Coverage)
```bash
pytest --cov=app --cov-report=term-missing
```

### Run Tests by Specific ISTQB Technique Marker

| Technique | Pytest Command |
| :--- | :--- |
| **Equivalence Partitioning** | `pytest -m equivalence_partitioning` |
| **Boundary Value Analysis** | `pytest -m boundary_value_analysis` |
| **Decision Table Testing** | `pytest -m decision_table` |
| **State Transition Testing** | `pytest -m state_transition` |
| **Error Guessing** | `pytest -m error_guessing` |
| **Risk-Based Testing** | `pytest -m risk_based` |
| **Regression Test Suite** | `pytest -m regression` |
| **REST API Automation** | `pytest -m api` |

---

## 7. REST API Endpoints

TestFlow provides a comprehensive REST API for CI/CD pipeline integration and automated testing:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status check |
| `GET` | `/api/metrics` | Real-time testing KPIs and release gate verdict |
| `GET` | `/api/requirements` | Retrieve all test basis requirements |
| `GET` | `/api/test-cases` | List test cases with risk scores |
| `POST` | `/api/test-cases` | Create test case with BVA/EP validation |
| `POST` | `/api/test-runs/<id>/executions` | Record test execution result |
| `GET` | `/api/defects` | List reported defects |
| `POST` | `/api/defects` | Report a new defect |
| `POST` | `/api/defects/<id>/transition` | Execute state machine transition |
| `POST` | `/api/istqb/triage` | Evaluate Defect Triage Decision Table |
| `POST` | `/api/istqb/risk` | Calculate RBT Risk Priority Number |

---

## 8. Project Structure

```
ISTQB/
├── app/
│   ├── __init__.py                # Flask application factory & custom filters
│   ├── config.py                  # Environment configurations
│   ├── database.py                # SQLite schema & seed data
│   ├── services/
│   │   ├── __init__.py
│   │   ├── istqb_engine.py        # Core ISTQB logic (STT, DTT, BVA, EP, RBT)
│   │   └── report_service.py      # Dashboard metrics, RTM, & IEEE 829 generator
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py                # Dashboard, RTM, & Guide routes
│   │   ├── requirements.py        # Requirements management
│   │   ├── test_cases.py          # Test case CRUD & RBT sorter
│   │   ├── test_runs.py           # Test execution & cycle recording
│   │   ├── defects.py             # Defect lifecycle & state transitions
│   │   └── api.py                 # REST API endpoints
│   ├── static/
│   │   ├── css/style.css          # Clean dashboard styling
│   │   └── js/app.js              # Real-time risk preview calculator
│   └── templates/
│       ├── base.html              # Responsive layout with navigation
│       ├── dashboard.html         # KPI cards, Chart.js, and Release Gate
│       ├── requirements/          # Requirement list & forms
│       ├── test_cases/            # Test case list, form, detail
│       ├── test_runs/             # Test runs & execution recording modal
│       ├── defects/               # Defect list, form, and state transition UI
│       └── reports/
│           ├── rtm.html           # Requirements Traceability Matrix
│           ├── test_summary_report.html # IEEE 829 Test Summary Report
│           └── istqb_guide.html   # Interactive ISTQB concepts guide
├── docs/
│   ├── ISTQB_METHODOLOGY.md       # Comprehensive ISTQB techniques guide
│   ├── TEST_PLAN_IEEE829.md       # Official Master Test Plan
│   ├── DEFECT_LIFECYCLE.md        # State machine transition specification
│   └── RTM_MATRIX.md              # Requirements Traceability documentation
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures & isolated DB setup
│   ├── istqb/                     # Dedicated ISTQB technique test suites
│   │   ├── test_equivalence_partitioning.py
│   │   ├── test_boundary_value_analysis.py
│   │   ├── test_decision_table.py
│   │   ├── test_state_transition.py
│   │   ├── test_error_guessing.py
│   │   └── test_risk_based_testing.py
│   ├── unit/
│   │   └── test_views.py          # Route & template rendering tests
│   ├── api/
│   │   └── test_api_endpoints.py  # REST API integration tests
│   ├── regression/
│   │   └── test_regression_suite.py # End-to-End STLC regression cycle
│   └── ui/
│       └── test_ui_automation.py  # Selenium WebDriver UI automation
├── pytest.ini                     # Pytest configuration with ISTQB markers
├── requirements.txt               # Dependencies
├── run.py                         # Application launcher
└── README.md                      # Project documentation
```

---

## 9. License & Academic Attribution
Developed as an exemplary software testing project demonstrating ISTQB Foundation & Advanced Level software testing methodologies.
