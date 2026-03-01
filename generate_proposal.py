"""
Generate a clean, professional research proposal PDF.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "RESEARCH_PROPOSAL.pdf")

# ── colours ──────────────────────────────────────────────────────────
DARK   = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
MID    = HexColor("#16213e")
LIGHT  = HexColor("#0f3460")
GREY   = HexColor("#f5f5f5")
DGREY  = HexColor("#333333")
WHITE  = HexColor("#ffffff")

# ── custom flowable: coloured box ────────────────────────────────────
class ColorBox(Flowable):
    def __init__(self, width, height, color, text, text_color=white, font_size=11):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        self.canv.setFillColor(self.text_color)
        self.canv.setFont("Helvetica-Bold", self.font_size)
        self.canv.drawCentredString(self.width / 2, self.height / 2 - 4, self.text)


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # custom styles
    styles.add(ParagraphStyle(
        "Title2", parent=styles["Title"], fontSize=22, leading=26,
        textColor=DARK, spaceAfter=4, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "Subtitle", parent=styles["Normal"], fontSize=12, leading=16,
        textColor=LIGHT, spaceAfter=2, fontName="Helvetica",
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "SectionHead", parent=styles["Heading1"], fontSize=15, leading=20,
        textColor=ACCENT, fontName="Helvetica-Bold", spaceBefore=18,
        spaceAfter=8, borderPadding=(0, 0, 2, 0),
    ))
    styles.add(ParagraphStyle(
        "SubHead", parent=styles["Heading2"], fontSize=12, leading=16,
        textColor=MID, fontName="Helvetica-Bold", spaceBefore=12,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=10.5, leading=15,
        textColor=DGREY, fontName="Helvetica", alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "BodyBold", parent=styles["Normal"], fontSize=10.5, leading=15,
        textColor=DGREY, fontName="Helvetica-Bold", alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        "BulletCustom", parent=styles["Normal"], fontSize=10.5, leading=15,
        textColor=DGREY, fontName="Helvetica", leftIndent=20,
        bulletIndent=8, spaceAfter=3, alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        "SmallCenter", parent=styles["Normal"], fontSize=9, leading=12,
        textColor=LIGHT, fontName="Helvetica", alignment=TA_CENTER,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "TableCell", parent=styles["Normal"], fontSize=9.5, leading=13,
        textColor=DGREY, fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "TableHead", parent=styles["Normal"], fontSize=9.5, leading=13,
        textColor=WHITE, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Quote", parent=styles["Normal"], fontSize=10, leading=14,
        textColor=LIGHT, fontName="Helvetica-Oblique",
        leftIndent=30, rightIndent=30, spaceAfter=8, spaceBefore=8,
        alignment=TA_CENTER,
    ))

    story = []

    # helper shortcuts
    def sec(text):   story.append(Paragraph(text, styles["SectionHead"]))
    def sub(text):   story.append(Paragraph(text, styles["SubHead"]))
    def body(text):  story.append(Paragraph(text, styles["Body"]))
    def bold(text):  story.append(Paragraph(text, styles["BodyBold"]))
    def bullet(text): story.append(Paragraph(text, styles["BulletCustom"], bulletText="•"))
    def gap(h=10):   story.append(Spacer(1, h))
    def line():      story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#dddddd"), spaceAfter=10, spaceBefore=10))
    def quote(text): story.append(Paragraph(text, styles["Quote"]))

    def make_table(headers, rows, col_widths=None):
        header_style = styles["TableHead"]
        cell_style = styles["TableCell"]
        data = [[Paragraph(h, header_style) for h in headers]]
        for row in rows:
            data.append([Paragraph(str(c), cell_style) for c in row])
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, -1), GREY),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREY]),
        ]))
        story.append(t)

    # ═══════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════════════════════════════════════
    gap(80)
    story.append(Paragraph("RESEARCH PROPOSAL", styles["Title2"]))
    gap(8)
    story.append(HRFlowable(width="40%", thickness=2, color=ACCENT, spaceAfter=8, spaceBefore=4))
    story.append(Paragraph(
        "Routing Between Humans and AI:<br/>"
        "A Stackelberg Game for Task Allocation<br/>"
        "and Worker Welfare",
        ParagraphStyle("BigTitle", parent=styles["Title"], fontSize=17, leading=22,
                       textColor=MID, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=12)
    ))
    gap(12)
    story.append(Paragraph("Nathan Amankwah", styles["Subtitle"]))
    story.append(Paragraph("Prepared for Prof. Rafid Mahmood", styles["Subtitle"]))
    story.append(Paragraph("Telfer School of Management, University of Ottawa", styles["Subtitle"]))
    gap(8)
    story.append(Paragraph("March 2026", styles["Subtitle"]))
    gap(40)
    story.append(HRFlowable(width="60%", thickness=0.5, color=HexColor("#cccccc"), spaceAfter=10))
    story.append(Paragraph(
        "Building on: Mahmood, \"Routing, Cascades, and User Choice for LLMs\" (ICLR 2026)<br/>"
        "and \"Pricing and Competition for Generative AI\" (NeurIPS 2024)",
        ParagraphStyle("Ref", parent=styles["Normal"], fontSize=9, leading=12,
                       textColor=LIGHT, alignment=TA_CENTER)
    ))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════════════════════
    sec("Table of Contents")
    line()
    toc_items = [
        ("1", "The Big Question"),
        ("2", "Why This Question Matters Right Now"),
        ("3", "How It Connects to Prof. Mahmood's Research"),
        ("4", "The Model — Step by Step"),
        ("5", "What I Expect to Find"),
        ("6", "How I Would Conduct the Research"),
        ("7", "Timeline"),
        ("8", "Why This is the Right Project"),
    ]
    for num, title in toc_items:
        body(f"<b>Section {num}</b> — {title}")
    gap(6)
    line()

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 1: THE BIG QUESTION
    # ═══════════════════════════════════════════════════════════════════
    sec("1. The Big Question")
    line()

    bold("Research Question:")
    gap(4)
    quote(
        "\"When a company decides which tasks go to AI and which stay with human workers, "
        "what happens to workers — and when are companies tempted to make jobs worse "
        "on purpose to push people out before replacing them with AI?\""
    )
    gap(6)

    body(
        "Every company today is making the same decision: should this task be done by a person "
        "or by an AI? A call center decides if your question goes to a chatbot or a human agent. "
        "A law firm decides if a contract gets reviewed by a junior lawyer or by AI software. "
        "Amazon decides if a warehouse task gets done by a robot or a worker."
    )
    body(
        "This is a <b>routing problem</b> — the exact same kind of problem Prof. Mahmood solved "
        "for AI models in his ICLR 2026 paper. In his paper, an AI company routes your question "
        "to either a cheap/fast model or an expensive/smart model. The user can give up if the "
        "model is too slow. The company tries to save money. There is a tension between what is "
        "best for the company and what is best for the user."
    )
    body(
        "My paper takes that exact same setup and asks: <b>what if instead of routing between "
        "two AI models, the company is routing between a human worker and an AI system?</b> "
        "The worker (like the user in Mahmood's paper) can quit if conditions get bad enough. "
        "The company (like the provider) tries to minimize costs. And just like Mahmood showed "
        "that AI companies can deliberately slow down models to push users away, I study whether "
        "companies are tempted to deliberately make jobs worse to push workers out."
    )

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 2: WHY THIS MATTERS
    # ═══════════════════════════════════════════════════════════════════
    sec("2. Why This Question Matters Right Now")
    line()

    body(
        "This is not a theoretical exercise. This is happening in the real economy today:"
    )
    gap(4)
    bullet("<b>McKinsey (2023)</b> estimates 30% of all work hours could be automated by 2030.")
    bullet("<b>Amazon warehouses</b> already use algorithms to route tasks between robots and human workers in real time.")
    bullet("<b>Call centers</b> route between AI chatbots and human agents — identical to the model I am proposing.")
    bullet("<b>Hollywood strikes (2023)</b> were specifically about studios replacing writers and actors with AI.")
    bullet("<b>Law firms</b> are using AI for document review work that was done by junior associates.")
    bullet("<b>\"Quiet firing\"</b> is a documented trend where companies deliberately degrade roles to push workers into quitting voluntarily before automating their position.")
    gap(6)
    body(
        "Despite all of this, there is <b>no formal mathematical model</b> that captures the strategic "
        "interaction between a company choosing automation levels and workers deciding whether to "
        "stay or leave. This paper fills that gap using the exact framework Prof. Mahmood has already "
        "built and proven."
    )

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 3: CONNECTION TO MAHMOOD
    # ═══════════════════════════════════════════════════════════════════
    sec("3. How It Connects to Prof. Mahmood's Research")
    line()

    sub("3.1 — Direct connection to the ICLR 2026 paper")
    body(
        "Prof. Mahmood's ICLR paper studies a game between an AI provider and a user. "
        "The provider routes tasks between two models. The user reacts. My paper uses the "
        "<b>exact same game structure</b> with different players:"
    )
    gap(4)

    make_table(
        ["Mahmood's Paper (ICLR 2026)", "My Paper", "In Plain English"],
        [
            ["M1 (standard model)", "H (human worker)", "The cheaper, less powerful option"],
            ["M2 (reasoning model)", "A (AI system)", "The more capable, more expensive option"],
            ["Provider (AI company)", "Firm (employer)", "The one making the routing decision"],
            ["User (person prompting)", "Worker (employee)", "The one who can stay or leave"],
            ["Success rate (p_i)", "Task quality (q_H, q_A)", "How well each option does the job"],
            ["Wait time (t_i)", "Wage (w_H) / compute cost (c_A)", "What each option costs"],
            ["User gives up (q)", "Worker quits (σ)", "The abandonment decision"],
            ["Lost revenue (P)", "Replacement cost (R)", "Penalty for losing them"],
            ["Cascade rate (s)", "Escalation rate (e)", "If AI fails, send to human"],
            ["Slow down the model", "Make the job worse", "Deliberate degradation for profit"],
        ],
        col_widths=[2.2*inch, 2.2*inch, 2.5*inch],
    )

    gap(10)
    body(
        "Because the mathematical structure is identical, all five of Prof. Mahmood's theorems "
        "and both propositions carry over. I do not need to re-derive the proofs — I need to "
        "<b>reinterpret what they mean</b> when the players are companies and workers instead of "
        "AI providers and users."
    )

    gap(8)
    sub("3.2 — Connection to the NeurIPS 2024 paper (Pricing and Competition)")
    body(
        "Prof. Mahmood's NeurIPS 2024 paper studies how AI companies price their models when "
        "competing for users. My paper connects to this because <b>AI pricing directly determines "
        "the cost of automation (c_A)</b>. When AI gets cheaper, the firm's incentive to automate "
        "increases, shifting the balance away from human workers. My model captures this: as c_A "
        "drops, the firm routes more tasks to AI, and workers face more pressure."
    )

    gap(8)
    sub("3.3 — Connection to the SSHRC Labour Equity Grant")
    body(
        "Prof. Mahmood holds an SSHRC Insight Development Grant ($68K) titled \"Levelling the "
        "Playing Field: Synthetic Data Solutions for Labour Market Equality.\" That grant studies "
        "how AI affects fairness in hiring. My paper studies the <b>next step</b> — what happens "
        "to workers AFTER they are hired, when the company starts routing tasks between them and AI. "
        "His grant asks: \"Who gets hired?\" My paper asks: \"Who gets to keep their job, and under "
        "what conditions?\""
    )

    gap(8)
    sub("3.4 — Connection to the societal impact focus")
    body(
        "In our meeting, Prof. Mahmood specifically mentioned societal and social issues in relation "
        "to his research. This paper is directly about one of the biggest social issues of our time: "
        "<b>AI replacing human workers and the power imbalance between employers and employees "
        "during that transition.</b> The \"quiet firing\" result — where companies are mathematically "
        "incentivized to degrade working conditions — is a finding with direct policy implications "
        "for labor law, union negotiations, and AI governance."
    )

    gap(8)
    sub("3.5 — His research philosophy: autonomous and self-directed")
    body(
        "Prof. Mahmood described research with him as autonomous and self-directed — people build "
        "on his work but find their own lane. This paper does exactly that:"
    )
    bullet("<b>His lane:</b> The math of how AI systems interact with people (routing games, pricing games)")
    bullet("<b>My lane:</b> Applying that math to the labor market — a distinct domain with its own literature, data, and policy implications")
    bullet("The framework is his. The application, interpretation, and societal contribution are mine.")

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 4: THE MODEL
    # ═══════════════════════════════════════════════════════════════════
    sec("4. The Model — Step by Step")
    line()

    sub("4.1 — The setup (who are the players, what do they choose?)")
    body("<b>Player 1: The Firm (employer)</b>")
    body(
        "A company has tasks that need to be done. For each task, the firm decides:"
    )
    bullet("<b>a</b> = what fraction of tasks go to AI (the \"automation rate\", between 0 and 1)")
    bullet("<b>e</b> = if AI fails a task, the chance it gets sent to a human worker (the \"escalation rate\")")
    body("This is identical to Mahmood's (i, s) — which model to route to first, and the cascade probability.")

    gap(6)
    body("<b>Player 2: The Worker (employee)</b>")
    body("The worker sees the firm's automation policy and decides:")
    bullet("<b>σ</b> = the chance they quit (between 0 and 1)")
    body("This is identical to Mahmood's q — the user's abandonment probability.")

    gap(8)
    sub("4.2 — The costs and values")
    body("Each option has a cost and a quality level:")
    gap(4)

    make_table(
        ["Parameter", "What it means", "Example"],
        [
            ["q_H (human quality)", "How well a human does the task", "A human agent resolves 85% of support tickets"],
            ["q_A (AI quality)", "How well AI does the task", "A chatbot resolves 60% of support tickets"],
            ["w_H (human wage)", "What the firm pays the worker per task", "$25/hour for a call center agent"],
            ["c_A (AI compute cost)", "What the firm pays to run AI per task", "$0.03 per chatbot interaction"],
            ["V (task revenue)", "What a completed task is worth to the firm", "$40 revenue per resolved ticket"],
            ["R (replacement cost)", "Cost to replace a worker who quits", "$4,000 to hire and train a new agent"],
            ["e_H (effort cost)", "How hard the work is for the worker", "Mental drain of handling angry customers"],
        ],
        col_widths=[1.6*inch, 2.5*inch, 2.8*inch],
    )

    gap(8)
    sub("4.3 — The key number: is the job worth it?")
    body(
        "In Mahmood's paper, the crucial number is the \"net value per pass\" — is this model "
        "worth trying once? (ξ_i = V × p_i − t_i). In my paper, the same idea applies:"
    )
    gap(4)
    bold("Worker net value: ξ_H = w_H − e_H")
    body(
        "This is simply: <b>wage minus effort</b>. Is the job worth doing?"
    )
    bullet("If ξ_H > 0: the job is \"worth it\" (good pay relative to effort)")
    bullet("If ξ_H < 0: the job is \"not worth it\" (effort exceeds the pay)")
    gap(4)
    body(
        "The worker also compares against their <b>outside option</b> — what they could earn or "
        "gain by leaving (unemployment benefits, a different job, going back to school). This "
        "determines whether quitting is attractive."
    )

    gap(8)
    sub("4.4 — The game (who moves first, who reacts)")
    body("The game follows the same order as Mahmood's Stackelberg game:")
    gap(4)
    bullet("<b>Step 1:</b> The firm announces its automation policy (a, e) — what fraction of tasks go to AI, and the escalation rate if AI fails.")
    bullet("<b>Step 2:</b> The worker observes this policy and decides whether to stay (σ = 0), quit (σ = 1), or something in between.")
    bullet("<b>Step 3:</b> Tasks are processed. AI handles some, humans handle some. If AI fails, some tasks escalate to humans.")
    bullet("<b>Step 4:</b> If the worker quits, the firm pays replacement cost R. If they stay, tasks keep flowing.")
    gap(4)
    body(
        "This repeats over time, just like the Markov chain in Mahmood's Figure 2. The absorbing "
        "states are \"task completed\" and \"worker quits.\""
    )

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 5: EXPECTED FINDINGS
    # ═══════════════════════════════════════════════════════════════════
    sec("5. What I Expect to Find")
    line()

    body(
        "Because the math maps directly from Mahmood's proven theorems, I can predict the key "
        "results. Each finding below corresponds to a specific theorem in his paper:"
    )
    gap(6)

    sub("Finding 1: Worker patience depends on whether the job is worth it")
    body("<i>Maps to Mahmood's Theorems 1 and 2</i>")
    gap(4)
    body("Workers fall into four groups based on whether the job is worth it and whether their outside options are good:")
    gap(4)

    make_table(
        ["Job worth it?", "Good outside options?", "What workers do", "Real-world example"],
        [
            ["Yes", "No", "Stay no matter what. They need this job and it pays well enough.", "Factory worker in a small town with no other employers"],
            ["No", "Yes", "Quit no matter what. Bad job, better options elsewhere.", "Software engineer getting lowballed — can easily get a new job"],
            ["No", "No", "Stay ONLY if the firm keeps sending them meaningful tasks (low automation)", "Warehouse worker who can't retrain but needs the income"],
            ["Yes", "Yes", "Stay ONLY if automation stays below a threshold", "Senior lawyer — likes the firm but will leave if AI takes the interesting cases"],
        ],
        col_widths=[0.9*inch, 1.1*inch, 2.3*inch, 2.6*inch],
    )

    gap(8)
    sub("Finding 2: Mixed human-AI teams are rarely the best strategy")
    body("<i>Maps to Mahmood's Theorems 3, 4, and 5</i>")
    gap(4)
    body(
        "Just like Mahmood found that cascading between AI models is rarely the best policy, "
        "I expect to find that the firm's best strategy is almost always a clean split: "
        "<b>either give the task to AI or give it to the human — don't mix.</b>"
    )
    body(
        "This goes against the popular narrative that \"human-AI collaboration\" is the future. "
        "The math suggests that clean task separation (AI does X, humans do Y) beats blurry "
        "hybrid setups in most situations."
    )

    gap(8)
    sub("Finding 3: What is cheapest for the firm is not best for workers")
    body("<i>Maps to Mahmood's Proposition 1 (misalignment gap)</i>")
    gap(4)
    body(
        "When the firm picks the automation level that saves them the most money, workers almost "
        "always end up worse off than they could be. The gap is biggest when:"
    )
    bullet("AI is almost as good as humans but way cheaper")
    bullet("Workers are easy to replace (large labor pool)")
    bullet("Workers and firms disagree on which tasks are \"human tasks\" vs. \"AI tasks\"")

    gap(8)
    sub("Finding 4: Companies are tempted to make jobs worse on purpose")
    body("<i>Maps to Mahmood's Proposition 2 (throttling)</i>")
    gap(4)
    body(
        "This is the strongest result. Mahmood proved that AI companies can benefit from "
        "deliberately slowing down their models to push users away. In the labor context, "
        "this means:"
    )
    gap(4)
    bold(
        "If replacing a worker is cheap enough, the firm saves money by deliberately "
        "making the job worse — cutting meaningful tasks, increasing monitoring, reducing "
        "autonomy — until the worker quits \"voluntarily.\""
    )
    gap(4)
    body("The mathematical condition is:")
    bold("Quiet firing is profitable when: R ≤ min{ w_H / q_H , c_A / q_A }")
    gap(4)
    body(
        "In plain English: if it costs less to replace a worker than what you spend per "
        "successful task, the company benefits from pushing workers out. This is \"quiet firing\" "
        "captured in a single equation."
    )

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 6: HOW I CONDUCT THE RESEARCH
    # ═══════════════════════════════════════════════════════════════════
    sec("6. How I Would Conduct the Research")
    line()

    sub("Phase 1: Foundation (Weeks 1–3)")
    bold("Goal: Deeply understand Mahmood's paper and the labor economics context")
    bullet("Re-read and annotate every theorem and proof in Mahmood (ICLR 2026)")
    bullet("Map each variable, assumption, and result to the labor setting")
    bullet("Read 15–20 key papers in labor economics on automation and task allocation")
    bullet("Key references: Acemoglu & Restrepo (2019) on automation and labor; Autor (2015) on task-based framework; Agrawal, Gans & Goldfarb (2019) on AI and jobs")
    bold("Deliverable: Annotated variable mapping document and literature review outline")

    gap(8)
    sub("Phase 2: Model Setup (Weeks 4–6)")
    bold("Goal: Write the formal model section of the paper")
    bullet("Define the Markov chain for human-AI task routing (mirrors Mahmood's Figure 2)")
    bullet("Write closed-form expressions for worker utility, firm cost, success probability, and total cost")
    bullet("Verify that the mathematical structure is identical to Mahmood's — proving the theorems carry over")
    bullet("Identify any places where the labor setting requires modified assumptions (e.g., workers may have contracts, AI quality may improve over time)")
    bold("Deliverable: Complete model section (Sections 3.1–3.3 of the paper)")

    gap(8)
    sub("Phase 3: Results and Interpretation (Weeks 7–10)")
    bold("Goal: Translate all theorems into the labor context and add new insights")
    bullet("Restate Theorems 1–5 with labor variables and provide economic interpretations")
    bullet("Restate Propositions 1–2 (misalignment and quiet firing) with labor interpretations")
    bullet("Identify any NEW results specific to the labor context that do not appear in Mahmood's paper")
    bullet("Create 3–4 figures showing the worker behaviour regimes, firm optimal policy regions, misalignment gap, and quiet firing conditions")
    bold("Deliverable: Complete results and analysis sections (Sections 4–7 of the paper)")

    gap(8)
    sub("Phase 4: Discussion and Writing (Weeks 11–14)")
    bold("Goal: Write introduction, literature review, policy discussion, and conclusion")
    bullet("Write the introduction framing the paper as a labor economics contribution")
    bullet("Complete the literature review connecting to both AI routing and labor economics")
    bullet("Write the policy implications section — what should labor laws, unions, and regulators do?")
    bullet("Revise and polish the full paper to submission quality")
    bold("Deliverable: Complete paper draft ready for Prof. Mahmood's review")

    gap(8)
    sub("Phase 5: Revision and Submission (Weeks 15–16)")
    bold("Goal: Incorporate feedback and prepare for submission")
    bullet("Incorporate Prof. Mahmood's feedback")
    bullet("Prepare supplementary materials and proofs appendix")
    bullet("Format for target venue (Management Science, NeurIPS, or ICLR)")
    bold("Deliverable: Submission-ready paper")

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 7: TIMELINE
    # ═══════════════════════════════════════════════════════════════════
    sec("7. Timeline")
    line()

    make_table(
        ["Weeks", "Phase", "What gets done", "Deliverable"],
        [
            ["1–3", "Foundation", "Deep-read Mahmood's proofs, map variables, read labor economics literature", "Variable mapping + lit review outline"],
            ["4–6", "Model Setup", "Write the formal model, define Markov chain, derive closed-form expressions", "Complete model section"],
            ["7–10", "Results", "Translate all theorems, create figures, find new labor-specific insights", "Complete results sections"],
            ["11–14", "Writing", "Introduction, lit review, policy discussion, full paper draft", "Full paper draft"],
            ["15–16", "Revision", "Incorporate feedback, format for submission", "Submission-ready paper"],
        ],
        col_widths=[0.7*inch, 1.1*inch, 3.0*inch, 2.1*inch],
    )

    gap(10)
    body("<b>Total estimated time: 16 weeks (4 months)</b>")

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 8: WHY THIS IS THE RIGHT PROJECT
    # ═══════════════════════════════════════════════════════════════════
    sec("8. Why This is the Right Project")
    line()

    sub("It builds directly on proven work")
    body(
        "The mathematical foundation is Prof. Mahmood's ICLR 2026 paper — a rigorous, "
        "peer-reviewed framework with full proofs. I am not starting from scratch. I am applying "
        "proven results to a new and important domain."
    )

    gap(6)
    sub("It fits his funded research")
    body(
        "Prof. Mahmood's SSHRC grant focuses on AI and labour market equality. This paper "
        "studies what happens to workers when companies route tasks between humans and AI. "
        "It sits directly within the scope of his funded research program."
    )

    gap(6)
    sub("It addresses the societal issue he cares about")
    body(
        "In our meeting, Prof. Mahmood specifically mentioned societal and social issues. "
        "AI-driven labor displacement is arguably the single biggest societal concern about AI. "
        "The \"quiet firing\" result — that companies can be mathematically incentivized to "
        "degrade jobs — has direct implications for labor policy, union negotiations, and "
        "worker protection laws."
    )

    gap(6)
    sub("It is autonomous and self-directed")
    body(
        "Prof. Mahmood described research with him as autonomous, self-directed, and building "
        "on his work in a new lane. This project takes his exact framework (Stackelberg routing "
        "games) and applies it to a domain he has not yet explored in a full paper (human-AI "
        "task allocation at firms). The framework is his. The application is mine."
    )

    gap(6)
    sub("It is publishable at top venues")
    body(
        "This paper sits at the intersection of operations research, AI, and labor economics — "
        "a space with growing interest and few formal models. Target venues include Management "
        "Science, Manufacturing & Service Operations Management (M&SOM), NeurIPS, and ICLR. "
        "Prof. Mahmood publishes at all of these."
    )

    gap(20)
    line()
    gap(6)
    story.append(Paragraph(
        "Prepared by Nathan Amankwah | March 2026<br/>"
        "For Prof. Rafid Mahmood, Telfer School of Management, University of Ottawa<br/>"
        "GitHub: github.com/nathanamankw/RAFIDRESEARCH",
        styles["SmallCenter"]
    ))

    # ── build ─────────────────────────────────────────────────────────
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
