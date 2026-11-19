import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

DOCS_PDF_PATH = r"c:\Users\Eya Khandoudi\Downloads\istqb\ISTQB\docs\TestFlow_Professor_Live_Demo_Guide.pdf"
ARTIFACT_PDF_PATH = r"C:\Users\Eya Khandoudi\.gemini\antigravity\brain\86fc9c4c-e6f5-410e-86a3-c9ce2182b962\TestFlow_Professor_Live_Demo_Guide.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress on cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header
        self.drawString(54, 792, "TESTFLOW  |  LIVE DEFENSE SCRIPT & PROFESSOR Q&A GUIDE")
        self.setFont("Helvetica", 8)
        self.drawRightString(541, 792, "ISTQB CTFL & IEEE 829")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 784, 541, 784)

        # Footer
        self.line(54, 46, 541, 46)
        self.drawString(54, 34, "Authors: Eya Khandoudi & Ichraf Sassi  |  Live Defense & Verification Cheat Sheet")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 34, page_str)
        self.restoreState()


def build_demo_guide_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Colors
    navy = colors.HexColor("#0F2942")
    blue = colors.HexColor("#2B6CB0")
    teal = colors.HexColor("#2C7A7B")
    dark_slate = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#E2E8F0")
    green = colors.HexColor("#22543D")
    red = colors.HexColor("#742A2A")

    # Typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=navy,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=blue,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=navy,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=blue,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=dark_slate,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    quote_style = ParagraphStyle(
        'DialogueQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1A365D")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_slate
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=navy
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#C53030")
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 30))
    badge_data = [[Paragraph("<b>LIVE PROJECT DEFENSE SCRIPT &amp; DEMONSTRATION GUIDE</b>", ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#2B6CB0")))]]
    t_badge = Table(badge_data, colWidths=[380])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#90CDF4")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 18))

    story.append(Paragraph("TestFlow — Live Examination &amp; Professor Demo Guide", title_style))
    story.append(Paragraph("A Step-by-Step Defense Script, Real-Time Verification Actions, CLI Commands, and Answers to Classic Professor Questions", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=blue, spaceAfter=18))

    meta_data = [
        [Paragraph("Document Purpose", table_cell_bold), Paragraph("Preparation guide for live project defense and interactive testing in front of the academic jury/professor", table_cell_style)],
        [Paragraph("Authors &amp; Presenters", table_cell_bold), Paragraph("<b>Eya Khandoudi &amp; Ichraf Sassi</b>", table_cell_style)],
        [Paragraph("Testing Standards", table_cell_bold), Paragraph("ISTQB CTFL v4.0 (Foundation) &amp; IEEE Std 829-2008 Standard", table_cell_style)],
        [Paragraph("Key Demonstrations", table_cell_bold), Paragraph("Live BVA/EP validation, Defect State Machine, Decision Table Triage, RTM Traceability, and Pytest CLI runs", table_cell_style)],
        [Paragraph("Application Endpoint", table_cell_bold), Paragraph("http://127.0.0.1:5000", table_cell_style)],
        [Paragraph("Automated Test Suite", table_cell_bold), Paragraph("92 Automated Tests (All Passed, 91% Code Statement Coverage)", table_cell_style)],
        [Paragraph("Defense Date", table_cell_bold), Paragraph("November 2026", table_cell_style)],
    ]
    meta_table = Table(meta_data, colWidths=[150, 337])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 25))

    # Core Principles Callout Box
    prin_data = [
        [
            Paragraph("<b>RULE 1: Show the Theory</b><br/><font size=7 color='#718096'>Explain EP, BVA, STT, DTT, and RBT clearly.</font>", ParagraphStyle('P1', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=navy)),
            Paragraph("<b>RULE 2: Prove Enforcement</b><br/><font size=7 color='#718096'>Show how backend code strictly blocks illegal actions.</font>", ParagraphStyle('P2', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=blue)),
            Paragraph("<b>RULE 3: Run the CLI</b><br/><font size=7 color='#718096'>Execute Pytest by marker in 2 seconds.</font>", ParagraphStyle('P3', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=1, textColor=green)),
        ]
    ]
    t_prin = Table(prin_data, colWidths=[162, 162, 163])
    t_prin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_prin)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: PRE-FLIGHT SETUP
    # =========================================================================
    story.append(Paragraph("1. Pre-Flight Setup (30 Seconds Before the Presentation)", h1_style))
    story.append(Paragraph(
        "Before calling the professor to your screen, ensure your environment is running and cleanly pre-configured:", body_style
    ))

    setup_data = [
        [Paragraph("Step", table_header_style), Paragraph("Action", table_header_style), Paragraph("Command / Location", table_header_style), Paragraph("Verification Check", table_header_style)],
        [
            Paragraph("<b>1</b>", table_cell_bold),
            Paragraph("Start Flask Server", table_cell_style),
            Paragraph("<code>python run.py</code>", code_style),
            Paragraph("Output shows: <i>Running on http://127.0.0.1:5000</i>", table_cell_style)
        ],
        [
            Paragraph("<b>2</b>", table_cell_bold),
            Paragraph("Open Browser Tabs", table_cell_style),
            Paragraph("Tab 1: <code>http://127.0.0.1:5000/</code><br/>Tab 2: <code>http://127.0.0.1:5000/rtm</code>", code_style),
            Paragraph("Dashboard displays metrics &amp; Decision Table Release Gate", table_cell_style)
        ],
        [
            Paragraph("<b>3</b>", table_cell_bold),
            Paragraph("Open Second Terminal", table_cell_style),
            Paragraph("Directory: <code>.../ISTQB</code>", code_style),
            Paragraph("Ready to type <code>pytest -m ...</code> on command", table_cell_style)
        ],
        [
            Paragraph("<b>4</b>", table_cell_bold),
            Paragraph("Have PDF Ready", table_cell_style),
            Paragraph("<code>docs/TestFlow_Full_Project_Report.pdf</code>", code_style),
            Paragraph("7-page master report open in background", table_cell_style)
        ],
    ]
    t_setup = Table(setup_data, colWidths=[35, 120, 192, 140])
    t_setup.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_setup)

    story.append(Spacer(1, 12))

    # =========================================================================
    # SECTION 2: THE 5-MINUTE LIVE DEMONSTRATION SCRIPT
    # =========================================================================
    story.append(Paragraph("2. The 5-Minute Live Demonstration Script", h1_style))
    story.append(Paragraph(
        "Follow this exact sequence. It walks the professor logically through the STLC phases: Analysis &rarr; Design &rarr; Execution &rarr; Defect Triage &rarr; Reporting.", body_style
    ))

    # Demo 1: Dashboard
    story.append(Paragraph("Step 1: Dashboard &amp; Decision Table Release Gate", h2_style))
    story.append(Paragraph("<b>Where to click:</b> Navigate to <code>http://127.0.0.1:5000/</code>", body_style))
    d1_box = [
        [Paragraph(
            "<b>What to Say:</b><br/>"
            "<i>\"Professor, TestFlow is built around the complete Software Testing Life Cycle (STLC). Here on the dashboard, we don't just display passive statistics; we actively evaluate an automated <b>IEEE 829 Release Gate Decision</b> using an <b>ISTQB Decision Table</b>. Right now, you can see the verdict is <b>NO-GO</b> in red because the system detected 2 open Blocker/Critical defects and the pass rate is 66.7%. The gate automatically flips to <b>GO</b> only when open blockers reach zero and pass rate exceeds 90%.\"</i>",
            quote_style
        )]
    ]
    t_d1 = Table(d1_box, colWidths=[487])
    t_d1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_d1)

    story.append(Spacer(1, 8))

    # Demo 2: BVA & RBT
    story.append(Paragraph("Step 2: Live Boundary Value Analysis (BVA) &amp; Risk-Based Testing (RBT)", h2_style))
    story.append(Paragraph("<b>Where to click:</b> Click <b>Test Cases</b> &rarr; <b>Create Test Case</b> (<code>/test-cases/new</code>)", body_style))
    d2_box = [
        [Paragraph(
            "<b>Live Actions to Perform in Front of Him:</b><br/>"
            "<b>1. Trigger BVA Rejection:</b> In the 'Test Case Code' field, enter <code>TC</code> (only 2 characters) and click Save. Show that the backend blocks submission: <i>'Code must have at least 3 characters.'</i><br/>"
            "&nbsp;&nbsp;&nbsp;&bull; <i>Explain: 'This enforces BVA at the minimum lower boundary of our input partition [3, 20] characters.'</i><br/>"
            "<b>2. Demonstrate Dynamic Risk Scoring:</b> Slide <b>Likelihood</b> to <code>4</code> and <b>Impact</b> to <code>5</code>.<br/>"
            "&nbsp;&nbsp;&nbsp;&bull; Point to the live preview badge: <b>Score: 20 (Critical Risk)</b> in red.<br/>"
            "&nbsp;&nbsp;&nbsp;&bull; <i>Explain: 'This applies <b>Risk-Based Testing (RBT)</b>. The system computes RPN = Likelihood &times; Impact. During execution cycles, high-risk scenarios are automatically sorted to run first (Shift-Left principle).'</i>",
            quote_style
        )]
    ]
    t_d2 = Table(d2_box, colWidths=[487])
    t_d2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FFF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C6F6D5")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_d2)

    story.append(PageBreak())

    # Demo 3: STT State Machine
    story.append(Paragraph("Step 3: State Transition Testing (STT) — The Core Highlight", h2_style))
    story.append(Paragraph("<b>Where to click:</b> Click <b>Defects</b> &rarr; Click on <b>BUG-001</b> (<code>/defects/1</code>)", body_style))
    d3_box = [
        [Paragraph(
            "<b>Live Actions to Perform in Front of Him:</b><br/>"
            "<b>1. Show Current State:</b> Point out that the defect is currently in state <b>Open</b>.<br/>"
            "<b>2. Inspect Permitted Transitions:</b> Open the 'Permitted Next State' dropdown. Notice that only <code>Fixed</code>, <code>Deferred</code>, and <code>Rejected</code> appear. <b>Closed is NOT an option!</b><br/>"
            "&nbsp;&nbsp;&nbsp;&bull; <i>Explain: 'According to ISTQB state transition rules, an open bug cannot jump directly to Closed. A developer cannot bypass the QA retesting process.'</i><br/>"
            "<b>3. Trigger Business Rule Rejection:</b> Select <code>Fixed</code>, leave the resolution notes blank, and click submit. Show the error: <i>'Transition to Fixed requires resolution notes.'</i><br/>"
            "<b>4. Complete Legal Transition:</b> Type: <code>Patched zero-division in commit #abc</code> and submit.<br/>"
            "&nbsp;&nbsp;&nbsp;&bull; The bug transitions to <b>Fixed</b> and the audit timeline updates.<br/>"
            "<b>5. Show QA Retest Requirement:</b> Look at the dropdown again: the only option is now <b>Retest</b>.<br/>"
            "&nbsp;&nbsp;&nbsp;&bull; <i>Explain: 'The bug is deployed to QA. Only when the QA engineer verifies the fix in Retest can it finally transition to Closed.'</i>",
            quote_style
        )]
    ]
    t_d3 = Table(d3_box, colWidths=[487])
    t_d3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FED7D7")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_d3)

    story.append(Spacer(1, 8))

    # Demo 4: RTM
    story.append(Paragraph("Step 4: Requirements Traceability Matrix (RTM)", h2_style))
    story.append(Paragraph("<b>Where to click:</b> Click <b>ISTQB Reports</b> &rarr; <b>Traceability Matrix (RTM)</b> (<code>/rtm</code>)", body_style))
    d4_box = [
        [Paragraph(
            "<b>What to Say:</b><br/>"
            "<i>\"Here we prove 100% bi-directional traceability. Every requirement on the left maps forward to its test cases, test run execution status, and any defect raised. Notice that our coverage gauge shows 100% and we have <b>0 orphaned test cases</b>. This guarantees that every single test in the repository exists solely to verify an approved business requirement.\"</i>",
            quote_style
        )]
    ]
    t_d4 = Table(d4_box, colWidths=[487])
    t_d4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAF5FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E9D8FD")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_d4)

    story.append(Spacer(1, 8))

    # Demo 5: Pytest CLI
    story.append(Paragraph("Step 5: Pytest Test Automation Execution via CLI", h2_style))
    story.append(Paragraph("Switch to your terminal window and announce: <i>\"We also automated 92 test cases in Pytest organized by ISTQB markers:\"</i>", body_style))

    cli_table_data = [
        [Paragraph("If the Professor Asks About...", table_header_style), Paragraph("Type This Exact Command", table_header_style), Paragraph("What It Shows", table_header_style)],
        [
            Paragraph("<b>Equivalence Partitioning</b>", table_cell_bold),
            Paragraph("<code>pytest -m equivalence_partitioning</code>", code_style),
            Paragraph("19 passed in 0.8s: valid/invalid ratings, emails, quantities.", table_cell_style)
        ],
        [
            Paragraph("<b>Boundary Value Analysis</b>", table_cell_bold),
            Paragraph("<code>pytest -m boundary_value_analysis</code>", code_style),
            Paragraph("16 passed in 0.7s: 0, 1, 2, 98, 99, 100 cart boundary tests.", table_cell_style)
        ],
        [
            Paragraph("<b>Decision Table Testing</b>", table_cell_bold),
            Paragraph("<code>pytest -m decision_table</code>", code_style),
            Paragraph("10 passed in 0.6s: Defect triage combinations &amp; release gate logic.", table_cell_style)
        ],
        [
            Paragraph("<b>State Transitions</b>", table_cell_bold),
            Paragraph("<code>pytest -m state_transition</code>", code_style),
            Paragraph("10 passed in 0.6s: Proves illegal jumps like New &rarr; Closed raise exceptions.", table_cell_style)
        ],
        [
            Paragraph("<b>Risk-Based Testing</b>", table_cell_bold),
            Paragraph("<code>pytest -m risk_based</code>", code_style),
            Paragraph("5 passed in 0.5s: RPN formula &amp; execution priority sorting.", table_cell_style)
        ],
        [
            Paragraph("<b>Code Coverage</b>", table_cell_bold),
            Paragraph("<code>pytest --cov=app --cov-report=term-missing</code>", code_style),
            Paragraph("Outputs full coverage breakdown showing <b>91% across all modules</b>.", table_cell_style)
        ],
    ]
    t_cli = Table(cli_table_data, colWidths=[130, 207, 150])
    t_cli.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_cli)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: PROFESSOR Q&A DEFENSE CHEAT SHEET
    # =========================================================================
    story.append(Paragraph("3. Professor Q&amp;A Defense Cheat Sheet (Classic Questions &amp; Answers)", h1_style))
    story.append(Paragraph(
        "Be ready for these common questions during your defense. Use the exact keywords provided below:", body_style
    ))

    qa_data = [
        [Paragraph("Professor's Question", table_header_style), Paragraph("Your Exact Answer &amp; ISTQB Keywords", table_header_style)],
        [
            Paragraph("<b>Q1: What is the fundamental difference between EP and BVA in your project?</b>", table_cell_bold),
            Paragraph(
                "<i>\"<b>Equivalence Partitioning</b> divides inputs into valid and invalid classes where all values produce equivalent behavior — for example, cart quantity between 1 and 99 is valid, while negative numbers are invalid. <br/><br/>"
                "<b>Boundary Value Analysis</b> specifically tests the extreme edges: 0 (below min), 1 (min), 99 (max), and 100 (above max), because empirical studies show that developers make the highest concentration of off-by-one errors at partition boundaries.\"</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q2: Why did you implement Risk-Based Testing (RBT) instead of running tests randomly?</b>", table_cell_bold),
            Paragraph(
                "<i>\"In real-world projects, budget and time constraints prevent running exhaustive suites on every build. By calculating <b>RPN = Likelihood &times; Impact</b> ($1 \\dots 25$), our test run engine sorts test cases so high-risk critical paths (like credit card payment processing) are executed first. This applies the <b>Shift-Left</b> principle to discover showstopper defects as early as possible in the test cycle.\"</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q3: How does your system prevent illegal defect status transitions?</b>", table_cell_bold),
            Paragraph(
                "<i>\"We implemented an active State Machine in <code>app/services/istqb_engine.py</code>. It defines an explicit transition graph. If someone attempts an illegal jump (like jumping directly from <code>New &rarr; Closed</code> without resolution or QA retest), the backend intercepts the request and raises an <code>InvalidStateTransitionError</code> (HTTP 422). The UI also dynamically filters the dropdown to only present legally permitted next states.\"</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q4: What happens if a bug fails during verification? How do you handle defect re-opening?</b>", table_cell_bold),
            Paragraph(
                "<i>\"When a defect is in <code>Retest</code> and verification fails, the QA engineer transitions it to <code>Reopened</code>. The state machine routes the defect back to the developer with the new failure logs, and the chronological audit timeline preserves every previous state change and comment.\"</i>",
                table_cell_style
            )
        ],
        [
            Paragraph("<b>Q5: What documentation and test standards did you adhere to?</b>", table_cell_bold),
            Paragraph(
                "<i>\"We adhered to <b>ISTQB CTFL v4.0</b> for all test design techniques (EP, BVA, DTT, STT, RBT) and <b>IEEE Std 829-2008</b> for the Master Test Plan structure, Exit Gate criteria, and Test Summary Reporting.\"</i>",
                table_cell_style
            )
        ],
    ]
    t_qa = Table(qa_data, colWidths=[150, 337])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_qa)

    story.append(Spacer(1, 14))

    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Presented By:</b><br/>Eya Khandoudi &amp; Ichraf Sassi<br/><font size=7 color='#718096'>Software Test Engineers</font>", table_cell_style),
            Paragraph("<b>Project:</b><br/>TestFlow ISTQB Suite<br/><font size=7 color='#718096'>IEEE 829 &amp; CTFL v4.0</font>", table_cell_style),
            Paragraph("<b>Verdict:</b><br/><font color='#22543D'><b>READY FOR LIVE PRESENTATION</b></font><br/><font size=7 color='#718096'>All 92 Tests Passing</font>", table_cell_style),
        ]
    ]
    t_sign = Table(sign_data, colWidths=[162, 162, 163])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated Live Demo Guide PDF: {output_filename}")


if __name__ == '__main__':
    os.makedirs(os.path.dirname(DOCS_PDF_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(ARTIFACT_PDF_PATH), exist_ok=True)

    # 1. Generate in docs directory
    build_demo_guide_pdf(DOCS_PDF_PATH)

    # 2. Generate in conversation artifact directory for user download
    build_demo_guide_pdf(ARTIFACT_PDF_PATH)

    print("Professor Live Demo Guide PDF generated successfully in both locations!")
