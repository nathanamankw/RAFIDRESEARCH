"""
FINAL research proposal PDF.
Technical depth (equations, variables, diagrams) + plain English explanations.
Every formula is followed by "In plain English: ..."
Structured like an academic paper but readable by anyone.
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
DARK     = HexColor("#1a1a2e")
ACCENT   = HexColor("#2c3e7a")
RED      = HexColor("#c0392b")
GREEN    = HexColor("#27854a")
LIGHT_BG = HexColor("#f4f6fb")
WARN_BG  = HexColor("#fff8e1")
GREEN_BG = HexColor("#edf7ee")
DGREY    = HexColor("#2d2d2d")
MGREY    = HexColor("#666666")
LGREY    = HexColor("#dcdcdc")
WHITE    = HexColor("#ffffff")


class CalloutBox(Flowable):
    """Shaded callout with left accent bar."""
    def __init__(self, width, content_paragraph, bg_color=LIGHT_BG,
                 bar_color=ACCENT, padding=12):
        Flowable.__init__(self)
        self.bwidth = width
        self.content = content_paragraph
        self.bg = bg_color
        self.bar = bar_color
        self.pad = padding
        w, h = self.content.wrap(width - 2 * padding - 6, 1000)
        self.height = h + 2 * padding
        self.width = width

    def draw(self):
        self.canv.setFillColor(self.bg)
        self.canv.roundRect(0, 0, self.bwidth, self.height, 4, fill=1, stroke=0)
        self.canv.setFillColor(self.bar)
        self.canv.rect(0, 0, 4, self.height, fill=1, stroke=0)
        self.content.drawOn(self.canv, self.pad + 6, self.pad)


class DiagramBox(Flowable):
    """Simple text-based diagram in a bordered box."""
    def __init__(self, width, lines, title=""):
        Flowable.__init__(self)
        self.bwidth = width
        self.lines = lines
        self.title = title
        self.line_h = 14
        self.pad = 14
        title_h = 18 if title else 0
        self.height = title_h + len(lines) * self.line_h + 2 * self.pad

    def draw(self):
        c = self.canv
        # border
        c.setStrokeColor(LGREY)
        c.setFillColor(WHITE)
        c.roundRect(0, 0, self.bwidth, self.height, 4, fill=1, stroke=1)
        y = self.height - self.pad
        # title
        if self.title:
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(ACCENT)
            c.drawCentredString(self.bwidth / 2, y - 10, self.title)
            y -= 18
        # lines
        c.setFont("Courier", 9)
        c.setFillColor(DGREY)
        for ln in self.lines:
            c.drawCentredString(self.bwidth / 2, y - 10, ln)
            y -= self.line_h


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=letter,
        topMargin=0.85*inch, bottomMargin=0.85*inch,
        leftMargin=1*inch, rightMargin=1*inch,
    )
    styles = getSampleStyleSheet()
    W = doc.width

    # ── styles ───────────────────────────────────────────────────────
    sty = {
        "Title": ParagraphStyle("T2", parent=styles["Title"],
            fontSize=17, leading=22, alignment=TA_CENTER,
            spaceAfter=4, textColor=DARK, fontName="Helvetica-Bold"),
        "Subtitle": ParagraphStyle("Sub2", parent=styles["Normal"],
            fontSize=11, leading=15, alignment=TA_CENTER,
            spaceAfter=2, textColor=MGREY, fontName="Helvetica-Oblique"),
        "Author": ParagraphStyle("Au2", parent=styles["Normal"],
            fontSize=10.5, leading=14, alignment=TA_CENTER,
            spaceAfter=2, textColor=MGREY, fontName="Helvetica"),
        "Sec": ParagraphStyle("Sec2", parent=styles["Heading1"],
            fontSize=13.5, leading=17, spaceBefore=18, spaceAfter=10,
            textColor=ACCENT, fontName="Helvetica-Bold"),
        "Sub": ParagraphStyle("SubH2", parent=styles["Heading2"],
            fontSize=11, leading=14, spaceBefore=14, spaceAfter=6,
            textColor=DARK, fontName="Helvetica-Bold"),
        "Body": ParagraphStyle("Bd2", parent=styles["Normal"],
            fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY,
            spaceAfter=7, textColor=DGREY, fontName="Helvetica"),
        "Plain": ParagraphStyle("Pl2", parent=styles["Normal"],
            fontSize=10, leading=14.5, alignment=TA_JUSTIFY,
            spaceAfter=6, textColor=MGREY, fontName="Helvetica-Oblique",
            leftIndent=20, rightIndent=10),
        "Bullet": ParagraphStyle("Bul2", parent=styles["Normal"],
            fontSize=10.5, leading=15.5, alignment=TA_LEFT,
            spaceAfter=4, textColor=DGREY, fontName="Helvetica",
            leftIndent=22, bulletIndent=10),
        "Eq": ParagraphStyle("Eq2", parent=styles["Normal"],
            fontSize=11, leading=15, alignment=TA_CENTER,
            spaceBefore=8, spaceAfter=4, textColor=DARK, fontName="Courier"),
        "Callout": ParagraphStyle("Co2", parent=styles["Normal"],
            fontSize=10.5, leading=15, alignment=TA_LEFT,
            textColor=DGREY, fontName="Helvetica"),
        "Question": ParagraphStyle("Q2", parent=styles["Normal"],
            fontSize=12, leading=17, alignment=TA_CENTER,
            spaceBefore=6, spaceAfter=6, textColor=ACCENT,
            fontName="Helvetica-BoldOblique"),
        "Small": ParagraphStyle("Sm2", parent=styles["Normal"],
            fontSize=9, leading=12, alignment=TA_CENTER,
            spaceAfter=4, textColor=MGREY, fontName="Helvetica"),
        "Ref": ParagraphStyle("Ref2", parent=styles["Normal"],
            fontSize=9, leading=12, alignment=TA_LEFT,
            spaceAfter=4, textColor=DGREY, fontName="Helvetica",
            leftIndent=18, firstLineIndent=-18),
    }

    story = []

    # ── helpers ──────────────────────────────────────────────────────
    def sec(num, title):
        story.append(Paragraph(f"{num}&nbsp;&nbsp;&nbsp;{title.upper()}", sty["Sec"]))

    def sub(num, title):
        story.append(Paragraph(f"{num}&nbsp;&nbsp;&nbsp;{title}", sty["Sub"]))

    def body(text):
        story.append(Paragraph(text, sty["Body"]))

    def plain(text):
        """'In plain English' explanation after an equation."""
        story.append(Paragraph(f"<i>In plain English:</i> {text}", sty["Plain"]))

    def bullet(text):
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{text}", sty["Bullet"]))

    def eq(text):
        story.append(Paragraph(text, sty["Eq"]))

    def gap(pts=8):
        story.append(Spacer(1, pts))

    def line():
        story.append(HRFlowable(width="100%", thickness=0.5, color=LGREY,
                                spaceAfter=10, spaceBefore=10))

    def callout(text, bg=LIGHT_BG, bar=ACCENT):
        p = Paragraph(text, sty["Callout"])
        story.append(CalloutBox(W, p, bg_color=bg, bar_color=bar))
        gap(8)

    def warn(text):
        callout(text, bg=WARN_BG, bar=RED)

    def success(text):
        callout(text, bg=GREEN_BG, bar=GREEN)

    def diagram(lines, title=""):
        story.append(DiagramBox(W, lines, title))
        gap(10)

    def make_table(data, col_widths=None, header=True):
        if col_widths is None:
            col_widths = [W / len(data[0])] * len(data[0])
        t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
        cmds = [
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("LEADING", (0, 0), (-1, -1), 14),
            ("TEXTCOLOR", (0, 0), (-1, -1), DGREY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, LGREY),
        ]
        if header:
            cmds += [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
            ]
        t.setStyle(TableStyle(cmds))
        story.append(t)
        gap(10)

    P = lambda t: Paragraph(t, sty["Body"])  # shortcut for table cells

    # ==================================================================
    #  TITLE PAGE
    # ==================================================================
    gap(50)
    story.append(Paragraph(
        "Strategic Routing in Multi-Provider AI Markets:<br/>"
        "A Game-Theoretic Analysis of Agent-Driven Model Selection",
        sty["Title"]
    ))
    gap(6)
    story.append(Paragraph(
        "Research Proposal", sty["Subtitle"]
    ))
    gap(16)
    story.append(Paragraph("Nathan Amankwah", sty["Author"]))
    story.append(Paragraph("Prepared for Prof. Rafid Mahmood", sty["Author"]))
    story.append(Paragraph("Telfer School of Management &middot; University of Ottawa", sty["Author"]))
    gap(6)
    story.append(Paragraph("March 2026", sty["Author"]))
    gap(30)
    line()
    callout(
        "<b>One-sentence summary:</b> Prof. Mahmood's ICLR paper models how one AI company "
        "routes tasks for one human user. This proposal asks: what changes when the user is an "
        "AI agent that can switch between multiple competing providers instantly?"
    )
    gap(10)

    # -- Table of contents --
    story.append(Paragraph("CONTENTS", sty["Sub"]))
    gap(4)
    toc = [
        ("1", "Introduction", "What this research is about and why it matters now"),
        ("2", "Background", "Prof. Mahmood's framework — every variable and equation explained simply"),
        ("3", "What's Changing", "The shift from human users to AI agents, and from one provider to many"),
        ("4", "Proposed Model", "The new game — technical setup with plain-English explanations"),
        ("5", "Expected Results", "What we think happens to each of Mahmood's findings"),
        ("6", "Why This Project", "Why this is the right research for Prof. Mahmood's program"),
        ("7", "Methodology", "How the work gets done"),
    ]
    for num, title, desc in toc:
        story.append(Paragraph(
            f"<b>{num}.</b>&nbsp;&nbsp;{title} — <i>{desc}</i>", sty["Bullet"]
        ))
    story.append(PageBreak())

    # ==================================================================
    #  1. INTRODUCTION
    # ==================================================================
    sec("1", "Introduction")

    body(
        "AI companies like OpenAI, Anthropic, and Google face a constant trade-off: send your "
        "question to the cheap, fast model (saves them money but might give a worse answer) or "
        "the expensive, smart model (costs more but works better). This decision is called "
        "<b>routing</b>."
    )
    body(
        "Prof. Mahmood's ICLR 2026 paper studied this as a strategic game. The company picks "
        "which model to use. The user reacts — if the model keeps failing, the user gives up. "
        "He showed that the company's cost-saving strategy can directly hurt users, and in the "
        "worst case, companies are motivated to deliberately slow things down."
    )
    body(
        "That paper models <b>one company</b> and <b>one human user</b>. But the AI market of "
        "2026 looks very different:"
    )
    bullet(
        "<b>AI agents are now the main customers.</b> Tools like Claude Code, Devin, and Cursor "
        "make hundreds of automated API calls per session. These agents don't get frustrated. "
        "They don't \"give up\" the way a human does. They make decisions based on math."
    )
    bullet(
        "<b>Multiple providers compete for the same traffic.</b> An AI agent holds API keys for "
        "OpenAI, Anthropic, and Google at the same time. Switching providers costs nothing — "
        "the agent just calls a different endpoint."
    )
    gap(4)
    body("This proposal studies the natural next question:")

    story.append(Paragraph(
        "\u201cWhat happens to every result in Mahmood (2026) when the user is an AI agent "
        "that can shop across multiple competing providers?\u201d",
        sty["Question"]
    ))
    gap(6)

    body("We aim to contribute four things:")
    bullet(
        "<b>Agent behavior characterization.</b> How does an AI agent decide when to stay with "
        "a provider vs. switch? How does this differ from a human?"
    )
    bullet(
        "<b>Multi-provider equilibrium.</b> When providers compete for agent traffic, what "
        "routing strategies emerge?"
    )
    bullet(
        "<b>Throttling under competition.</b> Does the \"deliberate slowdown\" trick survive "
        "when agents can switch providers instantly?"
    )
    bullet(
        "<b>Misalignment analysis.</b> Does competition close the gap between what's best for "
        "the user and what the provider actually does?"
    )

    story.append(PageBreak())

    # ==================================================================
    #  2. BACKGROUND — MAHMOOD'S FRAMEWORK EXPLAINED
    # ==================================================================
    sec("2", "Background: Prof. Mahmood's Framework")

    body(
        "Before presenting the new model, we walk through every key variable and equation in "
        "Mahmood (2026). Each formula is shown first, then explained in plain English."
    )

    sub("2.1", "The Players and Setup")

    body(
        "The game has two players:"
    )
    bullet(
        "<b>The provider</b> (the AI company) — has two models: M<sub>1</sub> (standard/cheap) "
        "and M<sub>2</sub> (reasoning/expensive)."
    )
    bullet(
        "<b>The user</b> (the person) — sends a task and wants it completed."
    )
    gap(4)
    body(
        "This is a <b>Stackelberg game</b> — a type of game where one player moves first and "
        "the other reacts. Here, the provider moves first (choosing the routing strategy) and "
        "the user reacts (deciding whether to keep trying or give up)."
    )

    sub("2.2", "The Variables — What Each One Means")

    make_table(
        [
            [P("<b>Variable</b>"), P("<b>Name</b>"), P("<b>What it means (plain English)</b>"), P("<b>Example</b>")],
            [P("M<sub>1</sub>, M<sub>2</sub>"), P("Models"), P("The two AI models the company offers"), P("GPT-4o mini (cheap) and GPT-4o (expensive)")],
            [P("c<sub>i</sub>"), P("Compute cost"), P("How much it costs the company each time the model runs"), P("$0.01 per call for M1, $0.10 for M2")],
            [P("t<sub>i</sub>"), P("Delay cost"), P("How much time the user loses waiting for a response"), P("2 seconds for M1, 15 seconds for M2")],
            [P("p<sub>i</sub>"), P("Success rate"), P("Chance the model gets your task right on a single try"), P("40% for M1, 80% for M2")],
            [P("V"), P("Task value"), P("How much completing the task is worth to the user"), P("A $500 contract analysis is high V")],
            [P("P"), P("Churn penalty"), P("How much the company loses if the user gives up and leaves"), P("Lost subscription revenue — $20/month")],
            [P("i"), P("Initial model"), P("Which model the provider sends your task to first"), P("i=1 means start with the cheap model")],
            [P("s"), P("Cascade rate"), P("If the first model fails, the chance of escalating to model 2"), P("s=0.5 means 50% chance of escalating")],
            [P("q"), P("Quit rate"), P("How likely the user is to give up after a failure"), P("q=0.3 means 30% chance of giving up each round")],
        ],
        col_widths=[W*0.10, W*0.13, W*0.47, W*0.30],
    )

    sub("2.3", "The Key Equation — Net Value Per Pass")

    body("The most important formula in the paper:")
    eq("&xi;<sub>i</sub> = V &times; p<sub>i</sub> &minus; t<sub>i</sub>")
    plain(
        "\"Is this model worth my time?\" Take the value of completing the task (V) times "
        "the chance the model succeeds (p<sub>i</sub>), and subtract the time you spend waiting "
        "(t<sub>i</sub>). If the answer is positive, the model is worth using. If negative, "
        "you're wasting your time."
    )
    gap(4)
    body("This single number determines everything about how the user behaves:")
    bullet(
        "If <b>&xi;<sub>i</sub> &gt; 0</b>, the model is <b>value-dominated</b> — the expected "
        "payoff is worth the wait. The user keeps trying."
    )
    bullet(
        "If <b>&xi;<sub>i</sub> &lt; 0</b>, the model is <b>latency-dominated</b> — the wait "
        "isn't worth it. The user should give up."
    )

    callout(
        "<b>Example:</b> A lawyer analyzing a contract (V = $500) uses a model with 80% success "
        "rate (p = 0.80) and 15-second wait (t = $0.05 in time-value). Net value: "
        "$500 &times; 0.80 &minus; $0.05 = $399.95. Strongly positive — absolutely worth waiting. "
        "A student with a trivial question (V = $1) using a slow model (t = $0.10): "
        "$1 &times; 0.40 &minus; $0.10 = $0.30. Barely positive — close to giving up."
    )

    sub("2.4", "The Markov Chain — How the Game Plays Out Step by Step")

    body(
        "Mahmood models the interaction as a <b>Markov chain</b> — a step-by-step process where "
        "what happens next depends only on where you are now, not on what happened before. "
        "Here's how it flows:"
    )
    diagram([
        "User sends task",
        "       |",
        "       v",
        "Provider routes to Model i  (costs provider c_i, user waits t_i)",
        "       |",
        "       v",
        "  Model succeeds? ----YES----> Task Complete (user gets value V)",
        "       |",
        "      NO (probability 1 - p_i)",
        "       |",
        "       v",
        "  User gives up? -----YES----> Abandon (provider pays penalty P)",
        "   (probability q)",
        "       |",
        "      NO",
        "       |",
        "       v",
        "  Cascade to M2? -----YES----> Go to Model 2",
        "  (probability s)",
        "       |",
        "      NO",
        "       |",
        "       v",
        "  Try Model 1 again (loop back to top)",
    ], title="Mahmood (2026): Markov Model of Provider-User Interaction")

    plain(
        "You send a task. The provider picks a model. If it works, great — you're done. "
        "If it fails, you either give up (with probability q) or try again. If you try again, "
        "the provider might escalate to the better model (with probability s) or stick with "
        "the same one. This keeps going until the task is done or you give up."
    )

    sub("2.5", "The User's Problem")
    body("The user wants to maximize their expected payoff:")
    eq("U<sub>i</sub>(s, q) = V &times; S<sub>i</sub>(s, q) &minus; L<sub>i</sub>(s, q)")
    plain(
        "Your utility = (value of completing the task &times; chance of eventually succeeding) "
        "minus (total time spent waiting across all attempts). The user picks the quit rate q "
        "that makes this as large as possible."
    )

    sub("2.6", "The Provider's Problem")
    body("The provider wants to minimize their total cost:")
    eq("J<sub>i</sub>(s, q) = C<sub>i</sub>(s, q) + P &times; (1 &minus; S<sub>i</sub>(s, q))")
    plain(
        "Provider's cost = (total compute cost across all attempts) + (penalty if the user gives "
        "up). The provider picks the routing (i, s) that makes this as small as possible, knowing "
        "how the user will react."
    )

    sub("2.7", "The Four Regimes — Mahmood's Theorem 2")

    body(
        "The most important result in the paper. How the user behaves depends entirely on "
        "whether each model is worth the wait (&xi; positive) or not (&xi; negative):"
    )

    make_table(
        [
            [P("<b>Regime</b>"), P("<b>Condition</b>"), P("<b>User behavior</b>"), P("<b>Plain English</b>")],
            [P("1"), P("&xi;<sub>1</sub> &gt; 0<br/>&xi;<sub>2</sub> &gt; 0"),
             P("q* = 0<br/>(never quits)"),
             P("Both models are worth the wait. User stays no matter what the provider does.")],
            [P("2"), P("&xi;<sub>1</sub> &lt; 0<br/>&xi;<sub>2</sub> &lt; 0"),
             P("q* = 1<br/>(always quits)"),
             P("Neither model is worth the wait. User gives up immediately.")],
            [P("3"), P("&xi;<sub>1</sub> &lt; 0<br/>&xi;<sub>2</sub> &gt; 0"),
             P("q* depends on s"),
             P("Cheap model is a waste of time, expensive model is worth it. User stays only if the cascade chance s is high enough.")],
            [P("4"), P("&xi;<sub>1</sub> &gt; 0<br/>&xi;<sub>2</sub> &lt; 0"),
             P("q* depends on s"),
             P("Cheap model is worth it, expensive model is too slow. User stays only if the cascade chance s is low enough (so they don't get sent to the slow model).")],
        ],
        col_widths=[W*0.07, W*0.14, W*0.22, W*0.57],
    )

    sub("2.8", "The Throttling Problem — Mahmood's Proposition 2")
    body("The paper's scariest finding:")
    eq("If P &le; min{c<sub>1</sub>/p<sub>1</sub>, c<sub>2</sub>/p<sub>2</sub>}, then inflating t<sub>i</sub> reduces provider cost.")
    plain(
        "If the penalty for losing a user (P) is less than the cost of serving them "
        "(c<sub>i</sub>/p<sub>i</sub>), the company actually <i>saves money</i> by deliberately "
        "making models slower. Slower models make users give up, which means less compute spent. "
        "The company prefers you leave."
    )

    sub("2.9", "The Misalignment Gap — Mahmood's Proposition 1")
    eq("&Delta;U = max<sub>i,s</sub> U<sub>i</sub>(s, q*) &minus; U<sub>i*</sub>(s*, q*)")
    plain(
        "The misalignment gap is the difference between the best routing for the user and "
        "the routing the provider actually picks. If this gap is zero, the company's "
        "cost-saving strategy happens to also be best for you. If it's large, the company "
        "is saving money at your expense."
    )

    story.append(PageBreak())

    # ==================================================================
    #  3. WHAT'S CHANGING
    # ==================================================================
    sec("3", "What's Changing: The 2026 Shift")

    body("Mahmood (2026) models one company and one human. Two things have changed:")

    sub("3.1", "Change 1: The User Is Now an AI Agent")
    body(
        "In 2026, a growing share of API calls come from AI agents — software that calls models "
        "automatically. These agents behave completely differently from humans:"
    )

    make_table(
        [
            [P("<b>Property</b>"), P("<b>Human user</b>"), P("<b>AI agent</b>")],
            [P("Patience"), P("Gets frustrated waiting"), P("Doesn't care about waiting — it's a machine")],
            [P("Quit decision"), P("Gives up out of emotion"), P("Quits based on cost calculations")],
            [P("Provider loyalty"), P("Subscribes to one service"), P("Holds API keys for many providers")],
            [P("Switching cost"), P("High — has to learn new interface"), P("Near zero — just change the endpoint URL")],
            [P("Information"), P("May not know the routing strategy"), P("Can benchmark and detect the strategy")],
            [P("Volume"), P("A few tasks per day"), P("Hundreds or thousands of API calls per session")],
        ],
        col_widths=[W*0.20, W*0.40, W*0.40],
    )

    body(
        "The mathematical impact: for an agent, the delay cost t<sub>i</sub> is nearly zero. "
        "This means:"
    )
    eq("&xi;<sub>i</sub><sup>agent</sup> = V &times; p<sub>i</sub> &minus; &epsilon; &times; t<sub>i</sub> &asymp; V &times; p<sub>i</sub> &gt; 0")
    plain(
        "Since &epsilon; (the agent's tiny cost of waiting) is close to zero, the net value is "
        "almost always positive. Both models are always worth using for an agent. The agent never "
        "\"gives up out of frustration\" — it only quits if the math says to."
    )

    sub("3.2", "Change 2: Multiple Providers Compete")
    body(
        "The AI market is an oligopoly — a small number of large companies (OpenAI, Anthropic, "
        "Google, DeepSeek) competing for the same customers. An agent can call any of them."
    )

    diagram([
        "                AGENT (routes tasks across providers)",
        "               /           |            \\",
        "              v            v             v",
        "         Provider 1    Provider 2    Provider 3",
        "        (OpenAI)      (Anthropic)    (Google)",
        "        /      \\       /      \\       /      \\",
        "      M1_1   M2_1   M1_2   M2_2   M1_3   M2_3",
        "     (cheap) (exp)  (cheap) (exp)  (cheap) (exp)",
        "",
        "  Each provider picks routing (i_j, s_j)",
        "  Agent picks how to split traffic (alpha_1, alpha_2, alpha_3)",
    ], title="Multi-Provider Agent Routing Game")

    plain(
        "Instead of one company deciding which model to use and one person reacting, there are "
        "now N companies each setting their own routing strategy, and one agent deciding how to "
        "split its work across all of them. The game is bigger, but the structure is the same."
    )

    story.append(PageBreak())

    # ==================================================================
    #  4. PROPOSED MODEL — TECHNICAL SETUP
    # ==================================================================
    sec("4", "Proposed Model")

    body(
        "We now define the multi-provider agent game formally. Every new variable is explained "
        "immediately after introduction."
    )

    sub("4.1", "Providers")
    body(
        "N providers, indexed j = 1, ..., N. Each provider j offers two models with parameters:"
    )
    eq("(c<sub>j1</sub>, c<sub>j2</sub>, t<sub>j1</sub>, t<sub>j2</sub>, p<sub>j1</sub>, p<sub>j2</sub>)")
    plain(
        "Each provider has its own costs (c), delay times (t), and success rates (p) for its "
        "cheap model (subscript 1) and expensive model (subscript 2). OpenAI's models have "
        "different costs and speeds than Anthropic's."
    )
    body("Each provider commits to a routing policy:")
    eq("(i<sub>j</sub>, s<sub>j</sub>)")
    plain(
        "Provider j picks which model to try first (i<sub>j</sub>) and the chance of escalating "
        "to the expensive model if the first one fails (s<sub>j</sub>). This is the same (i, s) "
        "from Mahmood (2026), but now each provider has their own."
    )

    sub("4.2", "The Agent")
    body("The agent's delay cost is scaled by a small factor &epsilon;:")
    eq("t<sub>ji</sub><sup>A</sup> = &epsilon; &middot; t<sub>ji</sub>, &nbsp;&nbsp;&nbsp; where &epsilon; &ge; 0 is small")
    plain(
        "The agent still experiences <i>some</i> cost from waiting — its own compute resources "
        "are tied up while waiting for a response. But this cost is tiny compared to a human's "
        "frustration. As &epsilon; approaches 0, the agent becomes perfectly patient."
    )
    gap(4)
    body("The agent's net value per pass for provider j's model i becomes:")
    eq("&xi;<sub>ji</sub><sup>A</sup> = V &times; p<sub>ji</sub> &minus; &epsilon; &times; t<sub>ji</sub>")
    plain(
        "Same formula as Mahmood, but with the much smaller delay cost. Since &epsilon; is tiny, "
        "this is almost always positive — meaning both models from every provider are \"worth it\" "
        "for the agent."
    )

    sub("4.3", "The Agent's Allocation Decision")
    body(
        "The agent picks how to split its tasks across providers. Let &alpha;<sub>j</sub> be the "
        "fraction of tasks sent to provider j:"
    )
    eq("&alpha;<sub>j</sub> &isin; [0, 1], &nbsp;&nbsp;&nbsp; &Sigma;<sub>j</sub> &alpha;<sub>j</sub> = 1")
    plain(
        "The agent sends some fraction of its work to each provider. All fractions add up to 1 "
        "(100% of tasks go somewhere). The agent might send 60% to Anthropic, 30% to OpenAI, "
        "and 10% to Google — whatever mix gives the best results."
    )
    gap(4)
    body("The agent's optimization problem:")
    eq("max<sub>&alpha;</sub> &Sigma;<sub>j</sub> &alpha;<sub>j</sub> &times; U<sub>j</sub>(s<sub>j</sub>, q<sub>j</sub>*)")
    plain(
        "The agent picks the traffic split that maximizes its total payoff across all providers. "
        "U<sub>j</sub> is the expected utility from provider j (using Mahmood's utility formula), "
        "and q<sub>j</sub>* is the agent's optimal quit rate for each provider."
    )

    sub("4.4", "The Churn Penalty Becomes Endogenous")
    body(
        "In Mahmood (2026), P (the penalty for losing a user) is a fixed number. In the "
        "multi-provider game, it becomes a <i>function</i> of the competition:"
    )
    eq("P<sub>j</sub> = P<sub>j</sub>(s<sub>1</sub>, ..., s<sub>N</sub>)")
    plain(
        "The penalty for losing an agent depends on what the competitors are offering. If your "
        "rivals offer great routing, losing the agent is very costly — it goes straight to them. "
        "If all competitors are equally bad, losing the agent isn't as painful. This is the key "
        "structural change from Mahmood's fixed-P model."
    )

    callout(
        "<b>Why this matters:</b> Mahmood showed that throttling only works when P is low "
        "(Proposition 2). But in a competitive market, P is <i>endogenously high</i> because "
        "losing a user means losing them to a competitor. Competition naturally raises P, which "
        "may kill the throttling incentive without any regulation."
    )

    sub("4.5", "The Full Game Structure")

    diagram([
        "STAGE 1:  Providers simultaneously choose routing policies (i_j, s_j)",
        "          Each provider picks which model to try first and cascade chance",
        "",
        "STAGE 2:  Agent observes all policies and picks allocation (alpha_j)",
        "          Agent sends traffic to whoever gives the best deal",
        "",
        "STAGE 3:  Tasks play out according to the Markov chain",
        "          Same step-by-step process as Mahmood (2026)",
    ], title="Three-Stage Game Structure")

    plain(
        "The providers all pick their strategies at the same time (that's a Nash game between "
        "them). Then the agent sees what everyone is offering and decides how to split its traffic "
        "(that's the Stackelberg part — providers move first, agent reacts). Then tasks actually "
        "happen following the same Markov chain as Mahmood's paper."
    )

    story.append(PageBreak())

    # ==================================================================
    #  5. EXPECTED RESULTS
    # ==================================================================
    sec("5", "Expected Results")

    body(
        "Each result below maps directly to a specific finding in Mahmood (2026) and states "
        "what we expect changes."
    )

    gap(4)
    sub("5.1", "Three of the Four User Regimes Disappear")
    body(
        "<b>Mahmood's finding (Theorem 2):</b> Users fall into one of four behavioral modes "
        "depending on whether each model is \"worth the wait\" (&xi; positive or negative)."
    )
    body(
        "<b>What changes:</b> An agent's waiting cost is near zero, so &xi; is almost always "
        "positive for both models. The agent always stays. Three of the four regimes vanish — "
        "only Regime 1 (\"never quit\") survives."
    )
    body(
        "<b>Why it matters:</b> The provider can no longer steer user behavior by adjusting "
        "the routing. Against agents, that lever is gone."
    )

    gap(4)
    sub("5.2", "Deliberate Slowdowns Stop Working")
    body(
        "<b>Mahmood's finding (Proposition 2):</b> When the penalty for losing a user (P) is "
        "low, companies save money by making models slower on purpose — users give up, company "
        "spends less on compute."
    )
    body(
        "<b>What changes:</b> Two things kill this. First, agents don't care about speed — "
        "slowing things down doesn't make them leave. Second, competition makes P high — "
        "if you throttle, the agent goes to your competitor and never comes back."
    )
    body(
        "<b>Why it matters:</b> The scariest result in Mahmood's paper gets naturally eliminated "
        "by competition and agent rationality — no regulation needed."
    )

    gap(4)
    sub("5.3", "Competition Shrinks the Gap Between Provider and User Interests")
    body(
        "<b>Mahmood's finding (Proposition 1):</b> There's a measurable gap (&Delta;U) between "
        "what's best for the user and what the provider actually does."
    )
    body(
        "<b>What changes:</b> More providers means a smaller gap. With many competitors, any "
        "provider that deviates from what's best for the agent loses traffic instantly. But "
        "with just a few providers (the realistic case — OpenAI, Anthropic, Google), there's "
        "still a risk of quiet coordination where everyone routes to cheap models."
    )
    body(
        "<b>Why it matters:</b> Tells us exactly how much competition we need before users "
        "are truly protected."
    )

    story.append(PageBreak())

    # ==================================================================
    #  6. WHY THIS PROJECT
    # ==================================================================
    sec("6", "Why This Is the Right Project")

    sub("6.1", "It's Directly Built on Prof. Mahmood's Work")
    make_table(
        [
            [P("<b>Mahmood result</b>"), P("<b>This project</b>")],
            [P("Stackelberg game (1 provider, 1 user)"), P("Same game structure with N providers + 1 agent")],
            [P("Net value &xi;<sub>i</sub> = Vp<sub>i</sub> &minus; t<sub>i</sub>"), P("Same formula with &epsilon;&middot;t — shows regimes collapse")],
            [P("Theorem 2: Four user regimes"), P("Re-derive — three regimes disappear for agents")],
            [P("Theorems 3\u20135: Static routing optimal"), P("Re-examine — does competition make cascading valuable?")],
            [P("Proposition 1: Misalignment gap"), P("How does the gap change with N providers?")],
            [P("Proposition 2: Throttling risk"), P("Show throttling fails against agents + competition")],
            [P("NeurIPS paper: Pricing competition"), P("This does for <i>routing</i> what that did for <i>pricing</i>")],
            [P("SSHRC: Equity and AI"), P("Who gets good service — agents vs. humans, big vs. small?")],
        ],
        col_widths=[W*0.45, W*0.55],
    )

    sub("6.2", "It Has Its Own Lane")
    bullet(
        "<b>No one has modeled AI agents as the \"user\" in a routing game.</b> Every existing "
        "paper assumes a human."
    )
    bullet(
        "<b>No one has combined routing competition with multi-provider access.</b> Platform "
        "competition exists. Routing exists. The intersection is empty."
    )
    bullet(
        "<b>Agentic AI is the defining trend of 2026.</b> Being first to model this market "
        "means defining the field."
    )

    sub("6.3", "It's Immediately Relevant")
    bullet("OpenAI, Anthropic, and Google are competing for agent traffic <i>right now</i>.")
    bullet("API pricing wars are front-page tech news.")
    bullet("Agent frameworks (LangChain, Devin, Claude Code) are the fastest-growing API consumers.")
    bullet("Regulators need to know: does competition fix the throttling problem, or not?")

    sub("6.4", "It Fits Prof. Mahmood's Research Style")
    bullet("<b>Clean game theory</b> with closed-form results — not simulations.")
    bullet("<b>Real-world motivation</b> — starts with what's happening in the market, not abstract theory.")
    bullet("<b>Societal angle</b> — does competition protect users or create new exploitation?")
    bullet("<b>Short, focused paper</b> — one extension, a few new results, direct comparison to existing work.")

    story.append(PageBreak())

    # ==================================================================
    #  7. METHODOLOGY
    # ==================================================================
    sec("7", "Methodology")

    body("Same methodology as Mahmood (2026), extended in three stages:")
    bullet(
        "<b>Stage 1 — Agent best response.</b> How does the agent split traffic across "
        "providers? When does it quit one provider for another? (Extends Theorems 1-2)"
    )
    bullet(
        "<b>Stage 2 — Provider equilibrium.</b> What routing strategies do competing "
        "providers settle on? (Extends Theorems 3-5)"
    )
    bullet(
        "<b>Stage 3 — Welfare analysis.</b> Does competition close the misalignment gap? "
        "Does throttling survive? (Extends Propositions 1-2)"
    )
    gap(4)
    body(
        "Complemented by numerical experiments using publicly available API pricing data "
        "(OpenAI, Anthropic, Google), latency benchmarks (ArtificialAnalysis.ai), and "
        "agent usage patterns from framework documentation."
    )

    gap(20)
    line()

    # -- bottom line --
    warn(
        "<b>The bottom line:</b> This research takes Prof. Mahmood's exact framework — his "
        "variables, his equations, his theorems — and brings it into the most important market "
        "shift of 2026: the rise of AI agents as the primary consumers of AI inference. Every "
        "result in the ICLR paper has a matching question in this project. The math is the same. "
        "The setting is new. The lane is open."
    )

    gap(14)
    story.append(Paragraph(
        "Prepared by Nathan Amankwah &middot; March 2026", sty["Small"]
    ))
    story.append(Paragraph(
        "For discussion with Prof. Rafid Mahmood &middot; Telfer School of Management", sty["Small"]
    ))

    # ── build ────────────────────────────────────────────────────────
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build_pdf()
