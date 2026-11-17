import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app=None):
    if app:
        with app.app_context():
            db = get_db()
            _create_schema(db)
            _seed_data(db)
    else:
        db = get_db()
        _create_schema(db)
        _seed_data(db)

def _create_schema(db):
    schema_sql = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS requirements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        req_code TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT DEFAULT 'Functional',
        priority TEXT DEFAULT 'Medium',
        project_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS test_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tc_code TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        precondition TEXT,
        steps TEXT NOT NULL,
        expected_result TEXT NOT NULL,
        test_type TEXT DEFAULT 'Functional',
        priority TEXT DEFAULT 'Medium',
        risk_likelihood INTEGER DEFAULT 2,
        risk_impact INTEGER DEFAULT 3,
        risk_score INTEGER GENERATED ALWAYS AS (risk_likelihood * risk_impact) VIRTUAL,
        requirement_id INTEGER,
        project_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (requirement_id) REFERENCES requirements (id) ON DELETE SET NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS test_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        description TEXT,
        environment TEXT DEFAULT 'QA',
        status TEXT DEFAULT 'In Progress',
        project_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS test_executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_run_id INTEGER NOT NULL,
        test_case_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Untested',
        actual_result TEXT,
        executed_by TEXT DEFAULT 'QA Engineer',
        executed_at TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (test_run_id) REFERENCES test_runs (id) ON DELETE CASCADE,
        FOREIGN KEY (test_case_id) REFERENCES test_cases (id) ON DELETE CASCADE,
        UNIQUE (test_run_id, test_case_id)
    );

    CREATE TABLE IF NOT EXISTS defects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bug_code TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        steps_to_reproduce TEXT NOT NULL,
        severity TEXT NOT NULL DEFAULT 'Major',
        priority TEXT NOT NULL DEFAULT 'Medium',
        status TEXT NOT NULL DEFAULT 'New',
        environment TEXT DEFAULT 'QA',
        test_case_id INTEGER,
        test_execution_id INTEGER,
        requirement_id INTEGER,
        assigned_to TEXT DEFAULT 'Unassigned',
        resolution_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (test_case_id) REFERENCES test_cases (id) ON DELETE SET NULL,
        FOREIGN KEY (test_execution_id) REFERENCES test_executions (id) ON DELETE SET NULL,
        FOREIGN KEY (requirement_id) REFERENCES requirements (id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS defect_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        defect_id INTEGER NOT NULL,
        from_status TEXT NOT NULL,
        to_status TEXT NOT NULL,
        changed_by TEXT DEFAULT 'QA Engineer',
        comment TEXT,
        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (defect_id) REFERENCES defects (id) ON DELETE CASCADE
    );
    """
    db.executescript(schema_sql)
    db.commit()

def _seed_data(db):
    # Check if project already exists
    cur = db.execute("SELECT COUNT(*) as count FROM projects")
    if cur.fetchone()['count'] > 0:
        return

    # 1. Project
    db.execute("""
        INSERT INTO projects (name, description)
        VALUES ('E-Commerce Checkout & Payment', 'ISTQB Demonstration Project: Testing the core order, checkout, discount calculation, and payment workflows.')
    """)
    project_id = 1

    # 2. Requirements (ISTQB: Basis for Test Cases and Traceability)
    requirements = [
        ('REQ-AUTH-01', 'User Authentication & Session', 'System shall authenticate registered users using valid email and password with secure session handling.', 'Security', 'High'),
        ('REQ-CART-02', 'Cart Item Limit & Total Calculation', 'Shopping cart shall accept between 1 and 99 items per line item and accurately calculate subtotals and taxes.', 'Functional', 'High'),
        ('REQ-DISC-03', 'Discount Voucher Application', 'System shall apply valid promo codes (e.g., ISTQB10 for 10% off, SAVE20 for $20 off orders > $100). Codes are mutually exclusive.', 'Business Rule', 'Medium'),
        ('REQ-PAY-04', 'Credit Card Payment Gateway Integration', 'System shall accept Visa/Mastercard payments. Cards expiring prior to current month must be rejected.', 'Payment', 'Critical'),
        ('REQ-ORD-05', 'Order Confirmation & Email Notification', 'Upon successful payment, system shall transition order to Paid, decrement inventory, and send email confirmation.', 'Workflow', 'High')
    ]
    for r in requirements:
        db.execute("""
            INSERT INTO requirements (req_code, title, description, category, priority, project_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r[0], r[1], r[2], r[3], r[4], project_id))

    # 3. Test Cases (Demonstrating EP, BVA, Decision Table, Error Guessing, RBT)
    test_cases = [
        (
            'TC-EP-001', 'Verify User Login with Valid Credentials',
            'Equivalence Partitioning: Valid input partition for email and password format.',
            'User account test@testflow.qa exists with password P@ssword123.',
            '1. Navigate to /login\n2. Enter valid email\n3. Enter valid password\n4. Click Submit',
            'User is redirected to Dashboard and session token is issued.',
            'Functional', 'High', 2, 4, 1
        ),
        (
            'TC-EP-002', 'Verify User Login Rejection with Invalid Email Format',
            'Equivalence Partitioning: Invalid input partition for email (missing @ or domain).',
            'Login page loaded.',
            '1. Enter "invalid-email-address"\n2. Enter "Pass1234"\n3. Click Submit',
            'Validation error message "Please enter a valid email address" displayed.',
            'Functional', 'Medium', 3, 2, 1
        ),
        (
            'TC-BVA-003', 'Cart Line Quantity - Lower Boundary (Qty = 1)',
            'Boundary Value Analysis: Minimum valid cart quantity boundary.',
            'Item in stock with inventory >= 1.',
            '1. Add item to cart\n2. Set quantity to 1\n3. Click update',
            'Cart updates to 1 item and subtotal equals unit price.',
            'Functional', 'High', 1, 4, 2
        ),
        (
            'TC-BVA-004', 'Cart Line Quantity - Below Min Boundary (Qty = 0)',
            'Boundary Value Analysis: Just below min boundary (0). Should trigger item removal prompt or error.',
            'Item in cart with quantity 1.',
            '1. Edit quantity to 0\n2. Click update',
            'System prompts user to confirm item removal or rejects 0 quantity.',
            'Functional', 'High', 2, 4, 2
        ),
        (
            'TC-BVA-005', 'Cart Line Quantity - Upper Boundary (Qty = 99)',
            'Boundary Value Analysis: Maximum allowable item quantity boundary.',
            'Item has inventory > 100.',
            '1. Set quantity to 99\n2. Click update',
            'Cart updates successfully to 99 items with total price calculated.',
            'Functional', 'Medium', 2, 3, 2
        ),
        (
            'TC-BVA-006', 'Cart Line Quantity - Exceeding Upper Boundary (Qty = 100)',
            'Boundary Value Analysis: Just above max boundary (100). Exceeds allowable quantity limit.',
            'Item in cart.',
            '1. Set quantity to 100\n2. Click update',
            'Error message displayed: "Maximum quantity per line item is 99 units."',
            'Functional', 'Medium', 3, 3, 2
        ),
        (
            'TC-DT-007', 'Decision Table: Discount Code Rules (Order > $100 + SAVE20)',
            'Decision Table Rule 1: Order total > $100 and SAVE20 promo entered.',
            'Cart subtotal is $120.00.',
            '1. Enter promo code "SAVE20"\n2. Click Apply',
            'Discount of $20.00 is deducted; Final Total = $100.00.',
            'Business Rule', 'High', 2, 4, 3
        ),
        (
            'TC-DT-008', 'Decision Table: Discount Code Rules (Order < $100 + SAVE20)',
            'Decision Table Rule 2: Order total <= $100 and SAVE20 promo entered.',
            'Cart subtotal is $80.00.',
            '1. Enter promo code "SAVE20"\n2. Click Apply',
            'Promo rejected with message: "Order total must be at least $100 for this voucher."',
            'Business Rule', 'Medium', 3, 3, 3
        ),
        (
            'TC-PAY-009', 'Payment Gateway - Valid Credit Card Transaction',
            'Risk-Based Testing: Critical risk transaction for order placement.',
            'Cart has active items and billing address entered.',
            '1. Enter valid 16-digit card number\n2. Enter future expiry date\n3. Enter valid CVV\n4. Click Pay Now',
            'Payment processed successfully, transaction ID generated, Order status set to Paid.',
            'Payment', 'Critical', 3, 5, 4
        ),
        (
            'TC-PAY-010', 'Payment Gateway - Expired Credit Card Rejection',
            'Boundary & Validation Testing: Expiry date prior to current month/year.',
            'Checkout page loaded.',
            '1. Enter test card with expiry date 10/2023 (past)\n2. Enter CVV\n3. Click Pay Now',
            'Payment declined with message: "Card has expired. Please use a valid card."',
            'Payment', 'Critical', 4, 5, 4
        ),
        (
            'TC-EG-011', 'Error Guessing - SQL Injection in Search and Input Fields',
            'Error Guessing: Test application resilience against SQL injection payloads.',
            'Search bar and input forms available.',
            '1. Enter "\' OR 1=1 --" into search and voucher fields\n2. Submit input',
            'System sanitizes input, executes parameterized query without syntax errors or data leak.',
            'Security', 'Critical', 2, 5, 1
        ),
        (
            'TC-REG-012', 'Regression: Order Confirmation & Inventory Decrement',
            'Regression Test: Ensure inventory counts decrease consistently after order placement.',
            'Product SKU-001 has initial stock = 50.',
            '1. Complete checkout for 2 units of SKU-001\n2. Check inventory table in database',
            'Stock for SKU-001 is updated to 48.',
            'Regression', 'High', 2, 4, 5
        )
    ]
    for tc in test_cases:
        db.execute("""
            INSERT INTO test_cases (
                tc_code, title, description, precondition, steps, expected_result,
                test_type, priority, risk_likelihood, risk_impact, requirement_id, project_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (tc[0], tc[1], tc[2], tc[3], tc[4], tc[5], tc[6], tc[7], tc[8], tc[9], tc[10], project_id))

    # 4. Test Run (Sprint 1 Regression & Functional Test Cycle)
    db.execute("""
        INSERT INTO test_runs (run_code, name, description, environment, status, project_id)
        VALUES ('TR-2026-001', 'Sprint 1 Acceptance & Regression Cycle', 'Master test run executing acceptance criteria and regression suite for checkout.', 'QA', 'In Progress', ?)
    """, (project_id,))
    run_id = 1

    # 5. Test Executions for the run
    # Let's populate executions with a realistic mix of Pass, Fail, Blocked, Untested
    executions = [
        (run_id, 1, 'Pass', 'Login succeeded with HTTP 200 and auth cookie.', 'Tester Alice', '2026-11-17 10:00:00', 'Passed first attempt.'),
        (run_id, 2, 'Pass', 'Email format regex correctly blocked invalid inputs.', 'Tester Alice', '2026-11-17 10:15:00', 'Validation passed.'),
        (run_id, 3, 'Pass', 'Cart quantity set to 1 successfully.', 'Tester Bob', '2026-11-17 10:30:00', 'Passed.'),
        (run_id, 4, 'Fail', 'Setting quantity to 0 caused 500 Internal Server Error instead of prompt.', 'Tester Bob', '2026-11-17 10:45:00', 'Defect BUG-001 raised.'),
        (run_id, 5, 'Pass', 'Quantity 99 allowed, total calculated correctly.', 'Tester Bob', '2026-11-17 11:00:00', 'Passed.'),
        (run_id, 6, 'Fail', 'Quantity 100 did not show validation warning; processed 100 units.', 'Tester Bob', '2026-11-17 11:15:00', 'Defect BUG-002 raised.'),
        (run_id, 7, 'Pass', '$20 discount deducted correctly on $120 order.', 'Tester Charlie', '2026-11-17 11:30:00', 'Rule 1 verified.'),
        (run_id, 8, 'Pass', 'Voucher declined for $80 order with proper user feedback.', 'Tester Charlie', '2026-11-17 11:45:00', 'Rule 2 verified.'),
        (run_id, 9, 'Pass', 'Mock gateway accepted valid card and returned auth code.', 'Tester Alice', '2026-11-17 12:00:00', 'Passed.'),
        (run_id, 10, 'Blocked', 'Cannot execute: Payment gateway sandbox timeout occurred.', 'Tester Alice', '2026-11-17 12:15:00', 'Awaiting gateway recovery.'),
        (run_id, 11, 'Pass', 'Parameterized query blocked injection payload cleanly.', 'Tester Security', '2026-11-17 13:00:00', 'Security check passed.'),
        (run_id, 12, 'Untested', None, 'QA Engineer', None, 'Pending regression execution.')
    ]
    for ex in executions:
        db.execute("""
            INSERT INTO test_executions (test_run_id, test_case_id, status, actual_result, executed_by, executed_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ex)

    # 6. Defects (Demonstrating Defect Lifecycle & State Transitions)
    defects = [
        (
            'BUG-001', '500 Server Error when updating cart item quantity to 0',
            'When setting line item quantity to 0, backend throws ZeroDivisionError in subtotal calculation.',
            '1. Add item to cart\n2. Change quantity to 0\n3. Click Update Cart',
            'Critical', 'High', 'Open', 'QA', 4, 4, 2, 'dev_backend',
            'Investigating in branch fix/cart-zero-qty'
        ),
        (
            'BUG-002', 'Cart accepts quantity 100 violating max limit of 99',
            'Boundary Value Analysis failure: Quantity validation misses upper boundary check for 100+ items.',
            '1. Add item to cart\n2. Enter 100 in quantity field\n3. Click Update',
            'Major', 'Medium', 'Fixed', 'QA', 6, 6, 2, 'dev_frontend',
            'Added client and server boundary check (max=99). Ready for retest.'
        ),
        (
            'BUG-003', 'Payment gateway mock timeout during expired card test',
            'Timeout during communication with payment mock sandbox under concurrent test load.',
            '1. Submit payment with expired card\n2. Request hangs for 60s then times out',
            'Blocker', 'Urgent', 'New', 'QA', 10, 10, 4, 'Unassigned',
            'Needs immediate triage by infrastructure team.'
        )
    ]
    for d in defects:
        db.execute("""
            INSERT INTO defects (
                bug_code, title, description, steps_to_reproduce, severity, priority,
                status, environment, test_case_id, test_execution_id, requirement_id,
                assigned_to, resolution_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, d)

    # 7. Defect History logs
    history_entries = [
        (1, 'New', 'Open', 'Lead QA', 'Triaged and assigned to backend team.'),
        (2, 'New', 'Open', 'Lead QA', 'Verified bug on QA environment.'),
        (2, 'Open', 'Fixed', 'Developer John', 'Boundary check applied in commit #89f2a.'),
        (3, 'New', 'New', 'Tester Alice', 'Initial defect logged from TR-2026-001 execution.')
    ]
    for h in history_entries:
        db.execute("""
            INSERT INTO defect_history (defect_id, from_status, to_status, changed_by, comment)
            VALUES (?, ?, ?, ?, ?)
        """, h)

    db.commit()
