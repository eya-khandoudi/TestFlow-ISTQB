import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, HRFlowable
from reportlab.pdfgen import canvas

SCREENSHOTS_DIR = r"c:\Users\Eya Khandoudi\Downloads\istqb\ISTQB\docs\screenshots"
DOCS_DIR = r"c:\Users\Eya Khandoudi\Downloads\istqb\ISTQB\docs"
ARTIFACT_DIR = r"C:\Users\Eya Khandoudi\.gemini\antigravity\brain\86fc9c4c-e6f5-410e-86a3-c9ce2182b962"

PPTX_PATH = os.path.join(DOCS_DIR, "TestFlow_ISTQB_Presentation.pptx")
PDF_PATH = os.path.join(DOCS_DIR, "TestFlow_ISTQB_Presentation.pdf")
ARTIFACT_PPTX_PATH = os.path.join(ARTIFACT_DIR, "TestFlow_ISTQB_Presentation.pptx")
ARTIFACT_PDF_PATH = os.path.join(ARTIFACT_DIR, "TestFlow_ISTQB_Presentation.pdf")

# ==============================================================================
# 1. BUILD PPTX PRESENTATION
# ==============================================================================
def create_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    c_navy = RGBColor(15, 41, 66)
    c_blue = RGBColor(43, 108, 176)
    c_teal = RGBColor(13, 148, 136)
    c_dark = RGBColor(30, 41, 59)
    c_gray = RGBColor(100, 116, 139)
    c_light_bg = RGBColor(248, 250, 252)
    c_white = RGBColor(255, 255, 255)
    c_green = RGBColor(34, 84, 61)
    c_red = RGBColor(197, 48, 48)

    def add_header(slide, tag_text, title_text):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = tag_text.upper()
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = c_blue

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.name = "Arial"
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = c_navy
        p2.space_before = Pt(3)

    def add_card(slide, left, top, width, height, bg_color=c_light_bg, border_color=RGBColor(226, 232, 240)):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    # --------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = add_card(s1, Inches(0), Inches(0), Inches(13.333), Inches(7.5), bg_color=c_navy, border_color=c_navy)

    # Title container
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ISTQB & IEEE 829 SOFTWARE TESTING PROJECT"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(144, 205, 244)

    p = tf.add_paragraph()
    p.text = "TestFlow — Software Test Management System"
    p.font.name = "Arial"
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.space_before = Pt(10)

    p = tf.add_paragraph()
    p.text = "Comprehensive STLC Demonstration, Formal Test Design Techniques, Automation & Quality Evaluation"
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(12)

    # Authors badge
    p = tf.add_paragraph()
    p.text = "Presenters & Lead QA:  Eya Khandoudi & Ichraf Sassi"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(254, 240, 138)
    p.space_before = Pt(30)

    p = tf.add_paragraph()
    p.text = "Standards: ISTQB CTFL v4.0 / CTAL-TM  |  IEEE Std 829-2008 Standard  |  November 2026"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(6)

    s1.notes_slide.notes_text_frame.text = (
        "Welcome everyone. Today, Ichraf and I are presenting TestFlow, an end-to-end software test management system "
        "specifically designed to demonstrate rigorous software testing methodologies throughout the SDLC and STLC. "
        "Our project strictly follows the ISTQB syllabus and IEEE 829 documentation standards."
    )

    # --------------------------------------------------------------------------
    # SLIDE 2: Project Vision & SUT
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Project Overview & Scope", "Beyond a Simple CRUD: An ISTQB Demonstration Platform")

    c1 = add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "The Problem in Academic QA Projects"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    bullets1 = [
        "Most student applications are basic CRUD apps with unstructured, ad-hoc testing.",
        "Testing techniques (EP, BVA, Decision Tables) are typically only written in reports but NEVER enforced in code.",
        "Defect lifecycles are treated as simple text dropdowns with zero state machine validation.",
        "Requirements lack bi-directional traceability to actual executions and logged incidents."
    ]
    for b in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark
        p.space_before = Pt(8)

    c2 = add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Our Solution: TestFlow SUT Architecture"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = c_navy
    bullets2 = [
        "Software Under Test (SUT): E-Commerce Checkout, Cart Quantities, Voucher Rules & Payment Gateway.",
        "Active Backend Enforcement: Python state machines and input validators actively enforce ISTQB rules.",
        "100% Traceability (RTM): Requirements <-> Test Cases <-> Executions <-> Defects.",
        "Automated IEEE 829 Release Gate: Evaluates exit criteria in real time to calculate Go / No-Go verdict.",
        "92 Automated Tests with 91% code coverage via Pytest and Coverage.py."
    ]
    for b in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = c_dark
        p.space_before = Pt(8)

    s2.notes_slide.notes_text_frame.text = (
        "In many software engineering projects, testing is an afterthought. We wanted to build TestFlow to prove that "
        "professional testing techniques can be directly embedded into software architecture. Our system under test covers "
        "complex business rules like shopping cart boundaries, discount voucher logic, and payment integrations."
    )

    # --------------------------------------------------------------------------
    # SLIDE 3: Tech Stack & Architecture
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Architecture & Technology Stack", "Robust, Modular Python & Flask Implementation")

    col_w = Inches(2.7)
    gap = Inches(0.25)
    start_x = Inches(0.8)
    top_y = Inches(1.8)
    card_h = Inches(5.0)

    techs = [
        ("Backend Tier", "Python 3.13 & Flask 3.1", [
            "Application Factory pattern",
            "6 Modular Blueprints",
            "REST API endpoints",
            "Real-time calculations"
        ], c_blue),
        ("Database Tier", "SQLite 3 Relational", [
            "Atomic ACID transactions",
            "Foreign key constraints",
            "Generated columns (RPN)",
            "Audit history logging"
        ], c_teal),
        ("Testing Framework", "Pytest 9.2 & Coverage", [
            "92 Automated unit/API tests",
            "Custom ISTQB markers",
            "91% statement coverage",
            "Parameterized test fixtures"
        ], c_green),
        ("Frontend & UI", "Bootstrap 5 & Chart.js", [
            "Responsive layout",
            "Chart.js live charts",
            "Dynamic RBT preview slider",
            "Selenium headless automation"
        ], c_navy)
    ]

    for i, (title, sub, items, col) in enumerate(techs):
        x = start_x + i * (col_w + gap)
        add_card(s3, x, top_y, col_w, card_h)
        tb = s3.shapes.add_textbox(x + Inches(0.15), top_y + Inches(0.2), col_w - Inches(0.3), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark
        p.space_before = Pt(4)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(9.5)
            p.font.color.rgb = c_dark
            p.space_before = Pt(10)

    s3.notes_slide.notes_text_frame.text = (
        "TestFlow uses a clean, decoupled architecture. The backend is written in Python 3.13 using Flask with Blueprints. "
        "The relational database is SQLite with strict foreign key integrity. Testing is handled through Pytest with custom markers, "
        "and our frontend features Bootstrap 5 and Chart.js for real-time visualization."
    )

    # --------------------------------------------------------------------------
    # SLIDE 4: The 8 ISTQB Methodologies Implemented
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Core Testing Methodologies", "8 Formal ISTQB Techniques Directly Built Into TestFlow")

    grid_items = [
        ("Equivalence Partitioning (EP)", "Valid and invalid input domain partitions for risk ratings, quantities, and email formats.", c_blue),
        ("Boundary Value Analysis (BVA)", "2-value and 3-value boundary tests on cart quantities [1, 99], triggering real bugs at 0 and 100.", c_green),
        ("Decision Table Testing (DTT)", "Combinatorial truth tables for Defect SLA Triage Priority and IEEE 829 Release Gate Decisions.", c_teal),
        ("State Transition Testing (STT)", "Defect Lifecycle state machine enforcing valid transitions and strictly rejecting illegal jumps.", c_red),
        ("Risk-Based Testing (RBT)", "Formula: RPN = Likelihood x Impact (1-25). Dynamically prioritizes test runs to catch blockers early.", c_navy),
        ("Error Guessing (EG)", "Negative testing resilience against classic SQL injection payloads, XSS script tags, and orphan keys.", c_blue),
        ("Traceability Matrix (RTM)", "Bi-directional matrix linking Requirements <-> Test Cases <-> Executions <-> Defects with 0 gaps.", c_teal),
        ("Regression Testing", "Automated end-to-end SDLC/STLC cycle ensuring patches do not break existing verified functionality.", c_green)
    ]

    gw = Inches(5.6)
    gh = Inches(1.1)
    for i, (title, desc, col) in enumerate(grid_items):
        r = i // 2
        c = i % 2
        x = Inches(0.8) + c * Inches(6.0)
        y = Inches(1.8) + r * Inches(1.3)
        add_card(s4, x, y, gw, gh)
        tb = s4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), gw - Inches(0.4), gh - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(2)

    s4.notes_slide.notes_text_frame.text = (
        "Here you see the 8 formal ISTQB techniques we implemented. Each technique is not just documented in our report — "
        "it is backed by dedicated Python algorithms in our domain engine and verified by automated Pytest test suites."
    )

    # --------------------------------------------------------------------------
    # SLIDE 5: Live UI — Dashboard & Release Gate
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "System Walkthrough: Dashboard", "Real-Time Quality Health & Automated Release Gate")

    # Left: Screenshot
    img_path1 = os.path.join(SCREENSHOTS_DIR, "01_dashboard.png")
    if os.path.exists(img_path1):
        s5.shapes.add_picture(img_path1, Inches(0.8), Inches(1.8), width=Inches(6.8))

    # Right: Explanatory Card
    add_card(s5, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.0))
    tb = s5.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Operational Features"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    features = [
        "<b>Decision Table Release Gate:</b> Automatically evaluates exit criteria: 0 blockers, >=90% pass rate. Currently displays <b>NO-GO</b> due to 2 open blocker/critical bugs.",
        "<b>KPI Summary Cards:</b> Real-time counters for requirements, test cases, pass rate percentage, and open blocker count.",
        "<b>Chart.js Visualizations:</b> Live doughnut chart of execution status (Pass, Fail, Blocked) and bar chart of defects by severity.",
        "<b>Active Cycles & Shortcuts:</b> One-click access to in-progress test runs and recently logged defect incident reports."
    ]
    for feat in features:
        p = tf.add_paragraph()
        p.text = "• " + feat.replace("<b>", "").replace("</b>", "")
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(10)

    s5.notes_slide.notes_text_frame.text = (
        "This is our main dashboard. As you can see, the red banner at the top shows our IEEE 829 Release Gate Decision. "
        "Because we have 2 open blocker and critical defects, the decision table automatically sets the verdict to NO-GO. "
        "This gives QA leadership an instant, objective release assessment based on empirical data."
    )

    # --------------------------------------------------------------------------
    # SLIDE 6: BVA & Equivalence Partitioning
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Specification-Based Testing", "Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)")

    # Left: Cart quantity BVA table
    add_card(s6, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Cart Item Quantity Boundaries [1, 99]"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    bva_bullets = [
        "<b>0 (Min - 1):</b> Invalid boundary. System threw 500 error &rarr; <b>Logged BUG-001 (Critical)</b>.",
        "<b>1 (Min):</b> Minimum valid boundary. Accepted successfully (TC-BVA-003).",
        "<b>2 (Min + 1):</b> 3-value BVA valid point. Accepted correctly.",
        "<b>98 (Max - 1):</b> 3-value BVA valid point. Accepted correctly.",
        "<b>99 (Max):</b> Maximum valid boundary. Accepted successfully (TC-BVA-005).",
        "<b>100 (Max + 1):</b> Invalid boundary. Validation missed &rarr; <b>Logged BUG-002 (Major)</b>."
    ]
    for b in bva_bullets:
        p = tf.add_paragraph()
        p.text = "• " + b.replace("<b>", "").replace("</b>", "").replace("&rarr;", "->")
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(8)

    # Right: EP and Form Screenshot
    add_card(s6, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.0))
    tb2 = s6.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Equivalence Partitioning (EP) Applied"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    ep_bullets = [
        "<b>Email Address Format:</b> Valid partition (user@domain.com) vs Invalid partitions (missing @, missing TLD, illegal spaces). Tested via TC-EP-001 & TC-EP-002.",
        "<b>Risk Likelihood & Impact [1, 5]:</b> Valid partition [1-5] vs Invalid partitions (<1, >5, non-numeric).",
        "<b>Text Field Lengths:</b> Enforces boundaries on Code [3, 20] and Title [5, 200] characters.",
        "<b>Backend Validator:</b> Programmed in <code>app/services/istqb_engine.py</code> and verified by 35 automated Pytest tests."
    ]
    for b in ep_bullets:
        p = tf2.add_paragraph()
        p.text = "• " + b.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "")
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(10)

    s6.notes_slide.notes_text_frame.text = (
        "On this slide, we illustrate our specification-based design. We chose our shopping cart quantity requirement "
        "to demonstrate 2-value and 3-value BVA. Notice that our boundary testing actually uncovered two real defects: "
        "BUG-001 at 0 items, and BUG-002 at 100 items. This proves the classic ISTQB principle that defects cluster at boundaries."
    )

    # --------------------------------------------------------------------------
    # SLIDE 7: Decision Table Testing
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Combinatorial Testing", "Decision Table Testing (DTT): Defect SLA & Release Rules")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Defect SLA Triage Decision Table"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    p = tf.add_paragraph()
    p.text = "Evaluates multi-condition inputs to automatically determine SLA resolution targets and escalation requirements:"
    p.font.size = Pt(10)
    p.font.color.rgb = c_gray
    p.space_before = Pt(4)

    # Decision Table as table shape
    rows, cols = 8, 7
    t_shape = s7.shapes.add_table(rows, cols, Inches(1.0), Inches(2.8), Inches(11.3), Inches(3.6))
    t = t_shape.table
    t.columns[0].width = Inches(3.3)
    for c in range(1, 7):
        t.columns[c].width = Inches(1.33)

    headers = ["Condition / Action", "Rule 1", "Rule 2", "Rule 3", "Rule 4", "Rule 5", "Rule 6"]
    for c, h in enumerate(headers):
        cell = t.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.color.rgb = c_white

    table_rows = [
        ("Severity in {Blocker, Critical}", ["True", "True", "True", "False", "False", "False"]),
        ("Environment == 'Production'", ["True", "False", "False", "*", "*", "*"]),
        ("Affects Core Flow (Checkout/Auth)", ["*", "True", "False", "True", "False", "*"]),
        ("Severity == 'Major'", ["False", "False", "False", "True", "True", "False"]),
        ("Severity == 'Minor'", ["False", "False", "False", "False", "False", "True"]),
        ("OUTPUT: Priority", ["Urgent", "Urgent", "High", "High", "Medium", "Low"]),
        ("OUTPUT: Max SLA Hours", ["4 Hours", "8 Hours", "16 Hours", "24 Hours", "48 Hours", "120 Hours"]),
    ]

    for r_idx, (cond, vals) in enumerate(table_rows, start=1):
        cell = t.cell(r_idx, 0)
        cell.text = cond
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_light_bg if r_idx <= 5 else RGBColor(235, 248, 255)
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(8.5)
            p.font.bold = True if r_idx > 5 else False
            p.font.color.rgb = c_navy

        for c_idx, val in enumerate(vals, start=1):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if r_idx <= 5 else RGBColor(235, 248, 255)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(8.5)
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True if r_idx > 5 else False
                p.font.color.rgb = c_blue if r_idx > 5 else c_dark

    s7.notes_slide.notes_text_frame.text = (
        "Decision tables model complex boolean business logic. Here, our triage decision table takes three conditions: "
        "defect severity, environment, and whether it impacts a core transaction flow. Based on these combinations, "
        "it automatically calculates recommended SLA resolution times from 4 hours down to 120 hours."
    )

    # --------------------------------------------------------------------------
    # SLIDE 8: State Transition Testing (The Highlight)
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "State Transition Testing (STT)", "Active Enforcement of the ISTQB Defect Lifecycle")

    # Left: Defect Screenshot
    img_path2 = os.path.join(SCREENSHOTS_DIR, "08_defect_detail.png")
    if os.path.exists(img_path2):
        s8.shapes.add_picture(img_path2, Inches(0.8), Inches(1.8), width=Inches(6.6))

    # Right: State Machine rules
    add_card(s8, Inches(7.6), Inches(1.8), Inches(4.9), Inches(5.0))
    tb = s8.shapes.add_textbox(Inches(7.8), Inches(2.0), Inches(4.5), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Strict State Machine Rules"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    stt_rules = [
        "<b>Standard Path:</b> New &rarr; Assigned &rarr; Open &rarr; Fixed &rarr; Retest &rarr; Closed.",
        "<b>Rule 1 (No Direct Close):</b> A defect cannot jump directly from <code>New &rarr; Closed</code> or <code>Open &rarr; Closed</code>. Intercepted with HTTP 422 error.",
        "<b>Rule 2 (No Developer Closure):</b> Developers cannot close fixed defects directly. A QA engineer MUST re-test on a new build.",
        "<b>Rule 3 (Mandatory Notes):</b> Marking Fixed, Deferred, or Rejected strictly requires resolution comments.",
        "<b>Rule 4 (Reopen Loop):</b> If verification in Retest fails, status transitions to <code>Reopened</code>."
    ]
    for r in stt_rules:
        p = tf.add_paragraph()
        p.text = "• " + r.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "").replace("&rarr;", "->")
        p.font.size = Pt(9)
        p.font.color.rgb = c_dark
        p.space_before = Pt(8)

    s8.notes_slide.notes_text_frame.text = (
        "State Transition Testing is the centerpiece of our backend. In most student projects, defect status is just a dropdown "
        "allowing anyone to set any state. In TestFlow, the backend actively enforces the ISTQB Defect Lifecycle. "
        "An open defect cannot be closed directly; it must be fixed by dev, and verified in Retest by QA."
    )

    # --------------------------------------------------------------------------
    # SLIDE 9: Risk-Based Testing (RBT)
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Test Strategy & Prioritization", "Risk-Based Testing (RBT): The Shift-Left Principle")

    col_w = Inches(2.7)
    gap = Inches(0.25)
    start_x = Inches(0.8)
    top_y = Inches(1.8)
    card_h = Inches(5.0)

    rbt_tiers = [
        ("Critical Risk (16-25)", "Score = L(4-5) x I(4-5)", [
            "Payment gateway timeout",
            "Credit card authorization",
            "Zero open blockers exit rule",
            "Executed first in every run"
        ], c_red),
        ("High Risk (10-15)", "Score = L(2-3) x I(4-5)", [
            "User login authentication",
            "Cart line quantity limit",
            "Discount voucher logic",
            "Blocks staging promotion"
        ], RGBColor(221, 107, 32)),
        ("Medium Risk (5-9)", "Score = L(2-3) x I(2-3)", [
            "Quantity boundary formatting",
            "Secondary search filters",
            "Email notification trigger",
            "Addressed in normal sprint"
        ], c_blue),
        ("Low Risk (1-4)", "Score = L(1-2) x I(1-2)", [
            "Minor UI alignment",
            "Helper text readability",
            "Cosmetic padding",
            "Deferred if time-constrained"
        ], c_green)
    ]

    for i, (title, sub, items, col) in enumerate(rbt_tiers):
        x = start_x + i * (col_w + gap)
        add_card(s9, x, top_y, col_w, card_h)
        tb = s9.shapes.add_textbox(x + Inches(0.15), top_y + Inches(0.2), col_w - Inches(0.3), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(4)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(9)
            p.font.color.rgb = c_dark
            p.space_before = Pt(10)

    s9.notes_slide.notes_text_frame.text = (
        "Exhaustive testing is mathematically impossible. We implemented Risk-Based Testing using the Risk Priority Number formula: "
        "Likelihood times Impact. High-risk scenarios, such as credit card payment failures, are automatically prioritized "
        "and scheduled first during test execution cycles. This applies the Shift-Left principle to find critical bugs early."
    )

    # --------------------------------------------------------------------------
    # SLIDE 10: Requirements Traceability Matrix (RTM)
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Test Management & Governance", "Requirements Traceability Matrix (RTM): 100% Coverage")

    img_path3 = os.path.join(SCREENSHOTS_DIR, "09_rtm.png")
    if os.path.exists(img_path3):
        s10.shapes.add_picture(img_path3, Inches(0.8), Inches(1.8), width=Inches(6.8))

    add_card(s10, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.0))
    tb = s10.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Bi-Directional Traceability"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    rtm_bullets = [
        "<b>Forward Traceability:</b> Proves every Requirement maps forward to Test Cases, Executions, and Incidents.",
        "<b>Backward Traceability:</b> Verifies that every Test Case and Defect traces back to an approved Requirement.",
        "<b>Zero Coverage Gaps:</b> All 5 business requirements are 100% covered by test cases.",
        "<b>Zero Orphaned Tests:</b> No test case exists without an underlying requirement.",
        "<b>Audit & Export:</b> Printable view for stakeholder sign-off and compliance audits."
    ]
    for b in rtm_bullets:
        p = tf.add_paragraph()
        p.text = "• " + b.replace("<b>", "").replace("</b>", "")
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(10)

    s10.notes_slide.notes_text_frame.text = (
        "Here is our Requirements Traceability Matrix. Notice the progress meter at the top showing 100% coverage. "
        "More importantly, our automated gap detector confirms 0 orphaned test cases. Every single test exists solely "
        "to verify an approved business requirement."
    )

    # --------------------------------------------------------------------------
    # SLIDE 11: Automated Pytest Suite & 91% Coverage
    # --------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Quality Assurance & Automation", "Pytest Test Suite: 92 Automated Tests & 91% Coverage")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Test Automation Breakdown by ISTQB Marker"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    # Table of tests
    t_shape2 = s11.shapes.add_table(7, 5, Inches(1.0), Inches(2.6), Inches(11.3), Inches(3.8))
    t2 = t_shape2.table
    t2.columns[0].width = Inches(3.2)
    t2.columns[1].width = Inches(3.6)
    t2.columns[2].width = Inches(1.2)
    t2.columns[3].width = Inches(1.5)
    t2.columns[4].width = Inches(1.8)

    th2 = ["Test Suite File", "ISTQB Concept Verified", "Tests", "Statement Coverage", "Status"]
    for c, h in enumerate(th2):
        cell = t2.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.color.rgb = c_white

    suite_rows = [
        ("test_equivalence_partitioning.py", "Valid/invalid partitions on ratings, quantities, string limits", "19", "92%", "PASSED"),
        ("test_boundary_value_analysis.py", "2-value and 3-value boundary tests on cart quantities [1, 99]", "16", "92%", "PASSED"),
        ("test_decision_table.py", "Defect triage SLA priority rules & Release Gate decisions", "10", "92%", "PASSED"),
        ("test_state_transition.py", "Defect lifecycle state machine: valid paths & illegal rejection", "10", "92%", "PASSED"),
        ("test_risk_based_testing.py", "Risk Priority Number calculation & priority sorting", "5", "92%", "PASSED"),
        ("test_regression_suite.py", "End-to-End STLC regression cycle (Req -> TC -> Exec -> Bug)", "1", "98%", "PASSED"),
    ]
    for r_idx, row in enumerate(suite_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if r_idx % 2 == 1 else c_light_bg
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(8.5)
                p.font.bold = True if c_idx == 4 or c_idx == 0 else False
                p.font.color.rgb = c_green if c_idx == 4 else c_dark

    s11.notes_slide.notes_text_frame.text = (
        "In addition to manual testing, our automation suite contains 92 tests written with Pytest. "
        "Notice how our test files map directly to ISTQB techniques. Running pytest coverage gives us 91% code coverage "
        "across our entire application codebase with zero test failures."
    )

    # --------------------------------------------------------------------------
    # SLIDE 12: IEEE 829 Summary Report & Sign-Off
    # --------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Test Completion & Governance", "IEEE 829 Test Summary Report & Formal Sign-Off")

    img_path4 = os.path.join(SCREENSHOTS_DIR, "10_ieee829_report.png")
    if os.path.exists(img_path4):
        s12.shapes.add_picture(img_path4, Inches(0.8), Inches(1.8), width=Inches(6.8))

    add_card(s12, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.0))
    tb = s12.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "IEEE Std 829-2008 Compliance"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = c_navy

    report_bullets = [
        "<b>Standardized Reporting:</b> Follows IEEE 829-2008 Test Summary Report structure.",
        "<b>Executive Summary:</b> Formal release gate exit evaluation based on open blocker count and pass rate.",
        "<b>Residual Defect Analysis:</b> Full inventory of open defects with severity and workaround status.",
        "<b>Exit Decision:</b> NO-GO for Production until BUG-003 and BUG-001 are closed; Approved for Staging.",
        "<b>Formal Sign-Off Block:</b> Dual approvals from Lead QA Engineers Eya Khandoudi & Ichraf Sassi."
    ]
    for b in report_bullets:
        p = tf.add_paragraph()
        p.text = "• " + b.replace("<b>", "").replace("</b>", "")
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_before = Pt(10)

    s12.notes_slide.notes_text_frame.text = (
        "Our test completion process culminates in the IEEE 829 Test Summary Report. The report assesses all exit criteria, "
        "provides full visibility into residual risks, and includes the formal sign-off block approved by Eya and Ichraf."
    )

    # --------------------------------------------------------------------------
    # SLIDE 13: Conclusion & Q&A
    # --------------------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    bg13 = add_card(s13, Inches(0), Inches(0), Inches(13.333), Inches(7.5), bg_color=c_navy, border_color=c_navy)

    tbox = s13.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PROJECT CONCLUSION & DEMONSTRATION COMPLETE"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(144, 205, 244)

    p = tf.add_paragraph()
    p.text = "Thank You! We are Ready for Your Questions."
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.space_before = Pt(12)

    p = tf.add_paragraph()
    p.text = "Live Web App: http://127.0.0.1:5000  |  GitHub: https://github.com/eya-khandoudi/TestFlow-ISTQB"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(14)

    p = tf.add_paragraph()
    p.text = "Presenters & Lead QA: Eya Khandoudi & Ichraf Sassi  |  November 2026"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(254, 240, 138)
    p.space_before = Pt(25)

    s13.notes_slide.notes_text_frame.text = (
        "Thank you, Professor, for your time and attention. Ichraf and I are now ready to answer any questions "
        "or perform any live testing scenario you would like to see."
    )

    prs.save(PPTX_PATH)
    prs.save(ARTIFACT_PPTX_PATH)
    print(f"Generated PPTX: {PPTX_PATH} and {ARTIFACT_PPTX_PATH}")


