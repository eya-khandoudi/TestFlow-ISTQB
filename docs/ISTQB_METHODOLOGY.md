# ISTQB Testing Methodology Guide — TestFlow

## 1. Overview
**TestFlow** is designed specifically to demonstrate end-to-end professional software testing methodologies conforming to the **ISTQB (International Software Testing Qualifications Board)** Foundation Level (CTFL) and Advanced Level (CTAL-TM / CTAL-TA) syllabi.

Rather than being a simple CRUD web application, TestFlow embeds ISTQB principles directly into its architecture, domain rules, data models, and automated test suites.

---

## 2. ISTQB Techniques Implemented & Demonstrated

| ISTQB Concept | Category | TestFlow Implementation | Automated Test Location |
| :--- | :--- | :--- | :--- |
| **Equivalence Partitioning (EP)** | Black-box / Specification | Valid & Invalid input partitions for risk ratings, quantity limits, email fields, and string lengths | `tests/istqb/test_equivalence_partitioning.py` |
| **Boundary Value Analysis (BVA)** | Black-box / Specification | 2-value and 3-value boundary testing on quantity [1, 99], risk ratings [1, 5], and title length [5, 200] | `tests/istqb/test_boundary_value_analysis.py` |
| **Decision Table Testing (DTT)** | Black-box / Specification | Combinatorial logic for automated defect triage (Severity + Environment + Core Flow) & Release Gate decisions | `tests/istqb/test_decision_table.py` |
| **State Transition Testing (STT)** | Black-box / Specification | Defect Lifecycle State Machine (New &rarr; Assigned &rarr; Open &rarr; Fixed &rarr; Retest &rarr; Closed). Enforces legal transitions and rejects invalid jumps | `tests/istqb/test_state_transition.py` |
| **Error Guessing (EG)** | Experience-based | Defect probing with SQLi payloads, XSS injections, Unicode scripts, whitespace-only, and orphaned references | `tests/istqb/test_error_guessing.py` |
| **Risk-Based Testing (RBT)** | Test Strategy / Planning | Risk Priority Number ($RPN = Likelihood \times Impact$, 1-25). Dynamic prioritization of test execution order | `tests/istqb/test_risk_based_testing.py` |
| **Requirements Traceability (RTM)** | Test Management | Forward and backward traceability: $Requirement \leftrightarrow TestCase \leftrightarrow Execution \leftrightarrow Defect$ | `tests/regression/test_regression_suite.py` & `/rtm` |
| **Regression Testing** | Test Execution | Automated end-to-end regression cycle verifying existing capabilities remain unbroken after bug fixes | `tests/regression/test_regression_suite.py` |

---

## 3. Deep Dive into Specific Techniques

### 3.1 Equivalence Partitioning (EP)
Input domains are divided into mutually exclusive partitions:
- **Valid Partitions:** Values expected to be processed successfully.
- **Invalid Partitions:** Values expected to be rejected with appropriate validation feedback.

**Example in TestFlow (`app/services/istqb_engine.py`):**
```python
# Partitioning for Risk Likelihood & Impact:
# Valid: [1, 2, 3, 4, 5]
# Invalid Partition A: Integers < 1 (e.g. 0, -1)
# Invalid Partition B: Integers > 5 (e.g. 6, 100)
# Invalid Partition C: Non-integer / type error (e.g. "abc", None)
validate_risk_rating(rating)
```

### 3.2 Boundary Value Analysis (BVA)
BVA focuses on the boundaries between equivalence partitions where defects cluster:
- **Cart Line Item Quantity Requirement (`REQ-CART-02`):** Permitted range: 1 to 99 units.
- **2-Value / 3-Value Boundary Points:**
  - $0$: Just below minimum $\rightarrow$ **Invalid Boundary** (Triggers `BUG-001`)
  - $1$: Minimum allowable value $\rightarrow$ **Valid Boundary**
  - $2$: Just above minimum $\rightarrow$ **Valid Boundary**
  - $98$: Just below maximum $\rightarrow$ **Valid Boundary**
  - $99$: Maximum allowable value $\rightarrow$ **Valid Boundary**
  - $100$: Just above maximum $\rightarrow$ **Invalid Boundary** (Triggers `BUG-002`)

### 3.3 Decision Table Testing (DTT)
Complex business logic governed by multiple conditions is mapped to decision tables:
- **Defect SLA Triage Rule Table:**

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Severity $\in$ {Blocker, Critical} | **Yes** | **Yes** | **Yes** | No | No | No |
| Environment == 'Production' | **Yes** | No | No | * | * | * |
| Affects Core Flow | * | **Yes** | No | **Yes** | No | * |
| Severity == 'Major' | No | No | No | **Yes** | **Yes** | No |
| Severity == 'Minor' | No | No | No | No | No | **Yes** |
| **Action: Priority** | **Urgent** | **Urgent** | **High** | **High** | **Medium** | **Low** |
| **Action: SLA Hours** | **4h** | **8h** | **16h** | **24h** | **48h** | **120h** |
| **Action: Escalation** | **True** | **True** | False | False | False | False |

### 3.4 State Transition Testing (STT)
Enforces the standardized ISTQB Defect Lifecycle:
```
[ New ] ──────> [ Assigned ] ──────> [ Open ] ──────> [ Fixed ] ──────> [ Retest ] ──────> [ Closed ]
   │                 │                  │                                    │
   ├────────> [ Rejected ]             └──> [ Deferred ]                    └──> [ Reopened ]
   │                 │
   └────────> [ Deferred ]
```
- **Strict Guard Rules:**
  - Cannot jump directly from `New` to `Closed` (Direct close without triage or resolution is forbidden).
  - Cannot close directly from `Open` (Developer cannot close without testing).
  - Cannot close directly from `Fixed` (QA engineer must verify in `Retest` first).
  - Moving to `Fixed`, `Deferred`, or `Rejected` strictly requires resolution notes.

### 3.5 Risk-Based Testing (RBT)
- Formula:
  $$\text{Risk Priority Number (RPN)} = \text{Likelihood of Failure} \times \text{Impact of Failure}$$
- Categories:
  - **Critical (16 - 25):** Core payment flows, gateway timeouts, authentication bypass.
  - **High (10 - 15):** Checkout discount calculation, inventory decrement.
  - **Medium (5 - 9):** Secondary validations, sorting filters.
  - **Low (1 - 4):** UI cosmetic alignments, helper text.
- **Execution Prioritization:** Test execution runs automatically sort test cases by RPN descending, ensuring high-risk defects are detected as early as possible (Shift-Left principle).
