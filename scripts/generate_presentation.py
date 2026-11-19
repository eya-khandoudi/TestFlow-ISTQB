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
# 1. BUILD BEAUTIFUL, HIGH-READABILITY PPTX PRESENTATION
# ==============================================================================
def create_pptx():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Modern, high-contrast, professional
    c_navy = RGBColor(15, 30, 54)        # Deep executive navy
    c_blue = RGBColor(37, 99, 235)       # Vibrant tech blue (#2563EB)
    c_teal = RGBColor(13, 148, 136)      # Modern teal accent
    c_dark = RGBColor(15, 23, 42)        # Slate 900 for high-contrast reading
    c_muted = RGBColor(71, 85, 105)      # Slate 600 for subtitles
    c_card_bg = RGBColor(255, 255, 255)  # Pure crisp white for cards
    c_slide_bg = RGBColor(241, 245, 249) # Clean soft slate background
    c_border = RGBColor(203, 213, 225)   # Slate 300 crisp border
    c_white = RGBColor(255, 255, 255)
    c_green = RGBColor(22, 101, 52)      # Deep readable green
    c_red = RGBColor(185, 28, 28)        # Deep readable red
    c_gold = RGBColor(202, 138, 4)       # Gold highlight

    def set_slide_background(slide, color=c_slide_bg):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text):
        # Top banner with strong hierarchy
        box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.15))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        # Category Tag
        p1 = tf.paragraphs[0]
        p1.text = tag_text.upper()
        p1.font.name = "Arial"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = c_blue

        # Slide Main Title
        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.name = "Arial"
        p2.font.size = Pt(26)
        p2.font.bold = True
        p2.font.color.rgb = c_navy
        p2.space_before = Pt(4)

    def add_card(slide, left, top, width, height, bg_color=c_card_bg, border_color=c_border):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # --------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, c_navy)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.2), Inches(4.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = c_blue
    bar.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.8), Inches(5.0))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ISTQB & IEEE 829 SOFTWARE TESTING DEFENSE"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)

    p = tf.add_paragraph()
    p.text = "TestFlow — Software Test Management System"
    p.font.name = "Arial"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.space_before = Pt(14)

    p = tf.add_paragraph()
    p.text = "End-to-End STLC Demonstration, Formal Test Design Techniques, Automation & Quality Evaluation"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(14)

    p = tf.add_paragraph()
    p.text = "Lead QA Engineers & Authors:  Eya Khandoudi & Ichraf Sassi"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(253, 224, 71) # Vibrant readable yellow
    p.space_before = Pt(28)

    p = tf.add_paragraph()
    p.text = "Standards: ISTQB CTFL v4.0 & IEEE Std 829-2008  |  92 Tests (91% Coverage)  |  November 2026"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_before = Pt(8)

    s1.notes_slide.notes_text_frame.text = (
        "Welcome everyone. Today, Ichraf and I are presenting TestFlow, an end-to-end software test management system "
        "specifically designed to demonstrate rigorous software testing methodologies throughout the SDLC and STLC."
    )

    # --------------------------------------------------------------------------
    # SLIDE 2: Project Vision & The Core Difference
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Project Overview & Engineering Goals", "Beyond a Simple CRUD: An ISTQB Demonstration Platform")

    # Card 1: The Problem
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1))
    tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "The Flaw in Typical QA Projects"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = c_red

    bullets1 = [
        ("Passive Documentation Only", "EP, BVA, and Decision Tables are written in Word reports but never enforced in code."),
        ("No Lifecycle Validation", "Defect status is just an unvalidated dropdown allowing impossible jumps like New -> Closed."),
        ("Zero Traceability", "Requirements lack automated forward/backward links to test executions and open bugs.")
    ]
    for title, desc in bullets1:
        p = tf1.add_paragraph()
        p.text = "• " + title + ":"
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = c_dark
        p.space_before = Pt(14)
        p2 = tf1.add_paragraph()
        p2.text = "   " + desc
        p2.font.size = Pt(13.5)
        p2.font.color.rgb = c_muted

    # Card 2: TestFlow Solution
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    tb2 = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "The TestFlow Engineering Solution"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = c_green

    bullets2 = [
        ("Active Backend Enforcement", "Python algorithms strictly validate boundary limits and calculate SLA triage rules."),
        ("State Machine Governance", "Defects must follow ISTQB transitions: New -> Assigned -> Open -> Fixed -> Retest -> Closed."),
        ("100% Traceability (RTM)", "Automated matrix guarantees 0 orphaned tests and complete coverage from spec to bug.")
    ]
    for title, desc in bullets2:
        p = tf2.add_paragraph()
        p.text = "• " + title + ":"
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = c_dark
        p.space_before = Pt(14)
        p2 = tf2.add_paragraph()
        p2.text = "   " + desc
        p2.font.size = Pt(13.5)
        p2.font.color.rgb = c_muted

    s2.notes_slide.notes_text_frame.text = (
        "In many software engineering projects, testing is an afterthought. We wanted to build TestFlow to prove that "
        "professional testing techniques can be directly embedded into software architecture."
    )

    # --------------------------------------------------------------------------
    # SLIDE 3: System Architecture & Tech Stack
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Architecture & Technology Stack", "Modular, Robust Python Full-Stack Implementation")

    col_w = Inches(2.7)
    gap = Inches(0.25)
    start_x = Inches(0.8)
    top_y = Inches(1.8)
    card_h = Inches(5.1)

    techs = [
        ("Backend Tier", "Python 3.13 & Flask", [
            "Application Factory pattern",
            "6 Modular Blueprints",
            "REST API automation",
            "Live ISTQB calculations"
        ], c_blue),
        ("Database Tier", "SQLite 3 Relational", [
            "Atomic ACID compliance",
            "Foreign key constraints",
            "Virtual generated columns",
            "Chronological audit trails"
        ], c_teal),
        ("Testing Harness", "Pytest 9.2 & Cov", [
            "92 Automated test cases",
            "Custom ISTQB markers",
            "91% statement coverage",
            "100% pass verification"
        ], c_green),
        ("Frontend & UI", "Bootstrap 5 & JS", [
            "Responsive clean layout",
            "Chart.js live visualizations",
            "Dynamic RBT risk slider",
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
        p.font.size = Pt(18)
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = c_dark
        p.space_before = Pt(6)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(13)
            p.font.color.rgb = c_muted
            p.space_before = Pt(14)

    s3.notes_slide.notes_text_frame.text = (
        "TestFlow uses a clean, decoupled architecture. The backend is written in Python 3.13 using Flask with Blueprints. "
        "The relational database is SQLite with strict foreign key integrity."
    )

    # --------------------------------------------------------------------------
    # SLIDE 4: The 8 ISTQB Methodologies Implemented
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Core Testing Methodologies", "8 Formal ISTQB Techniques Directly Built Into TestFlow")

    grid_items = [
        ("Equivalence Partitioning (EP)", "Valid & invalid partitions for ratings, quantities, and emails.", c_blue),
        ("Boundary Value Analysis (BVA)", "2-value & 3-value boundary tests triggering real bugs at 0 and 100.", c_green),
        ("Decision Table Testing (DTT)", "Combinatorial truth tables for Defect SLA Triage & Release Gate.", c_teal),
        ("State Transition Testing (STT)", "Defect Lifecycle state machine blocking illegal state jumps.", c_red),
        ("Risk-Based Testing (RBT)", "Formula: RPN = Likelihood x Impact. High-risk tests run first.", c_navy),
        ("Error Guessing (EG)", "Resilience against SQLi payloads, XSS tags, and orphan foreign keys.", c_blue),
        ("Traceability Matrix (RTM)", "Bi-directional matrix linking Requirements <-> Tests <-> Defects.", c_teal),
        ("Regression Testing", "Automated end-to-end SDLC/STLC cycle ensuring patches don't break code.", c_green)
    ]

    gw = Inches(5.65)
    gh = Inches(1.15)
    for i, (title, desc, col) in enumerate(grid_items):
        r = i // 2
        c = i % 2
        x = Inches(0.8) + c * Inches(6.08)
        y = Inches(1.8) + r * Inches(1.3)
        add_card(s4, x, y, gw, gh)
        tb = s4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), gw - Inches(0.4), gh - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(13)
        p.font.color.rgb = c_dark
        p.space_before = Pt(3)

    s4.notes_slide.notes_text_frame.text = (
        "Here you see the 8 formal ISTQB techniques we implemented. Each technique is backed by dedicated Python algorithms "
        "in our domain engine and verified by automated Pytest test suites."
    )

    # --------------------------------------------------------------------------
    # SLIDE 5: Live UI — Dashboard & Release Gate
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "System Walkthrough: Dashboard", "Real-Time Quality Health & Automated IEEE 829 Release Gate")

    # Left: Screenshot
    img_path1 = os.path.join(SCREENSHOTS_DIR, "01_dashboard.png")
    if os.path.exists(img_path1):
        s5.shapes.add_picture(img_path1, Inches(0.8), Inches(1.8), width=Inches(6.8))

    # Right: High Readability Card
    add_card(s5, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1))
    tb = s5.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Operational Features"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = c_navy

    features = [
        ("Automated Release Gate", "Decision Table evaluates open blockers and pass rate. Shows NO-GO due to 2 blockers."),
        ("Real-Time KPI Cards", "Live counters for Requirements, Test Cases, Pass Rate, and Open Blockers."),
        ("Chart.js Visualizations", "Execution Doughnut (Pass/Fail/Blocked) and Defect Severity breakdown."),
        ("One-Click Access", "Direct links to active test cycles and recent defect incident reports.")
    ]
    for heading, detail in features:
        p = tf.add_paragraph()
        p.text = "• " + heading + ":"
        p.font.bold = True
        p.font.size = Pt(15)
        p.font.color.rgb = c_blue
        p.space_before = Pt(12)
        p2 = tf.add_paragraph()
        p2.text = "   " + detail
        p2.font.size = Pt(13)
        p2.font.color.rgb = c_dark

    s5.notes_slide.notes_text_frame.text = (
        "This is our main dashboard. Notice the red banner at the top showing our IEEE 829 Release Gate Decision. "
        "Because we have 2 open blocker defects, the decision table automatically sets the verdict to NO-GO."
    )

    # --------------------------------------------------------------------------
    # SLIDE 6: BVA & Equivalence Partitioning
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Specification-Based Testing", "Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)")

    # Left: Cart quantity BVA table
    add_card(s6, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.1))
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Cart Quantity Boundaries [1, 99]"
    p.font.bold = True
    p.font.size = Pt(19)
    p.font.color.rgb = c_navy

    bva_bullets = [
        ("Qty = 0 (Min - 1)", "Invalid Boundary -> Throws 500 error (Logged BUG-001)", c_red),
        ("Qty = 1 (Min)", "Valid Boundary -> Accepted correctly (TC-BVA-003)", c_green),
        ("Qty = 2 (Min + 1)", "Valid 3-Value Point -> Accepted correctly", c_dark),
        ("Qty = 98 (Max - 1)", "Valid 3-Value Point -> Accepted correctly", c_dark),
        ("Qty = 99 (Max)", "Valid Boundary -> Maximum allowable items (TC-BVA-005)", c_green),
        ("Qty = 100 (Max + 1)", "Invalid Boundary -> Accepted 100 units! (Logged BUG-002)", c_red)
    ]
    for boundary, outcome, col in bva_bullets:
        p = tf.add_paragraph()
        p.text = "• " + boundary + ":"
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = col
        p.space_before = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = "   " + outcome
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = c_dark

    # Right: EP Applied
    add_card(s6, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.1))
    tb2 = s6.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Equivalence Partitioning (EP)"
    p.font.bold = True
    p.font.size = Pt(19)
    p.font.color.rgb = c_navy

    ep_bullets = [
        ("User Email Format", "Valid (user@domain.com) vs Invalid (missing @, invalid domain). Verified in TC-EP-001 & 002."),
        ("Risk Likelihood [1, 5]", "Valid [1-5] vs Invalid (<1, >5, non-numeric). Enforced on forms and API."),
        ("Text Field Lengths", "Strict limits on Code [3, 20] and Title [5, 200] characters."),
        ("Backend Algorithms", "Programmed in istqb_engine.py & verified by 35 automated Pytest tests.")
    ]
    for title, desc in ep_bullets:
        p = tf2.add_paragraph()
        p.text = "• " + title + ":"
        p.font.bold = True
        p.font.size = Pt(14.5)
        p.font.color.rgb = c_blue
        p.space_before = Pt(10)
        p2 = tf2.add_paragraph()
        p2.text = "   " + desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = c_dark

    s6.notes_slide.notes_text_frame.text = (
        "Here we demonstrate 2-value and 3-value Boundary Value Analysis. Notice that our boundary testing actually uncovered "
        "two real defects: BUG-001 at 0 items, and BUG-002 at 100 items. This proves the ISTQB principle that defects cluster at boundaries."
    )

    # --------------------------------------------------------------------------
    # SLIDE 7: Decision Table Testing
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Combinatorial Testing", "Decision Table Testing (DTT): Defect SLA & Release Rules")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Defect SLA Triage Decision Table"
    p.font.bold = True
    p.font.size = Pt(19)
    p.font.color.rgb = c_navy

    p = tf.add_paragraph()
    p.text = "Evaluates multi-condition inputs to automatically assign SLA resolution targets and escalation flags:"
    p.font.size = Pt(14)
    p.font.color.rgb = c_muted
    p.space_before = Pt(4)

    # Table with larger readable fonts
    rows, cols = 8, 7
    t_shape = s7.shapes.add_table(rows, cols, Inches(1.0), Inches(2.8), Inches(11.333), Inches(3.8))
    t = t_shape.table
    t.columns[0].width = Inches(3.533)
    for c in range(1, 7):
        t.columns[c].width = Inches(1.3)

    headers = ["Condition / Action", "Rule 1", "Rule 2", "Rule 3", "Rule 4", "Rule 5", "Rule 6"]
    for c, h in enumerate(headers):
        cell = t.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = c_white
            p.alignment = PP_ALIGN.CENTER if c > 0 else PP_ALIGN.LEFT

    table_rows = [
        ("Severity in {Blocker, Critical}", ["True", "True", "True", "False", "False", "False"]),
        ("Environment == 'Production'", ["True", "False", "False", "*", "*", "*"]),
        ("Affects Core Flow (Checkout/Auth)", ["*", "True", "False", "True", "False", "*"]),
        ("Severity == 'Major'", ["False", "False", "False", "True", "True", "False"]),
        ("Severity == 'Minor'", ["False", "False", "False", "False", "False", "True"]),
        ("OUTPUT: Priority SLA", ["Urgent", "Urgent", "High", "High", "Medium", "Low"]),
        ("OUTPUT: Max SLA Hours", ["4 Hours", "8 Hours", "16 Hours", "24 Hours", "48 Hours", "120 Hours"]),
    ]

    for r_idx, (cond, vals) in enumerate(table_rows, start=1):
        cell = t.cell(r_idx, 0)
        cell.text = cond
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_slide_bg if r_idx <= 5 else RGBColor(239, 246, 255)
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(12.5)
            p.font.bold = True if r_idx > 5 else False
            p.font.color.rgb = c_navy

        for c_idx, val in enumerate(vals, start=1):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if r_idx <= 5 else RGBColor(239, 246, 255)
            for p in cell.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(12)
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True if r_idx > 5 else False
                p.font.color.rgb = c_blue if r_idx > 5 else c_dark

    s7.notes_slide.notes_text_frame.text = (
        "Decision tables model complex boolean business logic. Here, our triage decision table takes defect severity, "
        "environment, and core flow impact to calculate SLA targets from 4 hours up to 120 hours."
    )

    # --------------------------------------------------------------------------
    # SLIDE 8: State Transition Testing (The Highlight)
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "State Transition Testing (STT)", "Active Enforcement of the ISTQB Defect Lifecycle")

    # Left: Defect Screenshot
    img_path2 = os.path.join(SCREENSHOTS_DIR, "08_defect_detail.png")
    if os.path.exists(img_path2):
        s8.shapes.add_picture(img_path2, Inches(0.8), Inches(1.8), width=Inches(6.6))

    # Right: State Machine rules
    add_card(s8, Inches(7.6), Inches(1.8), Inches(4.9), Inches(5.1))
    tb = s8.shapes.add_textbox(Inches(7.8), Inches(2.0), Inches(4.5), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Strict State Machine Rules"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = c_navy

    stt_rules = [
        ("Standard Lifecycle", "New -> Assigned -> Open -> Fixed -> Retest -> Closed."),
        ("No Direct Close (STT-01)", "Defects CANNOT jump from New -> Closed or Open -> Closed (Blocked with HTTP 422)."),
        ("No Dev Self-Close (STT-02)", "Developers cannot close Fixed bugs; only QA retesting can verify and close."),
        ("Mandatory Notes (STT-03)", "Marking Fixed, Deferred, or Rejected strictly requires resolution comments."),
        ("Reopen Loop (STT-04)", "Failed verification in Retest automatically transitions to Reopened.")
    ]
    for title, desc in stt_rules:
        p = tf.add_paragraph()
        p.text = "• " + title + ":"
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = c_red if "No" in title else c_blue
        p.space_before = Pt(10)
        p2 = tf.add_paragraph()
        p2.text = "   " + desc
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = c_dark

    s8.notes_slide.notes_text_frame.text = (
        "State Transition Testing is the centerpiece of our project. In TestFlow, the backend actively enforces "
        "the ISTQB Defect Lifecycle. An open defect cannot be closed directly; it must be fixed by dev, and verified in Retest by QA."
    )

    # --------------------------------------------------------------------------
    # SLIDE 9: Risk-Based Testing (RBT)
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Test Strategy & Prioritization", "Risk-Based Testing (RBT): The Shift-Left Principle")

    col_w = Inches(2.7)
    gap = Inches(0.25)
    start_x = Inches(0.8)
    top_y = Inches(1.8)
    card_h = Inches(5.1)

    rbt_tiers = [
        ("Critical (16-25)", "Score = L(4-5) x I(4-5)", [
            "Payment timeouts",
            "Credit card failures",
            "Zero open blockers exit rule",
            "Executed first in runs"
        ], c_red),
        ("High (10-15)", "Score = L(2-3) x I(4-5)", [
            "User authentication",
            "Cart quantity limits",
            "Discount voucher rules",
            "Blocks staging promotion"
        ], RGBColor(194, 65, 12)),
        ("Medium (5-9)", "Score = L(2-3) x I(2-3)", [
            "Boundary formatting",
            "Search query filters",
            "Email notifications",
            "Standard sprint cycle"
        ], c_blue),
        ("Low (1-4)", "Score = L(1-2) x I(1-2)", [
            "UI alignment gaps",
            "Helper copy styling",
            "Cosmetic padding",
            "Deferred if constrained"
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
        p.font.size = Pt(17)
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = c_dark
        p.space_before = Pt(6)

        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.size = Pt(12.5)
            p.font.color.rgb = c_muted
            p.space_before = Pt(14)

    s9.notes_slide.notes_text_frame.text = (
        "Exhaustive testing is impossible. We implemented Risk-Based Testing using RPN = Likelihood times Impact. "
        "High-risk scenarios, such as credit card payment failures, are automatically scheduled first during test execution."
    )

    # --------------------------------------------------------------------------
    # SLIDE 10: Requirements Traceability Matrix (RTM)
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Test Management & Governance", "Requirements Traceability Matrix (RTM): 100% Coverage")

    img_path3 = os.path.join(SCREENSHOTS_DIR, "09_rtm.png")
    if os.path.exists(img_path3):
        s10.shapes.add_picture(img_path3, Inches(0.8), Inches(1.8), width=Inches(6.8))

    add_card(s10, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1))
    tb = s10.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Traceability Governance"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = c_navy

    rtm_bullets = [
        ("Forward Traceability", "Every Requirement maps forward to Test Cases, Executions, and Defect Reports."),
        ("Backward Traceability", "Every Test Case and Defect traces back to an approved business requirement."),
        ("Zero Coverage Gaps", "100% of functional requirements have linked test coverage."),
        ("Zero Orphaned Tests", "No tests exist without a corresponding approved requirement."),
        ("Stakeholder Audits", "Printable and exportable report for governance sign-off.")
    ]
    for title, desc in rtm_bullets:
        p = tf.add_paragraph()
        p.text = "• " + title + ":"
        p.font.bold = True
        p.font.size = Pt(14.5)
        p.font.color.rgb = c_blue
        p.space_before = Pt(10)
        p2 = tf.add_paragraph()
        p2.text = "   " + desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = c_dark

    s10.notes_slide.notes_text_frame.text = (
        "Here is our Requirements Traceability Matrix. Notice the progress meter at the top showing 100% coverage. "
        "Our automated gap detector confirms 0 orphaned test cases."
    )

    # --------------------------------------------------------------------------
    # SLIDE 11: Automated Pytest Suite & 91% Coverage
    # --------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Quality Assurance & Automation", "Pytest Test Suite: 92 Automated Tests & 91% Coverage")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.1))
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Test Automation Breakdown by ISTQB Marker"
    p.font.bold = True
    p.font.size = Pt(19)
    p.font.color.rgb = c_navy

    # Table of tests with larger fonts
    t_shape2 = s11.shapes.add_table(7, 5, Inches(1.0), Inches(2.6), Inches(11.333), Inches(4.0))
    t2 = t_shape2.table
    t2.columns[0].width = Inches(3.2)
    t2.columns[1].width = Inches(3.833)
    t2.columns[2].width = Inches(1.1)
    t2.columns[3].width = Inches(1.4)
    t2.columns[4].width = Inches(1.8)

    th2 = ["Test Suite File", "ISTQB Concept Verified", "Tests", "Statement Cov.", "Status"]
    for c, h in enumerate(th2):
        cell = t2.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        for p in cell.text_frame.paragraphs:
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = c_white
            p.alignment = PP_ALIGN.CENTER if c >= 2 else PP_ALIGN.LEFT

    suite_rows = [
        ("test_equivalence_partitioning.py", "Valid/invalid partitions on ratings, quantities, limits", "19", "92%", "PASSED"),
        ("test_boundary_value_analysis.py", "2-value & 3-value boundary tests on cart quantities [1, 99]", "16", "92%", "PASSED"),
        ("test_decision_table.py", "Defect SLA triage priority rules & Release Gate decisions", "10", "92%", "PASSED"),
        ("test_state_transition.py", "Defect lifecycle state machine: valid paths & illegal rejection", "10", "92%", "PASSED"),
        ("test_risk_based_testing.py", "Risk Priority Number calculation & priority sorting", "5", "92%", "PASSED"),
        ("test_regression_suite.py", "End-to-End STLC regression cycle (Req -> TC -> Exec -> Bug)", "1", "98%", "PASSED"),
    ]
    for r_idx, row in enumerate(suite_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if r_idx % 2 == 1 else c_slide_bg
            for p in cell.text_frame.paragraphs:
                p.font.name = "Arial"
                p.font.size = Pt(12)
                p.font.bold = True if c_idx == 4 or c_idx == 0 else False
                p.font.color.rgb = c_green if c_idx == 4 else c_dark
                p.alignment = PP_ALIGN.CENTER if c_idx >= 2 else PP_ALIGN.LEFT

    s11.notes_slide.notes_text_frame.text = (
        "In addition to manual testing, our automation suite contains 92 tests written with Pytest. "
        "Running pytest coverage gives us 91% code coverage across our entire application codebase with zero test failures."
    )

    # --------------------------------------------------------------------------
    # SLIDE 12: IEEE 829 Summary Report & Sign-Off
    # --------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Test Completion & Governance", "IEEE 829 Test Summary Report & Formal Sign-Off")

    img_path4 = os.path.join(SCREENSHOTS_DIR, "10_ieee829_report.png")
    if os.path.exists(img_path4):
        s12.shapes.add_picture(img_path4, Inches(0.8), Inches(1.8), width=Inches(6.8))

    add_card(s12, Inches(7.8), Inches(1.8), Inches(4.7), Inches(5.1))
    tb = s12.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "IEEE Std 829-2008 Report"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = c_navy

    report_bullets = [
        ("Standard Compliance", "Strictly follows IEEE 829-2008 Test Summary Report structure."),
        ("Executive Summary", "Formal exit criteria evaluation based on blockers and pass rate."),
        ("Residual Risk Log", "Full inventory of open defects with severity and workaround status."),
        ("Release Verdict", "NO-GO for Production until BUG-001/003 are resolved; Approved for Staging."),
        ("Official Sign-Off", "Dual approvals from Lead QA Engineers Eya Khandoudi & Ichraf Sassi.")
    ]
    for title, desc in report_bullets:
        p = tf.add_paragraph()
        p.text = "• " + title + ":"
        p.font.bold = True
        p.font.size = Pt(14.5)
        p.font.color.rgb = c_blue
        p.space_before = Pt(10)
        p2 = tf.add_paragraph()
        p2.text = "   " + desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = c_dark

    s12.notes_slide.notes_text_frame.text = (
        "Our test completion process culminates in the IEEE 829 Test Summary Report. The report assesses all exit criteria "
        "and includes the formal sign-off block approved by Eya and Ichraf."
    )

    # --------------------------------------------------------------------------
    # SLIDE 13: Conclusion & Q&A
    # --------------------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, c_navy)

    # Accent decorative bar
    bar13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.4), Inches(0.2), Inches(4.6))
    bar13.fill.solid()
    bar13.fill.fore_color.rgb = c_blue
    bar13.line.fill.background()

    tbox = s13.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.8), Inches(4.6))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PROJECT DEMONSTRATION COMPLETE"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)

    p = tf.add_paragraph()
    p.text = "Thank You! We Are Ready for Your Questions."
    p.font.name = "Arial"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.space_before = Pt(14)

    p = tf.add_paragraph()
    p.text = "Live Web Application: http://127.0.0.1:5000\nGitHub Repository: https://github.com/eya-khandoudi/TestFlow-ISTQB"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_before = Pt(16)

    p = tf.add_paragraph()
    p.text = "Lead QA Presenters: Eya Khandoudi & Ichraf Sassi  |  November 2026"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(253, 224, 71)
    p.space_before = Pt(24)

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
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    navy = colors.HexColor("#0F1E36")
    blue = colors.HexColor("#2563EB")
    dark_slate = colors.HexColor("#0F172A")
    light_bg = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E0")

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=navy,
        spaceAfter=6
    )

    slide_tag = ParagraphStyle(
        'SlideTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=blue,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=dark_slate,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'SlideBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=navy
    )

    table_header = ParagraphStyle(
        'TH', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.white
    )
    table_cell = ParagraphStyle(
        'TC', fontName='Helvetica', fontSize=9, leading=11.5, textColor=dark_slate
    )
    table_cell_bold = ParagraphStyle(
        'TCB', fontName='Helvetica-Bold', fontSize=9, leading=11.5, textColor=navy
    )

    story = []

    # Slide 1: Cover
    story.append(Spacer(1, 40))
    story.append(Paragraph("ISTQB &amp; IEEE 829 SOFTWARE TESTING DEFENSE", slide_tag))
    story.append(Paragraph("TestFlow — Software Test Management System", ParagraphStyle('T1', fontName='Helvetica-Bold', fontSize=28, leading=34, textColor=navy)))
    story.append(Paragraph("Comprehensive STLC Demonstration, Formal Test Design Techniques, Automation &amp; Quality Evaluation", ParagraphStyle('T2', fontName='Helvetica', fontSize=14, leading=18, textColor=blue)))
    story.append(HRFlowable(width="100%", thickness=2, color=blue, spaceBefore=10, spaceAfter=20))
    story.append(Paragraph("<b>Presenters &amp; Lead QA:</b> Eya Khandoudi &amp; Ichraf Sassi &nbsp;|&nbsp; <b>Standards:</b> ISTQB CTFL v4.0 &amp; IEEE Std 829-2008", body_bold))
    story.append(Paragraph("<b>Test Suite:</b> 92 Automated Tests (All Passed, 91% Coverage) &nbsp;|&nbsp; <b>Live App:</b> http://127.0.0.1:5000", body_style))
    story.append(PageBreak())

    # Slide 2: Vision
    story.append(Paragraph("PROJECT OVERVIEW &amp; SCOPE", slide_tag))
    story.append(Paragraph("Beyond a Simple CRUD: An ISTQB Demonstration Platform", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=14))
    
    s2_data = [
        [
            Paragraph("<b>The Flaw in Typical QA Projects</b><br/><br/>"
                      "&bull; <b>Passive Documentation:</b> EP and BVA are written in Word reports but never enforced in code.<br/><br/>"
                      "&bull; <b>No Lifecycle Validation:</b> Defect status is an unvalidated dropdown allowing illegal jumps.<br/><br/>"
                      "&bull; <b>Zero Traceability:</b> Requirements lack links to executions and open bugs.", body_style),
            Paragraph("<b>The TestFlow Engineering Solution</b><br/><br/>"
                      "&bull; <b>Active Backend Enforcement:</b> Algorithms validate boundaries and calculate SLA triage.<br/><br/>"
                      "&bull; <b>State Machine Governance:</b> Enforces New &rarr; Assigned &rarr; Open &rarr; Fixed &rarr; Retest &rarr; Closed.<br/><br/>"
                      "&bull; <b>100% Traceability (RTM):</b> Full forward/backward traceability with zero orphaned tests.", body_style)
        ]
    ]
    t_s2 = Table(s2_data, colWidths=[380, 380])
    t_s2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), light_bg),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_s2)
    story.append(PageBreak())

    # Slide 3: Tech Stack
    story.append(Paragraph("ARCHITECTURE &amp; TECHNOLOGY STACK", slide_tag))
    story.append(Paragraph("Modular, Robust Python Full-Stack Implementation", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=14))

    s3_data = [
        [Paragraph("<b>Backend Tier</b>", table_header), Paragraph("<b>Database Tier</b>", table_header), Paragraph("<b>Testing Harness</b>", table_header), Paragraph("<b>Frontend &amp; UI</b>", table_header)],
        [
            Paragraph("<b>Python 3.13 &amp; Flask</b><br/><br/>&bull; Factory Pattern<br/>&bull; 6 Blueprints<br/>&bull; REST API endpoints<br/>&bull; Real-time calculations", table_cell),
            Paragraph("<b>SQLite 3 Relational</b><br/><br/>&bull; Atomic transactions<br/>&bull; Foreign key rules<br/>&bull; Generated columns<br/>&bull; Audit history logs", table_cell),
            Paragraph("<b>Pytest 9.2 &amp; Cov</b><br/><br/>&bull; 92 Automated tests<br/>&bull; ISTQB markers<br/>&bull; 91% code coverage<br/>&bull; All passed", table_cell),
            Paragraph("<b>Bootstrap 5 &amp; JS</b><br/><br/>&bull; Responsive UI<br/>&bull; Chart.js charts<br/>&bull; Dynamic risk slider<br/>&bull; Selenium headless", table_cell),
        ]
    ]
    t_s3 = Table(s3_data, colWidths=[190, 190, 190, 190])
    t_s3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white]),
    ]))
    story.append(t_s3)
    story.append(PageBreak())

    # Slide 4: 8 ISTQB Techniques
    story.append(Paragraph("CORE TESTING METHODOLOGIES", slide_tag))
    story.append(Paragraph("8 Formal ISTQB Techniques Directly Built Into TestFlow", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=14))

    s4_data = [
        [
            Paragraph("<b>1. Equivalence Partitioning (EP):</b> Valid &amp; invalid partitions for ratings, quantities, and emails.", body_style),
            Paragraph("<b>2. Boundary Value Analysis (BVA):</b> 2-value &amp; 3-value boundary tests on cart quantities [1, 99].", body_style)
        ],
        [
            Paragraph("<b>3. Decision Table Testing (DTT):</b> Combinatorial truth tables for Defect SLA Triage &amp; Release Gate.", body_style),
            Paragraph("<b>4. State Transition Testing (STT):</b> Defect Lifecycle state machine blocking illegal state jumps.", body_style)
        ],
        [
            Paragraph("<b>5. Risk-Based Testing (RBT):</b> Formula: RPN = Likelihood x Impact. High-risk tests run first.", body_style),
            Paragraph("<b>6. Error Guessing (EG):</b> Resilience against SQLi payloads, XSS tags, and orphan foreign keys.", body_style)
        ],
        [
            Paragraph("<b>7. Traceability Matrix (RTM):</b> Bi-directional matrix linking Requirements &harr; Tests &harr; Defects.", body_style),
            Paragraph("<b>8. Regression Testing:</b> Automated end-to-end SDLC/STLC cycle ensuring patches don't break code.", body_style)
        ]
    ]
    t_s4 = Table(s4_data, colWidths=[380, 380])
    t_s4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_s4)
    story.append(PageBreak())

    # Slide 5: Pytest Breakdown Table
    story.append(Paragraph("QUALITY ASSURANCE &amp; AUTOMATION", slide_tag))
    story.append(Paragraph("Pytest Test Suite: 92 Automated Tests &amp; 91% Coverage", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceAfter=14))

    s11_data = [
        [Paragraph("<b>Test Suite File</b>", table_header), Paragraph("<b>ISTQB Concept Verified</b>", table_header), Paragraph("<b>Tests</b>", table_header), Paragraph("<b>Statement Cov.</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [Paragraph("<code>test_equivalence_partitioning.py</code>", table_cell_bold), Paragraph("Valid/invalid partitions on ratings, quantities, limits", table_cell), Paragraph("19", table_cell), Paragraph("92%", table_cell), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", table_cell)],
        [Paragraph("<code>test_boundary_value_analysis.py</code>", table_cell_bold), Paragraph("2-value &amp; 3-value boundary tests on cart quantities [1, 99]", table_cell), Paragraph("16", table_cell), Paragraph("92%", table_cell), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", table_cell)],
        [Paragraph("<code>test_decision_table.py</code>", table_cell_bold), Paragraph("Defect SLA triage priority rules &amp; Release Gate decisions", table_cell), Paragraph("10", table_cell), Paragraph("92%", table_cell), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", table_cell)],
        [Paragraph("<code>test_state_transition.py</code>", table_cell_bold), Paragraph("Defect lifecycle state machine: valid paths &amp; illegal rejection", table_cell), Paragraph("10", table_cell), Paragraph("92%", table_cell), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", table_cell)],
        [Paragraph("<code>test_risk_based_testing.py</code>", table_cell_bold), Paragraph("Risk Priority Number calculation &amp; priority sorting", table_cell), Paragraph("5", table_cell), Paragraph("92%", table_cell), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", table_cell)],
        [Paragraph("<code>test_regression_suite.py</code>", table_cell_bold), Paragraph("End-to-End STLC regression cycle (Req -> TC -> Exec -> Bug)", table_cell), Paragraph("1", table_cell), Paragraph("98%", table_cell), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", table_cell)],
    ]
    t_s11 = Table(s11_data, colWidths=[200, 290, 70, 100, 100])
    t_s11.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_s11)
    story.append(PageBreak())

    # Slide 6: Conclusion
    story.append(Spacer(1, 40))
    story.append(Paragraph("PROJECT DEFENSE CONCLUSION", slide_tag))
    story.append(Paragraph("Thank You! We Are Ready for Your Questions.", ParagraphStyle('C1', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=navy)))
    story.append(HRFlowable(width="100%", thickness=2, color=blue, spaceBefore=10, spaceAfter=20))
    story.append(Paragraph("<b>Live Application URL:</b> http://127.0.0.1:5000", body_bold))
    story.append(Paragraph("<b>GitHub Repository:</b> https://github.com/eya-khandoudi/TestFlow-ISTQB", body_bold))
    story.append(Paragraph("<b>Lead QA Engineers &amp; Presenters:</b> Eya Khandoudi &amp; Ichraf Sassi", ParagraphStyle('C2', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=blue)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("All 92 automated tests passing with 91% code coverage. Master reports available in docs/ folder.", body_style))

    doc.build(story)
    
    # Copy to artifact folder
    import shutil
    shutil.copyfile(PDF_PATH, ARTIFACT_PDF_PATH)
    print(f"Generated PDF Slides: {PDF_PATH} and {ARTIFACT_PDF_PATH}")


if __name__ == '__main__':
    create_pptx()
    create_pdf_presentation()
    print("Presentation generation completed successfully!")
