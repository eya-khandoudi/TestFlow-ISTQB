# Requirements Traceability Matrix (RTM)

## 1. Traceability Purpose
The Requirements Traceability Matrix (RTM) establishes a bi-directional link between:
- **Business & Functional Requirements (Test Basis)**
- **Test Cases (Test Design)**
- **Test Executions (STLC Execution)**
- **Defects & Incidents (Defect Management)**

This ensures **100% test coverage**, eliminates untested requirements, and guarantees that no extraneous test cases exist without an underlying business justification.

---

## 2. Master Traceability Table

| Requirement Code | Requirement Title | Category | Test Case Code | Test Type | Priority | Risk Score | Execution Status | Defect Code | Defect Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **REQ-AUTH-01** | User Authentication & Session | Security | `TC-EP-001` | Functional | High | 8 | **Pass** | - | - |
| **REQ-AUTH-01** | User Authentication & Session | Security | `TC-EP-002` | Functional | Medium | 6 | **Pass** | - | - |
| **REQ-CART-02** | Cart Item Limit & Calculation | Functional | `TC-BVA-003` | Functional | High | 4 | **Pass** | - | - |
| **REQ-CART-02** | Cart Item Limit & Calculation | Functional | `TC-BVA-004` | Functional | High | 8 | **Fail** | `BUG-001` | Open |
| **REQ-CART-02** | Cart Item Limit & Calculation | Functional | `TC-BVA-005` | Functional | Medium | 6 | **Pass** | - | - |
| **REQ-CART-02** | Cart Item Limit & Calculation | Functional | `TC-BVA-006` | Functional | Medium | 9 | **Fail** | `BUG-002` | Fixed |
| **REQ-DISC-03** | Discount Voucher Rules | Business Rule | `TC-DT-007` | Business Rule | High | 8 | **Pass** | - | - |
| **REQ-DISC-03** | Discount Voucher Rules | Business Rule | `TC-DT-008` | Business Rule | Medium | 9 | **Pass** | - | - |
| **REQ-PAY-04** | Credit Card Payment Gateway | Payment | `TC-PAY-009` | Payment | Critical | 15 | **Pass** | - | - |
| **REQ-PAY-04** | Credit Card Payment Gateway | Payment | `TC-PAY-010` | Payment | Critical | 20 | **Blocked** | `BUG-003` | New |
| **REQ-AUTH-01** | Security Input Sanitization | Security | `TC-EG-011` | Security | Critical | 10 | **Pass** | - | - |
| **REQ-ORD-05** | Order & Inventory Decrement | Workflow | `TC-REG-012` | Regression | High | 8 | **Untested** | - | - |

---

## 3. Coverage Analysis
- **Total Requirements:** 5
- **Covered Requirements:** 5 (100% Specification Coverage)
- **Total Test Cases:** 12
- **Orphaned Test Cases (No Req Link):** 0
- **Failed Test Cases with Linked Defect:** 100% (Every failure has a corresponding defect logged)
- **High/Critical Risk Coverage:** 100%
