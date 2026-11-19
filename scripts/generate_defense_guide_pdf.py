import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

DOCS_PDF_PATH = r"c:\Users\Eya Khandoudi\Downloads\istqb\ISTQB\docs\TestFlow_Live_Defense_Guide.pdf"
ARTIFACT_PDF_PATH = r"C:\Users\Eya Khandoudi\.gemini\antigravity\brain\86fc9c4c-e6f5-410e-86a3-c9ce2182b962\TestFlow_Live_Defense_Guide.pdf"

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
        self.drawString(54, 792, "TESTFLOW  |  LIVE PROJECT DEFENSE & PRESENTATION GUIDE")
        self.setFont("Helvetica", 8)
        self.drawRightString(541, 792, "ISTQB CTFL & IEEE 829 DEMO PROTOCOL")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 784, 541, 784)

        # Footer
        self.line(54, 46, 541, 46)
        self.drawString(54, 34, "Presenters: Eya Khandoudi & Ichraf Sassi  |  ISTQB Live Defense Script")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 34, page_str)
        self.restoreState()


def build_defense_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color definitions
    navy = colors.HexColor("#0F2942")
    blue = colors.HexColor("#2B6CB0")
    teal = colors.HexColor("#2C7A7B")
    dark_slate = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#E2E8F0")
    green = colors.HexColor("#22543D")
    red = colors.HexColor("#742A2A")

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

    dialogue_say = ParagraphStyle(
        'DialogueSay',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=5
    )

    dialogue_do = ParagraphStyle(
        'DialogueDo',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor("#C53030"),
        spaceAfter=4
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

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 25))
    badge_data = [[Paragraph("<b>OFFICIAL PROJECT DEFENSE &amp; LIVE DEMO PROTOCOL</b>", ParagraphStyle('B', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#2B6CB0")))]]
    t_badge = Table(badge_data, colWidths=[380])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#90CDF4")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 16))

    story.append(Paragraph("TestFlow — Live Presentation &amp; Defense Guide", title_style))
    story.append(Paragraph("A Step-by-Step Practical Demonstration Protocol, Live Testing Script &amp; Examination Q&amp;A for the Professor", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=blue, spaceAfter=18))

    meta_data = [
        [Paragraph("Document Identifier", table_cell_bold), Paragraph("DEF-TESTFLOW-2026-LIVE", table_cell_style)],
        [Paragraph("Project Authors &amp; Presenters", table_cell_bold), Paragraph("<b>Eya Khandoudi &amp; Ichraf Sassi</b>", table_cell_style)],
        [Paragraph("Examination Role", table_cell_bold), Paragraph("Live System Demonstration &amp; ISTQB Methodology Defense", table_cell_style)],
        [Paragraph("Demonstration Focus", table_cell_bold), Paragraph("Live STLC Execution, State Transitions, Decision Tables, BVA/EP &amp; Pytest", table_cell_style)],
        [Paragraph("Application URL", table_cell_bold), Paragraph("http://127.0.0.1:5000", table_cell_style)],
        [Paragraph("Automated Tests Ready", table_cell_bold), Paragraph("92 Automated Pytest Tests (91% Statement Coverage)", table_cell_style)],
        [Paragraph("Standards Demonstrated", table_cell_bold), Paragraph("ISTQB CTFL v4.0 &amp; IEEE Std 829-2008 Standard", table_cell_style)],
        [Paragraph("Date of Presentation", table_cell_bold), Paragraph("November 2026", table_cell_style)],
    ]
    meta_table = Table(meta_data, colWidths=[160, 327])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 20))

    exec_tips = [
        [
            Paragraph("<b>GOLDEN RULE FOR DEFENSE</b><br/><font size=7.5 color='#2D3748'>Never show static slides. Open the live browser and active terminal. Professors grade on <i>demonstrable proof</i> that the backend enforces ISTQB rules rather than just showing mocked text.</font>", ParagraphStyle('H1', fontName='Helvetica', fontSize=8.5, leading=12, alignment=1, textColor=navy)),
        ]
    ]
    t_tip = Table(exec_tips, colWidths=[487])
    t_tip.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCBF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D69E2E")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_tip)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: 30-SECOND SETUP CHECKLIST
    # =========================================================================
    story.append(Paragraph("1. Rapid 30-Second Pre-Defense Checklist", h1_style))
    story.append(Paragraph(
        "Complete these three simple steps before inviting the professor to observe the demonstration:", body_style
    ))

    setup_data = [
        [Paragraph("Step", table_header_style), Paragraph("Action Required", table_header_style), Paragraph("Command / URL", table_header_style), Paragraph("Expected Verification State", table_header_style)],
        [
            Paragraph("<b>1</b>", table_cell_bold),
            Paragraph("Start Flask Server", table_cell_style),
            Paragraph("<code>python run.py</code>", table_cell_style),
            Paragraph("Server running at <code>http://127.0.0.1:5000</code>", table_cell_style)
        ],
        [
            Paragraph("<b>2</b>", table_cell_bold),
            Paragraph("Open Web Browser", table_cell_style),
            Paragraph("<code>http://127.0.0.1:5000</code>", table_cell_style),
            Paragraph("Dashboard displays with charts and Release Gate banner", table_cell_style)
        ],
        [
            Paragraph("<b>3</b>", table_cell_bold),
            Paragraph("Open Second Terminal", table_cell_style),
            Paragraph("In project root directory", table_cell_style),
            Paragraph("Ready to run <code>pytest</code> commands on demand", table_cell_style)
        ],
    ]
    t_setup = Table(setup_data, colWidths=[35, 120, 150, 182])
    t_setup.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_setup)

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 2: 5-MINUTE STEP-BY-STEP LIVE DEMO SCRIPT
    # =========================================================================
    story.append(Paragraph("2. The 5-Minute Live Demonstration Script", h1_style))
    story.append(Paragraph(
        "Follow this exact sequence to demonstrate the system smoothly and convincingly:", body_style
    ))

    # Step 1
    story.append(Paragraph("Step 1: Dashboard &amp; Decision Table Release Gate (60 Seconds)", h2_style))
    story.append(Paragraph("<b>Where to go:</b> <code>http://127.0.0.1:5000/</code> (Dashboard)", dialogue_do))
    story.append(Paragraph(
        "\"Professor, TestFlow is structured around the Software Testing Life Cycle (STLC). On this dashboard, "
        "we evaluate an automated <b>IEEE Std 829-2008 Release Gate Decision</b> using an <b>ISTQB Decision Table</b>. "
        "Notice the red banner displaying <b>NO-GO</b>: the decision engine automatically blocks release because we have "
        "2 unresolved Blocker/Critical defects and an execution pass rate of 66.7%. The gate automatically flips to <b>GO</b> "
        "only when blockers reach zero and pass rate meets the 90% exit threshold.\"",
        dialogue_say
    ))

    # Step 2
    story.append(Paragraph("Step 2: Boundary Value Analysis (BVA) &amp; Risk-Based Testing (60 Seconds)", h2_style))
    story.append(Paragraph("<b>Where to go:</b> Click 'Test Cases' &rarr; 'Create Test Case' (<code>/test-cases/new</code>)", dialogue_do))
    story.append(Paragraph(
        "\"Here we demonstrate two key techniques:<br/>"
        "1. <b>Boundary Value Analysis (BVA):</b> In the Test Case Code field, if I enter just <code>TC</code> (2 chars) and submit, "
        "the backend validator intercepts it with an ISTQBValidationError: <i>'Test Case Code must have at least 3 characters'</i>. "
        "This validates the lower boundary point $[3, 20]$ characters.<br/>"
        "2. <b>Risk-Based Testing (RBT):</b> As I adjust Likelihood to 4 and Impact to 5, the badge updates dynamically in real-time "
        "to compute the Risk Priority Number ($RPN = 4 \\times 5 = 20$, Critical Risk). The execution engine uses this score to schedule "
        "high-risk tests first.\"",
        dialogue_say
    ))

    story.append(PageBreak())

    # Step 3
    story.append(Paragraph("Step 3: State Transition Testing (STT) Defect Lifecycle (90 Seconds - The Highlight)", h2_style))
    story.append(Paragraph("<b>Where to go:</b> Click 'Defects' &rarr; Click on <b>BUG-001</b> (<code>/defects/1</code>)", dialogue_do))
    story.append(Paragraph(
        "\"This is our State Transition Testing engine enforcing the formal ISTQB Defect Lifecycle. Notice that BUG-001 is currently <b>Open</b>.<br/>"
        "&bull;&nbsp; Look at the 'Permitted Next State' dropdown: only <code>Fixed</code>, <code>Deferred</code>, and <code>Rejected</code> are allowed. "
        "<b><code>Closed</code> is not even an option!</b> According to ISTQB rules, a developer cannot close an open defect directly.<br/>"
        "&bull;&nbsp; If I select <code>Fixed</code> without entering notes, the system rejects it: resolution notes are mandatory.<br/>"
        "&bull;&nbsp; I enter a fix note and click Apply: the defect transitions to <code>Fixed</code> and logs the change to the audit timeline.<br/>"
        "&bull;&nbsp; Now the only allowed state is <code>Retest</code>. Only the QA engineer verifying the fix during retest has the authority to transition it to <code>Closed</code>.\"",
        dialogue_say
    ))

    # Step 4
    story.append(Paragraph("Step 4: Requirements Traceability Matrix (RTM) (45 Seconds)", h2_style))
    story.append(Paragraph("<b>Where to go:</b> Click 'ISTQB Reports' &rarr; 'Traceability Matrix (RTM)' (<code>/rtm</code>)", dialogue_do))
    story.append(Paragraph(
        "\"Here we prove 100% bi-directional traceability. Every requirement on the left maps forward to its test cases, "
        "execution outcomes, and linked defects. We have <b>0 orphaned test cases</b> — every test exists solely to verify "
        "an approved business requirement. This guarantees complete test basis coverage without scope creep.\"",
        dialogue_say
    ))

    # Step 5
    story.append(Paragraph("Step 5: Run Automated Tests in Front of the Professor (45 Seconds)", h2_style))
    story.append(Paragraph("<b>Where to go:</b> Switch to terminal and run: <code>pytest</code>", dialogue_do))
    story.append(Paragraph(
        "\"In addition to the web platform, we authored an automated test suite with <b>92 automated tests</b> using Pytest. "
        "Every single test is categorized by ISTQB technique. Running <code>pytest</code> executes all 92 tests in under 5 seconds with 100% pass rate. "
        "Running with coverage shows <b>91% code coverage</b> across the entire codebase.\"",
        dialogue_say
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: AUTOMATED PYTEST LIVE DEMO PROTOCOL
    # =========================================================================
    story.append(Paragraph("3. Pytest Live Execution Command Cheat-Sheet", h1_style))
    story.append(Paragraph(
        "If the professor asks you to demonstrate a specific technique via command-line automation, use these exact commands:", body_style
    ))

    cmd_data = [
        [Paragraph("Professor's Request", table_header_style), Paragraph("Pytest Command", table_header_style), Paragraph("What It Demonstrates to Him", table_header_style)],
        [
            Paragraph("Show me Equivalence Partitioning", table_cell_bold),
            Paragraph("<code>pytest -m equivalence_partitioning</code>", table_cell_style),
            Paragraph("Runs 19 tests validating valid vs invalid partitions for ratings, quantities, and email formats.", table_cell_style)
        ],
        [
            Paragraph("Show me Boundary Value Analysis", table_cell_bold),
            Paragraph("<code>pytest -m boundary_value_analysis</code>", table_cell_style),
            Paragraph("Runs 16 tests proving 2-value and 3-value boundary points: 0, 1, 2, 98, 99, 100 for cart lines.", table_cell_style)
        ],
        [
            Paragraph("Show me State Transitions", table_cell_bold),
            Paragraph("<code>pytest -m state_transition</code>", table_cell_style),
            Paragraph("Runs 10 tests proving valid state paths and verifying that illegal jumps (e.g. New &rarr; Closed) raise exceptions.", table_cell_style)
        ],
        [
            Paragraph("Show me Decision Tables", table_cell_bold),
            Paragraph("<code>pytest -m decision_table</code>", table_cell_style),
            Paragraph("Runs 10 tests verifying the SLA triage truth table and Release Gate logic.", table_cell_style)
        ],
        [
            Paragraph("Show me Error Guessing", table_cell_bold),
            Paragraph("<code>pytest -m error_guessing</code>", table_cell_style),
            Paragraph("Runs 5 tests proving parameterized protection against SQL injection and XSS script tags.", table_cell_style)
        ],
        [
            Paragraph("Show me Code Coverage", table_cell_bold),
            Paragraph("<code>pytest --cov=app --cov-report=term-missing</code>", table_cell_style),
            Paragraph("Displays the complete 91% code coverage breakdown across all 710 statements.", table_cell_style)
        ],
    ]
    t_cmd = Table(cmd_data, colWidths=[130, 187, 170])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg]),
    ]))
    story.append(t_cmd)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: 6 CLASSIC PROFESSOR QUESTIONS & MODEL ANSWERS
    # =========================================================================
    story.append(Paragraph("4. Anticipated Professor Questions &amp; Exact Model Answers", h1_style))
    story.append(Paragraph(
        "Here are the most common questions examiners ask during software testing project defenses, along with your recommended answers:", body_style
    ))

    def add_qa_box(q_num, question, answer):
        q_data = [
            [Paragraph(f"<b>Q{q_num}: {question}</b>", ParagraphStyle('Q', fontName='Helvetica-Bold', fontSize=8.5, leading=12, textColor=navy))],
            [Paragraph(f"<b>Your Exact Answer:</b> {answer}", ParagraphStyle('A', fontName='Helvetica', fontSize=8, leading=11.5, textColor=dark_slate))]
        ]
        t_qa = Table(q_data, colWidths=[487])
        t_qa.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0,1), (-1,1), light_bg),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        return t_qa

    story.append(add_qa_box(
        1,
        "What is the exact distinction between Equivalence Partitioning and Boundary Value Analysis in your system?",
        "\"Equivalence Partitioning divides the input domain into classes where all elements are expected to produce equivalent behavior — "
        "for example, cart quantity between 1 and 99 is valid, while negative numbers are invalid. Boundary Value Analysis specifically tests the extreme edges "
        "of those partitions: 0 (below min), 1 (min), 99 (max), and 100 (above max). BVA is critical because developers most frequently make off-by-one errors (&lt; vs &le;) at boundary conditions.\""
    ))
    story.append(Spacer(1, 6))

    story.append(add_qa_box(
        2,
        "Why did you choose to implement Risk-Based Testing (RBT) in TestFlow?",
        "\"In professional software testing, testing exhaustively is impossible due to project time and budget constraints. "
        "By calculating $RPN = Likelihood \\times Impact$, our test execution engine automatically sorts scenarios to execute high-risk tests "
        "(such as payment gateway authorization) first. This applies the ISTQB Shift-Left principle, surfacing critical blocker defects as early as possible in the STLC.\""
    ))
    story.append(Spacer(1, 6))

    story.append(add_qa_box(
        3,
        "What happens in your state machine if a defect fix fails during verification?",
        "\"According to the ISTQB Defect Lifecycle, when a defect is in the <code>Retest</code> state and verification fails, the QA engineer transitions "
        "it to <code>Reopened</code>. The defect is routed back to the developer with the new failure log. It cannot be closed directly, preserving an unbroken audit history.\""
    ))
    story.append(Spacer(1, 6))

    story.append(add_qa_box(
        4,
        "How do you ensure you haven't introduced security vulnerabilities in user inputs?",
        "\"We applied Error Guessing and negative security testing. In <code>tests/istqb/test_error_guessing.py</code>, we pass classic SQL injection payloads "
        "like <code>'; DROP TABLE test_cases; --</code> and XSS script tags. All database queries use parameterized SQL statements through SQLite, and templates enforce auto-escaping, "
        "preventing data leaks and script execution.\""
    ))
    story.append(Spacer(1, 6))

    story.append(add_qa_box(
        5,
        "What IEEE standard did you follow for your test documentation?",
        "\"We adhered to <b>IEEE Std 829-2008 Standard for Software and System Test Documentation</b>. We authored the Master Test Plan (<code>TEST_PLAN_IEEE829.md</code>) "
        "and generate the official Test Summary Report (<code>/report/1</code>) containing executive summaries, variance assessments, residual defect tables, and sign-off blocks.\""
    ))
    story.append(Spacer(1, 6))

    story.append(add_qa_box(
        6,
        "Is this a mock frontend, or is the backend actually processing real data?",
        "\"It is a 100% active Python and Flask backend backed by an atomic SQLite database (<code>testflow.db</code>). When we record a test execution or log a bug, "
        "an actual SQL INSERT or UPDATE executes on disk. When we attempt an illegal transition, the Python state machine in <code>app/services/istqb_engine.py</code> "
        "actively intercepts it and throws an <code>InvalidStateTransitionError</code>.\""
    ))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: SIGN-OFF & PRESENTERS
    # =========================================================================
    story.append(Paragraph("5. Student Presenters &amp; Examination Verification", h1_style))
    sign_data = [
        [
            Paragraph("<b>Presenter &amp; Lead QA:</b><br/>Eya Khandoudi<br/><font size=7 color='#718096'>ISTQB Certified Tester</font><br/><br/><b>Role:</b> Live System Demo &amp; BVA/STT", table_cell_style),
            Paragraph("<b>Presenter &amp; Lead QA:</b><br/>Ichraf Sassi<br/><font size=7 color='#718096'>ISTQB Certified Tester</font><br/><br/><b>Role:</b> Decision Tables, RTM &amp; Pytest", table_cell_style),
            Paragraph("<b>Evaluation Standard:</b><br/>ISTQB CTFL v4.0 &amp; IEEE 829<br/><br/><b>Status:</b> <font color='#22543D'><b>DEFENSE READY</b></font>", table_cell_style),
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
    print(f"Generated Live Defense Guide PDF: {output_filename}")


if __name__ == '__main__':
    os.makedirs(os.path.dirname(DOCS_PDF_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(ARTIFACT_PDF_PATH), exist_ok=True)

    # 1. Generate in docs directory
    build_defense_pdf(DOCS_PDF_PATH)

    # 2. Generate in conversation artifact directory for user download
    build_defense_pdf(ARTIFACT_PDF_PATH)

    print("Live Defense Guide PDF generated successfully in both locations!")
