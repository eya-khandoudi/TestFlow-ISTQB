# ISTQB Defect Lifecycle & State Machine Specification

## 1. Defect State Machine Diagram
```
                     ┌───────────────┐
                     │      New      │
                     └───────┬───────┘
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │   Assigned   │ │   Rejected   │ │   Deferred   │
     └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
            │                │                │
            ▼                ▼                │
     ┌──────────────┐ ┌──────────────┐        │
     │     Open     │ │    Closed    │        │
     └──────┬───────┘ └──────▲───────┘        │
            │                │                │
            ▼                │                │
     ┌──────────────┐        │                │
     │    Fixed     │        │                │
     └──────┬───────┘        │                │
            │                │                │
            ▼                │                │
     ┌──────────────┐        │                │
     │    Retest    │────────┘                │
     └──────┬───────┘                         │
            │ (Fix Failed)                    │
            ▼                                 │
     ┌──────────────┐                         │
     │   Reopened   │─────────────────────────┘
     └──────────────┘
```

---

## 2. State Definitions

| State | Role Owner | Description | Exit Criteria |
| :--- | :--- | :--- | :--- |
| **New** | QA Engineer | Defect initially logged with reproduction steps. | Triaged and assigned, rejected, or deferred. |
| **Assigned** | QA Lead / Dev Lead | Defect triaged and allocated to a specific developer. | Developer acknowledges and begins investigation. |
| **Open** | Developer | Active root-cause analysis and code fixing underway. | Code patch developed and committed. |
| **Fixed** | Developer | Bug resolved in development branch; notes added. | Deployed to QA environment for retesting. |
| **Retest** | QA Engineer | Retesting previously failed test case on new build. | Verification of fix. |
| **Closed** | QA Engineer | Fix confirmed working; no regression detected. | Terminal state (or reopened if recurrence). |
| **Reopened** | QA Engineer | Fix failed in retest or recurrence discovered. | Sent back to developer for further work. |
| **Deferred** | Product Owner / QA | Valid bug, but fix postponed to future release. | Re-evaluated in next sprint planning. |
| **Rejected** | Dev Lead / QA | Not a defect, duplicate, or working as designed. | Documented justification provided. |

---

## 3. Allowed Transition Matrix

| From State | Allowed Target States | Strict Validation Rules |
| :--- | :--- | :--- |
| `New` | `Assigned`, `Rejected`, `Deferred` | Direct closure prohibited without triage notes. |
| `Assigned` | `Open`, `Deferred`, `Rejected` | Developer must open before fixing. |
| `Open` | `Fixed`, `Deferred`, `Rejected` | Transition to `Fixed` requires resolution notes. |
| `Fixed` | `Retest` | Cannot jump to `Closed` directly; QA verification required. |
| `Retest` | `Closed`, `Reopened` | `Closed` if passed, `Reopened` if failed. |
| `Reopened` | `Assigned`, `Open`, `Fixed` | Developer re-engages on issue. |
| `Deferred` | `Assigned`, `Open` | Revived in subsequent sprint. |
| `Rejected` | `Closed`, `Reopened` | Closed if team agrees, Reopened if disputed. |
| `Closed` | `Reopened` | Defect recurrence in later regression cycle. |