# ==============================================================================
# 2. BUILD SLIDE DECK PDF PRESENTATION (LANDSCAPE A4)
# ==============================================================================
def create_pdf_presentation():
    # Landscape A4: 841.89 x 595.27 pt
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    navy = colors.HexColor("#0F2942")
    blue = colors.HexColor("#2B6CB0")
    dark_slate = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#E2E8F0")

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=navy,
        spaceAfter=4
    )

    slide_tag = ParagraphStyle(
        'SlideTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=blue,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=dark_slate,
        spaceAfter=4
    )

    table_header = ParagraphStyle(
        'TH', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white
    )
    table_cell = ParagraphStyle(
        'TC', fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=dark_slate
    )
    table_cell_bold = ParagraphStyle(
        'TCB', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=navy
    )

    story = []

    # Slide 1: Cover
    story.append(Spacer(1, 40))
    story.append(Paragraph("ISTQB CTFL v4.0 & IEEE Std 829-2008 Standard", ParagraphStyle('C1', fontName='Helvetica-Bold', fontSize=10, textColor=blue, alignment=1)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("TestFlow — Software Test Management System", ParagraphStyle('C2', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=navy, alignment=1)))
    story.append(Paragraph("Project Presentation & Defense: Formal Test Design Techniques, Automation & STLC Implementation", ParagraphStyle('C3', fontName='Helvetica', fontSize=12, leading=16, textColor=blue, alignment=1)))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="80%", thickness=2, color=blue, spaceAfter=20))
    story.append(Paragraph("<b>Presenters &amp; Lead QA:</b> Eya Khandoudi &amp; Ichraf Sassi", ParagraphStyle('C4', fontName='Helvetica-Bold', fontSize=13, textColor=navy, alignment=1)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Python 3.13 | Flask 3.1 | SQLite 3 | Pytest (92 Tests, 91% Coverage) | Bootstrap 5", ParagraphStyle('C5', fontName='Helvetica', fontSize=10, textColor=dark_slate, alignment=1)))
    story.append(Spacer(1, 30))
    story.append(Paragraph("November 2026", ParagraphStyle('C6', fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#718096"), alignment=1)))
    story.append(PageBreak())

    # Slide 2: Project Vision
    story.append(Paragraph("PROJECT CONTEXT &amp; PROBLEM STATEMENT", slide_tag))
    story.append(Paragraph("Beyond a Simple CRUD: An ISTQB Demonstration Platform", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=12))

    v_data = [
        [
            Paragraph("<b>The Problem in Academic QA Projects:</b><br/><br/>"
                      "&bull;&nbsp; Most student applications are basic CRUD apps with unstructured testing.<br/>"
                      "&bull;&nbsp; Testing techniques (EP, BVA, Decision Tables) are documented on paper but never enforced in code.<br/>"
                      "&bull;&nbsp; Defect tracking uses simple text dropdowns with zero state transition validation.<br/>"
                      "&bull;&nbsp; Requirements lack bi-directional traceability to executions and defect logs.", body_style),
            Paragraph("<b>TestFlow's Architectural Solution:</b><br/><br/>"
                      "&bull;&nbsp; <b>SUT Scope:</b> E-Commerce Checkout, Cart Boundaries, Voucher Rules &amp; Payments.<br/>"
                      "&bull;&nbsp; <b>Active Backend Enforcement:</b> Python state machines actively validate state rules.<br/>"
                      "&bull;&nbsp; <b>100% Traceability (RTM):</b> Reqs &harr; Test Cases &harr; Executions &harr; Defects.<br/>"
                      "&bull;&nbsp; <b>IEEE 829 Release Gate:</b> Real-time Decision Table exit evaluation.<br/>"
                      "&bull;&nbsp; <b>High Automation:</b> 92 automated tests with 91% statement coverage.", body_style)
        ]
    ]
    t_v = Table(v_data, colWidths=[380, 380])
    t_v.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), light_bg),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_v)
    story.append(PageBreak())

    # Slide 3: The 8 ISTQB Techniques
    story.append(Paragraph("METHODOLOGICAL FOUNDATION", slide_tag))
    story.append(Paragraph("8 Core ISTQB Techniques Directly Built Into TestFlow", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=12))

    tech_table_data = [
        [Paragraph("ISTQB Technique", table_header), Paragraph("Category", table_header), Paragraph("Application in TestFlow", table_header), Paragraph("Pytest Suite", table_header)],
        [Paragraph("<b>Equivalence Partitioning (EP)</b>", table_cell_bold), Paragraph("Specification (Black-box)", table_cell), Paragraph("Valid/invalid partitions on ratings, quantities, string limits", table_cell), Paragraph("<code>test_equivalence_partitioning.py</code>", table_cell)],
        [Paragraph("<b>Boundary Value Analysis (BVA)</b>", table_cell_bold), Paragraph("Specification (Black-box)", table_cell), Paragraph("2-value and 3-value boundary tests on cart quantities [1, 99]", table_cell), Paragraph("<code>test_boundary_value_analysis.py</code>", table_cell)],
        [Paragraph("<b>Decision Table Testing (DTT)</b>", table_cell_bold), Paragraph("Specification (Black-box)", table_cell), Paragraph("Defect triage SLA priority rules &amp; Release Gate decisions", table_cell), Paragraph("<code>test_decision_table.py</code>", table_cell)],
        [Paragraph("<b>State Transition Testing (STT)</b>", table_cell_bold), Paragraph("Specification (Black-box)", table_cell), Paragraph("Defect lifecycle state machine: valid paths &amp; illegal rejection", table_cell), Paragraph("<code>test_state_transition.py</code>", table_cell)],
        [Paragraph("<b>Risk-Based Testing (RBT)</b>", table_cell_bold), Paragraph("Strategy / Planning", table_cell), Paragraph("Risk Priority Number (RPN = L x I, 1-25) execution sorting", table_cell), Paragraph("<code>test_risk_based_testing.py</code>", table_cell)],
        [Paragraph("<b>Error Guessing (EG)</b>", table_cell_bold), Paragraph("Experience-based", table_cell), Paragraph("Resilience against SQLi payloads, XSS script tags, emojis", table_cell), Paragraph("<code>test_error_guessing.py</code>", table_cell)],
        [Paragraph("<b>Traceability Matrix (RTM)</b>", table_cell_bold), Paragraph("Test Management", table_cell), Paragraph("Bi-directional matrix: Requirements <-> Tests <-> Defects", table_cell), Paragraph("<code>/rtm</code> &amp; Regression", table_cell)],
        [Paragraph("<b>Regression Testing</b>", table_cell_bold), Paragraph("Test Execution", table_cell), Paragraph("Automated end-to-end SDLC/STLC cycle simulating bug resolution", table_cell), Paragraph("<code>test_regression_suite.py</code>", table_cell)],
    ]
    t_tech = Table(tech_table_data, colWidths=[150, 130, 310, 170])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_tech)
    story.append(PageBreak())

    # Slide 4: Live Dashboard
    story.append(Paragraph("SYSTEM DEMONSTRATION", slide_tag))
    story.append(Paragraph("QA Testing Dashboard &amp; Automated Release Gate", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=8))

    img1 = os.path.join(SCREENSHOTS_DIR, "01_dashboard.png")
    d_content = [
        Paragraph("<b>Key Dashboard Capabilities:</b><br/><br/>"
                  "&bull;&nbsp; <b>IEEE 829 Decision Table Release Gate:</b> Automatically calculates exit criteria (Zero open blockers, &ge;90% pass rate). Shows NO-GO banner.<br/><br/>"
                  "&bull;&nbsp; <b>Real-Time KPI Cards:</b> Requirements count, test cases, live pass rate, and blocker defect count.<br/><br/>"
                  "&bull;&nbsp; <b>Chart.js Visualizations:</b> Execution status doughnut chart and defect severity bar chart.<br/><br/>"
                  "&bull;&nbsp; <b>One-Click Execution:</b> Shortcuts to active test runs and recent defects.", body_style)
    ]
    if os.path.exists(img1):
        d_table = Table([[RLImage(img1, width=460, height=258), d_content]], colWidths=[470, 290])
    else:
        d_table = Table([[Paragraph("[Dashboard Image]", body_style), d_content]], colWidths=[470, 290])
    d_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(d_table)
    story.append(PageBreak())

    # Slide 5: STT State Machine
    story.append(Paragraph("STATE TRANSITION TESTING (STT)", slide_tag))
    story.append(Paragraph("Active Enforcement of the ISTQB Defect Lifecycle", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=8))

    img2 = os.path.join(SCREENSHOTS_DIR, "08_defect_detail.png")
    stt_content = [
        Paragraph("<b>State Machine Enforcement Rules:</b><br/><br/>"
                  "&bull;&nbsp; <b>Standard Path:</b> New &rarr; Assigned &rarr; Open &rarr; Fixed &rarr; Retest &rarr; Closed.<br/><br/>"
                  "&bull;&nbsp; <b>Rule STT-01 (No Direct Close):</b> Direct jumps (e.g. New &rarr; Closed or Open &rarr; Closed) are blocked by the backend with HTTP 422.<br/><br/>"
                  "&bull;&nbsp; <b>Rule STT-02 (No Developer Closure):</b> Developers cannot close Fixed bugs; QA must verify in Retest.<br/><br/>"
                  "&bull;&nbsp; <b>Rule STT-03 (Mandatory Notes):</b> Marking Fixed, Deferred, or Rejected requires resolution notes.<br/><br/>"
                  "&bull;&nbsp; <b>Rule STT-04 (Reopen Loop):</b> If verification in Retest fails, status transitions to Reopened.", body_style)
    ]
    if os.path.exists(img2):
        stt_table = Table([[RLImage(img2, width=460, height=258), stt_content]], colWidths=[470, 290])
    else:
        stt_table = Table([[Paragraph("[Defect Image]", body_style), stt_content]], colWidths=[470, 290])
    stt_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(stt_table)
    story.append(PageBreak())

    # Slide 6: Pytest Automation & Coverage
    story.append(Paragraph("AUTOMATION &amp; CODE QUALITY", slide_tag))
    story.append(Paragraph("Pytest Test Suite: 92 Automated Tests &amp; 91% Code Coverage", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=blue, spaceAfter=10))

    cov_rows = [
        [Paragraph("Module / Component", table_header), Paragraph("Statements", table_header), Paragraph("Missed", table_header), Paragraph("Coverage %", table_header), Paragraph("Verified Focus", table_header)],
        [Paragraph("<code>app/config.py</code>", table_cell_bold), Paragraph("12", table_cell), Paragraph("0", table_cell), Paragraph("100%", table_cell), Paragraph("Configuration &amp; database paths", table_cell)],
        [Paragraph("<code>app/services/report_service.py</code>", table_cell_bold), Paragraph("54", table_cell), Paragraph("1", table_cell), Paragraph("98%", table_cell), Paragraph("KPIs, RTM generator &amp; IEEE 829 summary", table_cell)],
        [Paragraph("<code>app/__init__.py</code>", table_cell_bold), Paragraph("43", table_cell), Paragraph("2", table_cell), Paragraph("95%", table_cell), Paragraph("App factory, Blueprints &amp; filters", table_cell)],
        [Paragraph("<code>app/database.py</code>", table_cell_bold), Paragraph("50", table_cell), Paragraph("3", table_cell), Paragraph("94%", table_cell), Paragraph("SQLite schema, foreign keys &amp; seed data", table_cell)],
        [Paragraph("<code>app/services/istqb_engine.py</code>", table_cell_bold), Paragraph("93", table_cell), Paragraph("7", table_cell), Paragraph("92%", table_cell), Paragraph("State machine, BVA/EP &amp; Decision tables", table_cell)],
        [Paragraph("<code>app/routes/main.py</code>", table_cell_bold), Paragraph("25", table_cell), Paragraph("1", table_cell), Paragraph("96%", table_cell), Paragraph("Dashboard, RTM &amp; Guide endpoints", table_cell)],
        [Paragraph("<code>app/routes/defects.py</code>", table_cell_bold), Paragraph("89", table_cell), Paragraph("9", table_cell), Paragraph("90%", table_cell), Paragraph("Incident logging &amp; state transitions", table_cell)],
        [Paragraph("<code>app/routes/test_runs.py</code>", table_cell_bold), Paragraph("58", table_cell), Paragraph("6", table_cell), Paragraph("90%", table_cell), Paragraph("Test run cycles &amp; inline logging", table_cell)],
        [Paragraph("<code>app/routes/test_cases.py</code>", table_cell_bold), Paragraph("114", table_cell), Paragraph("11", table_cell), Paragraph("90%", table_cell), Paragraph("Test case CRUD &amp; RBT sorter", table_cell)],
        [Paragraph("<b>TOTAL APPLICATION</b>", table_cell_bold), Paragraph("<b>710</b>", table_cell_bold), Paragraph("<b>62</b>", table_cell_bold), Paragraph("<b>91%</b>", table_cell_bold), Paragraph("<b>92 Tests Passing (0 Failures)</b>", table_cell_bold)],
    ]
    t_cov2 = Table(cov_rows, colWidths=[180, 70, 60, 80, 370])
    t_cov2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, light_bg]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#EDF2F7")),
    ]))
    story.append(t_cov2)
    story.append(PageBreak())

    # Slide 7: Conclusion
    story.append(Spacer(1, 50))
    story.append(Paragraph("PROJECT CONCLUSION", ParagraphStyle('EndTag', fontName='Helvetica-Bold', fontSize=10, textColor=blue, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Thank You! Ready for Demonstration &amp; Questions", ParagraphStyle('EndTitle', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=navy, alignment=1)))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="60%", thickness=2, color=blue, spaceAfter=20))
    story.append(Paragraph("<b>Presenters &amp; Lead QA:</b> Eya Khandoudi &amp; Ichraf Sassi", ParagraphStyle('EndAuth', fontName='Helvetica-Bold', fontSize=13, textColor=navy, alignment=1)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Live App: <b>http://127.0.0.1:5000</b> &nbsp;|&nbsp; GitHub: <b>https://github.com/eya-khandoudi/TestFlow-ISTQB</b>", ParagraphStyle('EndLinks', fontName='Helvetica', fontSize=10, textColor=dark_slate, alignment=1)))
    story.append(Spacer(1, 25))
    story.append(Paragraph("ISTQB CTFL v4.0 &amp; IEEE Std 829-2008 Standard  |  November 2026", ParagraphStyle('EndDate', fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#718096"), alignment=1)))

    doc.build(story)
    # Also save in artifact directory
    import shutil
    shutil.copyfile(PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"Generated Presentation PDF: {PDF_PATH} and {ARTIFACT_PDF_PATH}")


if __name__ == '__main__':
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    create_pptx()
    create_pdf_presentation()
    print("All presentations created successfully!")
