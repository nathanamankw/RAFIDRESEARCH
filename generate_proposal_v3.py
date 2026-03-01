"""
Generate a research proposal PDF — pitch style.
Part 1: Explains the research idea in plain English.
Part 2: Shows why this is the right project (lane, fit, relevance).
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
DARK    = HexColor("#1a1a2e")
ACCENT  = HexColor("#2c3e7a")
RED     = HexColor("#c0392b")
LIGHT_BG = HexColor("#f4f6fb")
HIGHLIGHT_BG = HexColor("#fff8e1")
DGREY   = HexColor("#2d2d2d")
MGREY   = HexColor("#666666")
LGREY   = HexColor("#dcdcdc")
WHITE   = HexColor("#ffffff")


# ── custom flowables ────────────────────────────────────────────────
class CalloutBox(Flowable):
    """Shaded callout box with left accent bar."""
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


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
    )

    styles = getSampleStyleSheet()
    W = doc.width

    # ── styles ───────────────────────────────────────────────────────
    styles.add(ParagraphStyle(
        "PaperTitle", parent=styles["Title"],
        fontSize=18, leading=24, alignment=TA_CENTER,
        spaceAfter=4, textColor=DARK, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=11, leading=15, alignment=TA_CENTER,
        spaceAfter=2, textColor=MGREY, fontName="Helvetica-Oblique",
    ))
    styles.add(ParagraphStyle(
        "Author", parent=styles["Normal"],
        fontSize=10.5, leading=14, alignment=TA_CENTER,
        spaceAfter=2, textColor=MGREY, fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "SectionHead", parent=styles["Heading1"],
        fontSize=14, leading=18, spaceBefore=20, spaceAfter=10,
        textColor=ACCENT, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "SubHead", parent=styles["Heading2"],
        fontSize=11.5, leading=15, spaceBefore=14, spaceAfter=6,
        textColor=DARK, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY,
        spaceAfter=7, textColor=DGREY, fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "BodyBold", parent=styles["Normal"],
        fontSize=10.5, leading=15.5, alignment=TA_LEFT,
        spaceAfter=3, textColor=DARK, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "BulletItem", parent=styles["Normal"],
        fontSize=10.5, leading=15.5, alignment=TA_LEFT,
        spaceAfter=4, textColor=DGREY, fontName="Helvetica",
        leftIndent=22, bulletIndent=10,
    ))
    styles.add(ParagraphStyle(
        "CalloutText", parent=styles["Normal"],
        fontSize=10.5, leading=15, alignment=TA_LEFT,
        textColor=DGREY, fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "BigQuestion", parent=styles["Normal"],
        fontSize=12, leading=17, alignment=TA_CENTER,
        spaceBefore=6, spaceAfter=6, textColor=ACCENT,
        fontName="Helvetica-BoldOblique",
    ))
    styles.add(ParagraphStyle(
        "SmallNote", parent=styles["Normal"],
        fontSize=9, leading=12, alignment=TA_CENTER,
        spaceAfter=4, textColor=MGREY, fontName="Helvetica",
    ))

    # ── helpers ──────────────────────────────────────────────────────
    story = []

    def sec(title):
        story.append(Paragraph(title, styles["SectionHead"]))

    def sub(title):
        story.append(Paragraph(title, styles["SubHead"]))

    def body(text):
        story.append(Paragraph(text, styles["Body"]))

    def bold(text):
        story.append(Paragraph(text, styles["BodyBold"]))

    def bullet(text):
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{text}", styles["BulletItem"]))

    def question(text):
        story.append(Paragraph(f"\u201c{text}\u201d", styles["BigQuestion"]))

    def gap(pts=8):
        story.append(Spacer(1, pts))

    def line():
        story.append(HRFlowable(width="100%", thickness=0.5, color=LGREY,
                                spaceAfter=10, spaceBefore=10))

    def callout(text, bg=LIGHT_BG, bar=ACCENT):
        p = Paragraph(text, styles["CalloutText"])
        story.append(CalloutBox(W, p, bg_color=bg, bar_color=bar))
        gap(8)

    def highlight(text):
        p = Paragraph(text, styles["CalloutText"])
        story.append(CalloutBox(W, p, bg_color=HIGHLIGHT_BG, bar_color=RED))
        gap(8)

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

    # ==================================================================
    #  TITLE PAGE
    # ==================================================================
    gap(60)
    story.append(Paragraph(
        "What Happens to AI Routing<br/>When the User Is an AI Agent?",
        styles["PaperTitle"]
    ))
    gap(6)
    story.append(Paragraph(
        "A Research Proposal on Multi-Provider Competition<br/>"
        "in the Age of Agentic AI",
        styles["Subtitle"]
    ))
    gap(20)
    story.append(Paragraph("Nathan Amankwah", styles["Author"]))
    story.append(Paragraph("Prepared for Prof. Rafid Mahmood", styles["Author"]))
    story.append(Paragraph("Telfer School of Management &middot; University of Ottawa", styles["Author"]))
    gap(8)
    story.append(Paragraph("March 2026", styles["Author"]))

    gap(40)
    line()
    gap(4)
    callout(
        "<b>In one sentence:</b> Prof. Mahmood's ICLR paper models how one AI company routes "
        "tasks for one human user. This proposal asks: what changes when the user is an AI agent "
        "that can shop across multiple providers at once?"
    )

    story.append(PageBreak())

    # ==================================================================
    #  PART 1 — THE RESEARCH IDEA IN PLAIN ENGLISH
    # ==================================================================
    sec("Part 1 — The Research Idea in Plain English")
    line()

    # -- What Prof. Mahmood showed --
    sub("What Prof. Mahmood's Paper Shows")

    body(
        "In \"Routing, Cascades, and User Choice for LLMs\" (under review at ICLR 2026), "
        "Prof. Mahmood studies a simple but important question: when an AI company like OpenAI "
        "or Anthropic decides which model to send your question to, how does that affect you?"
    )
    body(
        "He sets up a game between two players:"
    )
    bullet(
        "<b>The provider</b> (the AI company) — picks which model handles your task. They can "
        "start with the cheap model and, if it fails, escalate to the expensive one. Their goal: "
        "spend as little money as possible."
    )
    bullet(
        "<b>The user</b> (you, the person) — decides whether to keep trying if the model fails, "
        "or give up. Your goal: get your task done without wasting too much time waiting."
    )
    gap(4)
    body("He finds four key things:")
    bullet(
        "<b>Your patience depends on whether the model is worth your time.</b> If the value you "
        "get from the model is higher than the time you spend waiting, you'll keep trying. If not, "
        "you'll give up."
    )
    bullet(
        "<b>The best strategy for the company is usually simple.</b> Just pick one model and "
        "stick with it — don't bother escalating. Cascading (trying the cheap model first, then "
        "the expensive one) is rarely worth it."
    )
    bullet(
        "<b>What's best for the company is often NOT what's best for you.</b> The company wants "
        "to save money. You want the best answer. These goals conflict. He measures this gap precisely."
    )
    bullet(
        "<b>Companies can cheat by deliberately slowing things down.</b> If the penalty for losing "
        "you is low, the company can make models slower on purpose to get you to give up — "
        "which actually saves them money. This is his scariest finding."
    )

    gap(6)
    callout(
        "<b>The core insight:</b> Routing is not just a technical decision — it's a strategic "
        "game, and the company's cost-saving incentives can directly hurt users."
    )

    # -- What's changing right now --
    sub("What's Changing Right Now (2026)")

    body(
        "Prof. Mahmood's paper models a <b>human</b> user interacting with <b>one</b> provider. "
        "That was an accurate picture of the AI market in 2024. But two things have changed dramatically:"
    )

    bold("Change 1: The \"user\" is increasingly an AI agent, not a person.")
    body(
        "In 2026, a huge and growing share of LLM API calls come from AI agents — software that "
        "calls AI models automatically, without a person typing each prompt. Examples:"
    )
    bullet("<b>Claude Code</b> — Anthropic's coding assistant that makes hundreds of API calls per session.")
    bullet("<b>Devin</b> — an autonomous coding agent that plans, writes, and tests code by calling LLMs.")
    bullet("<b>Cursor</b> — a code editor where AI agents call multiple models behind the scenes.")
    bullet(
        "<b>Autonomous browsing agents</b> — tools that browse the web, fill forms, book flights, "
        "all by chaining LLM calls."
    )
    body(
        "These agents don't get frustrated. They don't get impatient. They don't \"give up\" the way "
        "a human does. They make decisions based on math — cost budgets, quality checks, timeout "
        "rules — not emotions."
    )

    gap(4)
    bold("Change 2: The agent can switch providers instantly.")
    body(
        "A human user subscribes to ChatGPT or Claude and mostly sticks with that one provider. "
        "An AI agent holds API keys for OpenAI, Anthropic, Google, and open-source models "
        "simultaneously. Switching from one provider to another costs the agent nothing — it just "
        "changes which API endpoint it calls. There's no loyalty, no habit, no switching cost."
    )

    gap(6)
    highlight(
        "<b>The big question this research asks:</b><br/><br/>"
        "Prof. Mahmood showed how the routing game works with one provider and one human user. "
        "What happens to every one of his findings when the user is an AI agent that can shop "
        "across multiple competing providers?"
    )

    # -- Why this matters --
    sub("Why This Matters")

    body("This isn't a hypothetical future question. It's happening right now:")
    bullet(
        "<b>OpenAI, Anthropic, and Google are competing for agent traffic</b> — API pricing "
        "wars are front-page tech news in 2026."
    )
    bullet(
        "<b>Agent frameworks are the fastest-growing segment of LLM usage</b> — more tokens are "
        "consumed by agents than by humans in many product categories."
    )
    bullet(
        "<b>Providers are redesigning their APIs for agents</b> — batch endpoints, streaming "
        "protocols, and volume pricing are all aimed at this new customer type."
    )
    bullet(
        "<b>Nobody has the game theory for this market</b> — existing routing models assume "
        "a human user and a single provider. The multi-provider agent game is wide open."
    )

    story.append(PageBreak())

    # -- What we expect to find --
    sub("What We Expect to Find")

    body(
        "By re-examining each of Prof. Mahmood's key results in the new setting, we expect "
        "four main findings:"
    )

    gap(4)
    bold("Finding 1: Most of the user behavior regimes disappear.")
    body(
        "Prof. Mahmood identifies four types of user behavior depending on whether each model "
        "is \"worth the wait\" or not. For a human, waiting is costly — so some models aren't "
        "worth it. For an agent, waiting costs almost nothing. That means the agent almost always "
        "finds both models worth using. Three of the four behavior types effectively collapse into "
        "one: the agent stays and keeps trying."
    )
    callout(
        "<b>What this means:</b> The provider loses a key lever. With human users, the company "
        "could influence your behavior by adjusting the routing strategy. With agents, that "
        "lever disappears — the agent stays regardless. The provider can only compete on cost "
        "and quality, not on manipulating user patience."
    )

    bold("Finding 2: The \"deliberate slowdown\" trick stops working.")
    body(
        "Prof. Mahmood's scariest result is that companies can deliberately slow down their models "
        "to make users give up — saving the company money at the user's expense. This works because "
        "humans are impatient and the penalty for losing one user is low."
    )
    body("Against an AI agent, this breaks for two reasons:")
    bullet(
        "<b>Agents aren't impatient.</b> Making the model slower doesn't bother an agent the way "
        "it bothers a person. The agent just waits."
    )
    bullet(
        "<b>The agent will switch to a competitor.</b> Even if the agent did care about speed, "
        "it would just call a different provider. The penalty for losing an agent isn't \"they "
        "might unsubscribe\" — it's \"they immediately send all their traffic to your rival.\" "
        "That makes the penalty very high, which Prof. Mahmood already showed kills the "
        "slowdown incentive."
    )
    callout(
        "<b>What this means:</b> Competition among providers, combined with agent rationality, "
        "may naturally eliminate the worst behavior Prof. Mahmood identified — without needing "
        "any regulation."
    )

    bold("Finding 3: The gap between \"what's best for users\" and \"what providers do\" changes with competition.")
    body(
        "Prof. Mahmood measures the gap between what would be best for the user and what the "
        "provider actually does. With one provider, this gap can be large. We expect:"
    )
    bullet(
        "With <b>two providers</b>, the gap shrinks but doesn't disappear — each provider is "
        "somewhat constrained by the other."
    )
    bullet(
        "With <b>many providers</b>, the gap approaches zero — any provider that deviates from "
        "what's best for the agent loses all its traffic instantly."
    )
    bullet(
        "With a <b>small number of providers</b> (the realistic case — OpenAI, Anthropic, Google), "
        "there's a risk of implicit coordination — if all providers route to cheap models, the "
        "agent has no better option. Competition helps, but doesn't fully solve the problem."
    )

    bold("Finding 4: Cascading might become a competitive advantage.")
    body(
        "Prof. Mahmood shows that cascading (trying the cheap model first, then escalating) "
        "is rarely optimal for a single provider. But with competition, a provider might offer "
        "cascading as a selling point — \"we always escalate to our best model if the first one "
        "fails\" — to attract agents away from competitors who only use one model. Competition "
        "might make cascading useful in ways it wasn't before."
    )

    story.append(PageBreak())

    # ==================================================================
    #  PART 2 — WHY THIS IS THE RIGHT PROJECT
    # ==================================================================
    sec("Part 2 — Why This Is the Right Project")
    line()

    # -- It's in his exact lane --
    sub("It's Directly in Prof. Mahmood's Research Lane")

    body(
        "This proposal doesn't ask Prof. Mahmood to work on something new. It asks him to take "
        "the exact work he's already done and push it into the most important setting of 2026."
    )

    make_table(
        [
            [Paragraph("<b>What Prof. Mahmood<br/>already built</b>", styles["Body"]),
             Paragraph("<b>What this project does<br/>with it</b>", styles["Body"])],
            [Paragraph("Stackelberg game between provider and user", styles["Body"]),
             Paragraph("Same game, but the user is an AI agent and there are multiple providers competing", styles["Body"])],
            [Paragraph("Net value per pass: is the model worth the wait?", styles["Body"]),
             Paragraph("Same formula, but the agent's wait cost is near zero — changes which regime you're in", styles["Body"])],
            [Paragraph("Four types of user behavior (Theorem 2)", styles["Body"]),
             Paragraph("Re-derive all four — show three collapse when the user is an agent", styles["Body"])],
            [Paragraph("Optimal routing is static, no cascading (Theorems 3\u20135)", styles["Body"]),
             Paragraph("Re-examine — does cascading become useful when providers compete?", styles["Body"])],
            [Paragraph("Misalignment gap (Proposition 1)", styles["Body"]),
             Paragraph("How does competition change the gap? Does more providers = less misalignment?", styles["Body"])],
            [Paragraph("Throttling risk (Proposition 2)", styles["Body"]),
             Paragraph("Show throttling fails against agents + competition — his scariest result gets \"cured\"", styles["Body"])],
            [Paragraph("NeurIPS paper on pricing competition", styles["Body"]),
             Paragraph("This does for <i>routing</i> competition what that paper did for <i>pricing</i> competition", styles["Body"])],
            [Paragraph("SSHRC research on equity and AI", styles["Body"]),
             Paragraph("This studies who gets good AI service and who doesn't — agents vs. humans, big vs. small customers", styles["Body"])],
        ],
        col_widths=[W * 0.45, W * 0.55],
    )

    callout(
        "<b>Every single theorem and proposition in the ICLR paper has a matching question in "
        "this project.</b> The results directly compare to each other. This makes the connection "
        "between the two papers unmistakable."
    )

    # -- It has its own lane --
    sub("It Has Its Own Lane — Nobody Has Done This")

    body("Three reasons this occupies a unique space:")
    bullet(
        "<b>No existing model treats AI agents as the \"user\" in a routing game.</b> "
        "Every routing paper (Chen et al., 2023; Ding et al., 2024; Dekoninck et al., 2025) "
        "assumes a human user who submits one task and waits. The agent-as-user model is new."
    )
    bullet(
        "<b>No existing model combines routing competition with multi-provider access.</b> "
        "Platform competition has been studied (Rochet &amp; Tirole, 2003), and routing has been "
        "studied (Mahmood, 2026), but nobody has put them together. This project sits at the "
        "intersection."
    )
    bullet(
        "<b>The \"agentic AI\" wave is the defining trend of 2026.</b> "
        "This is the first game-theoretic model of how the agentic shift reshapes the economics "
        "of AI inference. Being first to publish here means defining the field."
    )

    # -- It's super relevant --
    sub("It's Immediately Relevant and Applied")

    body("This research speaks directly to decisions being made right now:")

    make_table(
        [
            [Paragraph("<b>Who cares</b>", styles["Body"]),
             Paragraph("<b>What this research tells them</b>", styles["Body"])],
            [Paragraph("AI providers<br/>(OpenAI, Anthropic, Google)", styles["Body"]),
             Paragraph("How to price and route when your fastest-growing customers are agents, not humans", styles["Body"])],
            [Paragraph("Agent developers<br/>(LangChain, Devin, Cursor)", styles["Body"]),
             Paragraph("Which provider to call for which task type — the game theory of smart API shopping", styles["Body"])],
            [Paragraph("Regulators<br/>(EU AI Act, Canada's AIDA)", styles["Body"]),
             Paragraph("Does competition fix the throttling problem, or do governments still need to act?", styles["Body"])],
            [Paragraph("Researchers", styles["Body"]),
             Paragraph("A new framework for studying AI markets — not just models, not just prices, but routing as strategy", styles["Body"])],
        ],
        col_widths=[W * 0.28, W * 0.72],
    )

    # -- It fits his research style --
    sub("It Fits Prof. Mahmood's Research Style Perfectly")

    body("Based on reviewing Prof. Mahmood's full body of work, four things stand out about how he does research:")

    bullet(
        "<b>Clean game theory with closed-form results.</b> "
        "His papers don't use simulations as the main contribution — they prove things. "
        "This project follows the same approach: define the game, solve for the equilibrium, "
        "prove propositions about when competition helps and when it doesn't."
    )
    bullet(
        "<b>Real-world motivation, not abstract theory.</b> "
        "His ICLR paper starts with GPT-5's routing feature. His NeurIPS paper starts with "
        "subscription pricing. This project starts with the fact that AI agents are taking over "
        "the API market in 2026."
    )
    bullet(
        "<b>Societal angle built into the math.</b> "
        "His SSHRC grant is about equity. His throttling result is about companies harming users. "
        "This project asks: does competition protect users, or does it just create new ways to "
        "exploit them? That's the same equity lens applied to a market question."
    )
    bullet(
        "<b>Short, focused papers that prove specific things.</b> "
        "His ICLR paper is tight — one model, a few theorems, clear propositions. This project "
        "follows the same pattern: one extension (multi-provider + agent), a few new results, "
        "direct comparison to his existing work."
    )

    story.append(PageBreak())

    # ==================================================================
    #  PART 3 — PRACTICAL DETAILS
    # ==================================================================
    sec("Part 3 — How the Research Would Work")
    line()

    sub("Approach")
    body("The research follows the same methodology as the ICLR paper:")
    bullet(
        "<b>Step 1 — Define the game.</b> N providers, each with two models, facing one AI agent "
        "that allocates tasks across them. The provider moves first (picks routing), the agent "
        "reacts (picks how to split its traffic)."
    )
    bullet(
        "<b>Step 2 — Solve the agent's best response.</b> Given provider routing strategies, what "
        "does the agent do? How does it split traffic? When does it abandon a provider entirely? "
        "This extends Theorems 1\u20132 of the ICLR paper."
    )
    bullet(
        "<b>Step 3 — Solve the provider equilibrium.</b> Knowing how the agent will react, what "
        "routing strategies do providers choose? This extends Theorems 3\u20135 to a competitive setting."
    )
    bullet(
        "<b>Step 4 — Analyze misalignment and throttling.</b> Does competition close the gap? "
        "Does throttling survive? This extends Propositions 1\u20132."
    )
    bullet(
        "<b>Step 5 — Numerical experiments.</b> Run simulations with real API pricing data "
        "(OpenAI, Anthropic, Google — all public) to illustrate the results."
    )

    sub("Data")
    body("All data needed is publicly available:")
    bullet("API pricing: published on provider websites (per-token costs for each model).")
    bullet("Latency benchmarks: reported by platforms like ArtificialAnalysis.ai.")
    bullet("Agent usage patterns: published by agent frameworks (call volumes, routing behavior).")
    body("No proprietary data, no IRB approval, no access restrictions.")

    sub("Timeline")
    make_table(
        [
            [Paragraph("<b>Phase</b>", styles["Body"]),
             Paragraph("<b>Weeks</b>", styles["Body"]),
             Paragraph("<b>What gets done</b>", styles["Body"])],
            [Paragraph("Literature review + model setup", styles["Body"]),
             Paragraph("1\u20133", styles["Body"]),
             Paragraph("Review routing, agents, and competition literature. Define the game formally.", styles["Body"])],
            [Paragraph("Agent best response", styles["Body"]),
             Paragraph("3\u20137", styles["Body"]),
             Paragraph("Derive how the agent behaves under multi-provider access (extending Theorems 1\u20132).", styles["Body"])],
            [Paragraph("Provider equilibrium", styles["Body"]),
             Paragraph("6\u201310", styles["Body"]),
             Paragraph("Characterize provider strategies under competition (extending Theorems 3\u20135).", styles["Body"])],
            [Paragraph("Misalignment + throttling", styles["Body"]),
             Paragraph("9\u201313", styles["Body"]),
             Paragraph("Analyze welfare, gap, and throttling under competition (extending Props 1\u20132).", styles["Body"])],
            [Paragraph("Simulations + writing", styles["Body"]),
             Paragraph("11\u201316", styles["Body"]),
             Paragraph("Numerical experiments with real data. Write full paper draft.", styles["Body"])],
        ],
        col_widths=[W * 0.28, W * 0.12, W * 0.60],
    )

    sub("Target Venues")
    bullet("<b>Primary:</b> ICLR 2027 or NeurIPS 2027 — follows the trajectory of the ICLR 2026 paper.")
    bullet("<b>Secondary:</b> Management Science or Operations Research — fits the game theory and market design angle.")
    bullet("<b>Workshop option:</b> EC (Economics and Computation) 2027 — bridges CS and economics.")

    story.append(PageBreak())

    # ==================================================================
    #  PART 4 — THE BOTTOM LINE
    # ==================================================================
    sec("Part 4 — The Bottom Line")
    line()

    gap(8)
    highlight(
        "<b>This research takes the exact framework Prof. Mahmood built in his ICLR paper and "
        "brings it into the most important market shift of 2026 — the rise of AI agents as the "
        "primary consumers of AI inference.</b><br/><br/>"

        "It doesn't require new methodology. It doesn't require proprietary data. It doesn't "
        "require departing from the type of research Prof. Mahmood already excels at.<br/><br/>"

        "It asks one clean question — <i>what happens to the routing game when the user is an "
        "agent shopping across competing providers?</i> — and answers it by re-deriving every "
        "result from the ICLR paper in the new setting.<br/><br/>"

        "The result is a paper that:<br/>"
        "&bull;&nbsp;&nbsp;Stands on its own as a study of multi-provider AI markets<br/>"
        "&bull;&nbsp;&nbsp;Directly builds on and cites Prof. Mahmood's foundational work<br/>"
        "&bull;&nbsp;&nbsp;Addresses the most pressing question in AI economics right now<br/>"
        "&bull;&nbsp;&nbsp;Occupies a lane that no other research group has claimed<br/>"
        "&bull;&nbsp;&nbsp;Fits the style, rigor, and venue trajectory of Prof. Mahmood's existing program"
    )

    gap(20)
    line()
    gap(10)
    story.append(Paragraph(
        "Prepared by Nathan Amankwah &middot; March 2026",
        styles["SmallNote"]
    ))
    story.append(Paragraph(
        "For discussion with Prof. Rafid Mahmood, Telfer School of Management",
        styles["SmallNote"]
    ))

    # ── build ────────────────────────────────────────────────────────
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")


if __name__ == "__main__":
    build_pdf()
