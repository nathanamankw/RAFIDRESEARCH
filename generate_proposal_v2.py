"""
Generate a research proposal PDF at academic paper quality.
Matches the structure and tone of Mahmood (ICLR 2026).
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
ACCENT = HexColor("#c0392b")
LIGHT_BG = HexColor("#f9f9f9")
DGREY  = HexColor("#333333")
MGREY  = HexColor("#666666")
LGREY  = HexColor("#e8e8e8")
WHITE  = HexColor("#ffffff")

# ── custom flowables ────────────────────────────────────────────────
class ShadedBox(Flowable):
    """A shaded box with text — used for key definitions and findings."""
    def __init__(self, width, content_paragraph, bg_color=LIGHT_BG, padding=10):
        Flowable.__init__(self)
        self.width = width
        self.content = content_paragraph
        self.bg = bg_color
        self.pad = padding
        # Calculate height
        w, h = self.content.wrap(width - 2*padding, 1000)
        self.height = h + 2*padding

    def draw(self):
        self.canv.setFillColor(self.bg)
        self.canv.setStrokeColor(LGREY)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)
        self.content.drawOn(self.canv, self.pad, self.pad)


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=letter,
        topMargin=0.9*inch,
        bottomMargin=0.9*inch,
        leftMargin=1*inch,
        rightMargin=1*inch,
    )

    styles = getSampleStyleSheet()
    W = doc.width

    # ── styles ───────────────────────────────────────────────────────
    styles.add(ParagraphStyle(
        "PaperTitle", parent=styles["Title"],
        fontSize=17, leading=22, alignment=TA_CENTER,
        spaceAfter=6, textColor=DARK,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Author", parent=styles["Normal"],
        fontSize=11, leading=14, alignment=TA_CENTER,
        spaceAfter=2, textColor=MGREY,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "SectionHead", parent=styles["Heading1"],
        fontSize=13, leading=17, spaceBefore=18, spaceAfter=8,
        textColor=DARK, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "SubHead", parent=styles["Heading2"],
        fontSize=11, leading=14, spaceBefore=12, spaceAfter=6,
        textColor=DARK, fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=10, leading=14.5, alignment=TA_JUSTIFY,
        spaceAfter=6, textColor=DGREY,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        "BodyIndent", parent=styles["Normal"],
        fontSize=10, leading=14.5, alignment=TA_JUSTIFY,
        spaceAfter=4, textColor=DGREY,
        fontName="Helvetica",
        leftIndent=20,
    ))
    styles.add(ParagraphStyle(
        "BulletItem", parent=styles["Normal"],
        fontSize=10, leading=14.5, alignment=TA_LEFT,
        spaceAfter=3, textColor=DGREY,
        fontName="Helvetica",
        leftIndent=24, bulletIndent=12,
    ))
    styles.add(ParagraphStyle(
        "AbstractLabel", parent=styles["Normal"],
        fontSize=10, leading=14, fontName="Helvetica-Bold",
        textColor=DARK, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "AbstractBody", parent=styles["Normal"],
        fontSize=10, leading=14, alignment=TA_JUSTIFY,
        spaceAfter=10, textColor=DGREY,
        fontName="Helvetica",
        leftIndent=0, rightIndent=0,
    ))
    styles.add(ParagraphStyle(
        "Equation", parent=styles["Normal"],
        fontSize=10, leading=14, alignment=TA_CENTER,
        spaceAfter=8, spaceBefore=8,
        textColor=DARK, fontName="Courier",
    ))
    styles.add(ParagraphStyle(
        "Caption", parent=styles["Normal"],
        fontSize=9, leading=12, alignment=TA_CENTER,
        spaceAfter=10, textColor=MGREY,
        fontName="Helvetica-Oblique",
    ))
    styles.add(ParagraphStyle(
        "RefItem", parent=styles["Normal"],
        fontSize=9, leading=12, alignment=TA_LEFT,
        spaceAfter=4, textColor=DGREY,
        fontName="Helvetica",
        leftIndent=18, firstLineIndent=-18,
    ))
    styles.add(ParagraphStyle(
        "Footer", parent=styles["Normal"],
        fontSize=8, leading=10, alignment=TA_CENTER,
        textColor=MGREY, fontName="Helvetica",
    ))

    # ── helper functions ─────────────────────────────────────────────
    story = []

    def sec(num, title):
        story.append(Paragraph(f"{num}&nbsp;&nbsp;&nbsp;{title.upper()}", styles["SectionHead"]))

    def sub(num, title):
        story.append(Paragraph(f"{num}&nbsp;&nbsp;&nbsp;{title}", styles["SubHead"]))

    def body(text):
        story.append(Paragraph(text, styles["Body"]))

    def bodyindent(text):
        story.append(Paragraph(text, styles["BodyIndent"]))

    def bullet(text):
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{text}", styles["BulletItem"]))

    def eq(text):
        story.append(Paragraph(text, styles["Equation"]))

    def gap(pts=6):
        story.append(Spacer(1, pts))

    def line():
        story.append(HRFlowable(width="100%", thickness=0.5, color=LGREY, spaceAfter=8, spaceBefore=8))

    def shaded(text):
        p = Paragraph(text, styles["Body"])
        story.append(ShadedBox(W, p))
        gap(6)

    def make_table(data, col_widths=None, header=True):
        if col_widths is None:
            col_widths = [W / len(data[0])] * len(data[0])
        t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
        style_cmds = [
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEADING", (0, 0), (-1, -1), 13),
            ("TEXTCOLOR", (0, 0), (-1, -1), DGREY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, LGREY),
        ]
        if header:
            style_cmds += [
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#f0f0f0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
            ]
        t.setStyle(TableStyle(style_cmds))
        story.append(t)
        gap(8)

    # ══════════════════════════════════════════════════════════════════
    # TITLE BLOCK
    # ══════════════════════════════════════════════════════════════════
    gap(20)
    story.append(Paragraph(
        "STRATEGIC ROUTING IN MULTI-PROVIDER AI MARKETS:<br/>"
        "A GAME-THEORETIC ANALYSIS OF AGENT-DRIVEN<br/>"
        "MODEL SELECTION",
        styles["PaperTitle"]
    ))
    gap(8)
    story.append(Paragraph("Nathan Amankwah", styles["Author"]))
    story.append(Paragraph("Supervised by Prof. Rafid Mahmood", styles["Author"]))
    story.append(Paragraph("Telfer School of Management, University of Ottawa", styles["Author"]))
    gap(6)
    story.append(Paragraph("Research Proposal — March 2026", styles["Author"]))
    gap(16)
    line()

    # ══════════════════════════════════════════════════════════════════
    # ABSTRACT
    # ══════════════════════════════════════════════════════════════════
    story.append(Paragraph("ABSTRACT", styles["AbstractLabel"]))
    story.append(Paragraph(
        "Recent work models LLM routing as a Stackelberg game between a single provider and a single "
        "human user (Mahmood, 2026). We propose extending this framework to study routing in "
        "<b>multi-provider markets</b> where the user is an <b>AI agent</b> — an autonomous system that "
        "calls LLM APIs, evaluates responses, and can switch between providers without friction. "
        "As agentic AI systems (e.g., coding assistants, autonomous browsing tools, multi-step task "
        "planners) become the dominant consumers of LLM inference, the assumptions underlying single-provider, "
        "human-user models no longer hold. We study how the shift from human users to computational agents, "
        "combined with provider competition, transforms optimal routing policies, eliminates the viability "
        "of latency throttling, and reshapes the misalignment gap between provider and user objectives. "
        "We formulate the problem as a multi-provider Stackelberg game, characterize the agent's best "
        "response across providers, and identify conditions under which competition improves or worsens "
        "outcomes for the agent. The analysis yields practical implications for LLM pricing, API design, "
        "and the emerging market structure of AI inference services.",
        styles["AbstractBody"]
    ))
    line()

    # ══════════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ══════════════════════════════════════════════════════════════════
    sec("1", "Introduction")

    body(
        "Large language model providers navigate a three-way trade-off between output quality, "
        "inference latency, and compute cost by routing user tasks across a family of models "
        "(Chen et al., 2023; Ding et al., 2024; Dekoninck et al., 2025). Mahmood (2026) formalized "
        "this interaction as a Stackelberg game between a provider choosing a routing and cascading "
        "policy, and a user deciding whether to re-prompt or abandon the task. The key insight is that "
        "user patience — governed by the net value per pass — determines which routing strategies are "
        "optimal, and that low churn penalties can incentivize providers to deliberately inflate latency."
    )

    body(
        "However, the landscape of LLM consumption is changing rapidly. In 2026, a growing share of "
        "LLM API calls originate not from human users typing prompts, but from <b>AI agents</b> — "
        "autonomous software systems that chain multiple LLM calls to accomplish complex tasks. "
        "Coding assistants like Claude Code and Devin make hundreds of API calls per session. "
        "Autonomous browsing agents call LLMs to interpret web pages, fill forms, and make decisions. "
        "Multi-step planning systems orchestrate calls across multiple providers, routing each sub-task "
        "to whichever model offers the best quality-cost trade-off for that specific step."
    )

    body(
        "This shift has two consequences that fundamentally alter the routing game:"
    )

    bullet(
        "<b>The user is no longer human.</b> An AI agent does not experience frustration, impatience, "
        "or cognitive fatigue. Its \"abandonment\" decision is computational — driven by timeout "
        "thresholds, cost budgets, and quality checks rather than the subjective delay costs that "
        "govern human behavior. This changes the user's best-response function and the set of "
        "equilibria the provider faces."
    )
    bullet(
        "<b>The user faces multiple providers.</b> Unlike a human subscriber locked into one "
        "platform, an AI agent can hold API keys for OpenAI, Anthropic, Google, and open-source "
        "endpoints simultaneously. Switching costs are near zero — the agent simply changes which "
        "API it calls. This transforms the single-provider Stackelberg game into a multi-provider "
        "competition where each provider's routing strategy must account for rival offerings."
    )

    gap(4)
    body(
        "We propose a research agenda that extends Mahmood (2026) along both dimensions. "
        "Specifically, we study a game with <b>N competing LLM providers</b>, each offering a "
        "routing policy over their own model family, and a single <b>AI agent</b> that allocates "
        "its inference budget across providers to maximize task completion value minus total cost. "
        "The contributions of this work are:"
    )

    bullet(
        "<b>Agent best-response characterization.</b> We re-derive the user's abandonment and "
        "re-prompting decisions when the user is a cost-minimizing agent with access to multiple "
        "providers, showing how the four regimes identified in Mahmood (2026) collapse or transform."
    )
    bullet(
        "<b>Multi-provider equilibrium.</b> We characterize the Nash equilibrium among providers "
        "competing for agent traffic, and show when competition drives routing toward user-optimal "
        "policies versus when it leads to a race-to-the-bottom on quality."
    )
    bullet(
        "<b>Throttling under competition.</b> We prove conditions under which provider competition "
        "eliminates the throttling incentive identified in Mahmood (2026), and identify edge cases "
        "where implicit coordination can preserve it."
    )
    bullet(
        "<b>Misalignment under competition.</b> We characterize how the misalignment gap between "
        "provider-optimal and agent-optimal routing evolves as the number of providers grows, and "
        "identify market structures that minimize the gap."
    )

    # ══════════════════════════════════════════════════════════════════
    # 2. RELATED LITERATURE
    # ══════════════════════════════════════════════════════════════════
    sec("2", "Related Literature")

    sub("2.1", "LLM Routing and Cascading")
    body(
        "The routing literature focuses on allocating tasks across models to optimize accuracy, "
        "latency, and cost (Chen et al., 2023; Ding et al., 2024; Yue et al., 2023; Hu et al., 2024; "
        "Dekoninck et al., 2025). These works treat user behavior as fixed — the user submits a task "
        "and accepts whatever the router returns. Mahmood (2026) introduced user agency into the "
        "routing problem by modeling the user's re-prompt and abandonment decisions as a best response "
        "to the provider's routing policy. Our work extends this by replacing the single human user "
        "with a computationally rational agent and introducing provider competition."
    )

    sub("2.2", "AI Agents and API Consumption")
    body(
        "The rise of agentic AI systems has shifted LLM consumption patterns from single-turn "
        "human interactions to multi-step automated pipelines (Park et al., 2023; Significant Gravitas, "
        "2023; Wang et al., 2024). Agent frameworks such as LangChain, AutoGPT, and Claude Code "
        "make sequential LLM calls, sometimes across multiple providers, to complete complex workflows. "
        "This creates a new class of API consumer whose behavior differs fundamentally from individual "
        "human users: agents are price-sensitive, latency-tolerant, and capable of real-time provider "
        "switching. No existing routing model captures this consumer type."
    )

    sub("2.3", "Platform Competition and Multi-Sided Markets")
    body(
        "The economics of platform competition has been studied extensively in the context of "
        "telecommunications, cloud computing, and software-as-a-service markets (Rochet & Tirole, 2003; "
        "Armstrong, 2006). The LLM inference market shares features with these settings — providers "
        "compete on price and quality while facing economies of scale in compute. However, the "
        "specific structure of the routing game (where providers can strategically degrade service "
        "through cascading and throttling) introduces dynamics not captured by standard platform models. "
        "Our framework bridges the routing literature with the platform competition literature."
    )

    sub("2.4", "Pricing and Competition for Generative AI")
    body(
        "Mahmood (2024) studies pricing competition between generative AI providers, characterizing "
        "equilibrium pricing strategies under different market structures. Our work complements this "
        "by studying the <i>routing</i> dimension of competition — even at fixed prices, providers "
        "compete through how they allocate tasks across their model families, which affects the "
        "quality of service that agents experience."
    )

    # ══════════════════════════════════════════════════════════════════
    # 3. PROPOSED MODEL
    # ══════════════════════════════════════════════════════════════════
    sec("3", "Proposed Model")

    body(
        "We extend the Markov model of Mahmood (2026) to incorporate multiple providers and an "
        "agent user. We first describe the single-provider baseline, then introduce competition "
        "and the agent's optimization problem."
    )

    sub("3.1", "Single-Provider Baseline (Mahmood, 2026)")
    body(
        "A provider offers two models M<sub>1</sub> (standard) and M<sub>2</sub> (reasoning). "
        "Each model has inference cost c<sub>i</sub>, latency cost t<sub>i</sub>, and success "
        "probability p<sub>i</sub>. The provider commits to a routing policy (i, s), where i is "
        "the initial model and s is the cascade probability. The user sets an abandonment probability "
        "q. The user's net value per pass is:"
    )
    eq("&xi;<sub>i</sub> = V &middot; p<sub>i</sub> &minus; t<sub>i</sub>")
    body(
        "where V is the task value and t<sub>i</sub> is the delay cost. A model is <i>value-dominated</i> "
        "if &xi;<sub>i</sub> &gt; 0 and <i>latency-dominated</i> if &xi;<sub>i</sub> &lt; 0. "
        "The interaction forms a Stackelberg game: the provider moves first (choosing routing), "
        "the user responds (choosing abandonment). Key results include:"
    )
    bullet("User patience depends entirely on the sign of &xi;<sub>1</sub> and &xi;<sub>2</sub> (Theorem 2).")
    bullet("Optimal routing is almost always static — no cascading (Theorems 3-5).")
    bullet("Low churn penalty P incentivizes providers to inflate latency (Proposition 2).")
    bullet("Misalignment arises when cost and utility rankings of models disagree (Proposition 1).")

    sub("3.2", "Multi-Provider Extension")
    body(
        "We consider N providers, indexed by j = 1, ..., N. Each provider j offers two models "
        "with parameters (c<sub>j1</sub>, c<sub>j2</sub>, t<sub>j1</sub>, t<sub>j2</sub>, "
        "p<sub>j1</sub>, p<sub>j2</sub>) and sets a routing policy (i<sub>j</sub>, s<sub>j</sub>). "
        "The key structural change is that each provider's churn penalty P<sub>j</sub> is no longer "
        "a fixed parameter — it depends on the competing providers' offerings. When a user abandons "
        "provider j, they do not leave the market; they switch to a rival. This makes P<sub>j</sub> "
        "a function of the equilibrium strategies of all providers:"
    )
    eq("P<sub>j</sub> = P<sub>j</sub>(s<sub>1</sub>, ..., s<sub>N</sub>)")
    body(
        "Specifically, the penalty for losing a user increases when rivals offer better routing "
        "policies (higher effective success rates, lower latencies). This endogenizes a parameter "
        "that Mahmood (2026) treats as fixed, with important consequences for the throttling result."
    )

    sub("3.3", "Agent User Model")
    body(
        "We replace the human user with an AI agent. The agent differs from a human in three ways "
        "that directly affect the game's structure:"
    )

    body("<b>1. Near-zero subjective delay cost.</b>")
    bodyindent(
        "A human user experiences frustration while waiting for a model response. An agent does not. "
        "We model the agent's delay cost as t<sub>i</sub><sup>A</sup> = &epsilon; &middot; t<sub>i</sub>, "
        "where &epsilon; &ge; 0 is small and represents the marginal compute cost of the agent's own "
        "runtime while waiting. As &epsilon; &rarr; 0, the agent's net value becomes:"
    )
    eq("&xi;<sub>i</sub><sup>A</sup> = V &middot; p<sub>i</sub> &minus; &epsilon; &middot; t<sub>i</sub> &asymp; V &middot; p<sub>i</sub> &gt; 0")
    bodyindent(
        "This means <b>both models are always value-dominated for the agent</b>. Two of the four "
        "regimes in Theorem 2 (where &xi;<sub>i</sub> &lt; 0 for at least one model) effectively "
        "disappear. The agent is always patient."
    )

    body("<b>2. Computational rationality.</b>")
    bodyindent(
        "The agent can observe or estimate the provider's routing policy (i, s) and compute its "
        "optimal response exactly. Unlike a human who may infer s from experience or reputation, "
        "the agent can benchmark providers systematically — sending test queries, measuring response "
        "distributions, and estimating p<sub>i</sub> directly. The information asymmetry assumption "
        "in the baseline model weakens significantly."
    )

    body("<b>3. Multi-provider access.</b>")
    bodyindent(
        "The agent holds API keys for multiple providers and can switch between them at near-zero "
        "cost. The agent's problem is not \"stay or leave\" (as in the human model) but "
        "\"which provider should I call next?\" This transforms the binary abandonment decision "
        "q &isin; [0, 1] into a multi-provider allocation decision."
    )

    sub("3.4", "Agent's Optimization Problem")
    body(
        "Let &alpha;<sub>j</sub> &isin; [0, 1] denote the fraction of tasks the agent routes to "
        "provider j, with &Sigma;<sub>j</sub> &alpha;<sub>j</sub> = 1. Given provider routing "
        "policies {(i<sub>j</sub>, s<sub>j</sub>)}<sub>j</sub>, the agent solves:"
    )
    eq("max<sub>&alpha;</sub> &Sigma;<sub>j</sub> &alpha;<sub>j</sub> &middot; U<sub>j</sub>(s<sub>j</sub>, q<sub>j</sub><sup>*</sup>)")
    body(
        "subject to a budget constraint on total inference spend. Here, U<sub>j</sub> is the "
        "expected utility from provider j using the notation of Mahmood (2026), and q<sub>j</sub><sup>*</sup> "
        "is the agent's optimal abandonment policy for provider j (which may now depend on the "
        "outside option offered by other providers)."
    )
    body(
        "The agent's quit probability for provider j is no longer a standalone decision — it is "
        "informed by the best alternative. In the single-provider model, quitting means getting "
        "nothing. In the multi-provider model, quitting provider j means trying provider k. This "
        "raises the agent's effective outside option and makes it <i>more</i> willing to abandon "
        "any individual provider, fundamentally changing the equilibrium."
    )

    # ══════════════════════════════════════════════════════════════════
    # 4. EXPECTED CONTRIBUTIONS
    # ══════════════════════════════════════════════════════════════════
    sec("4", "Expected Contributions")

    body(
        "We outline the main results we expect to derive, each corresponding to a specific result "
        "in Mahmood (2026). The goal is to show precisely how each finding transforms under "
        "competition and agent rationality."
    )

    sub("4.1", "Regime Collapse Under Agent Users")
    body(
        "Mahmood (2026, Theorem 2) identifies four user-behavior regimes based on the signs of "
        "&xi;<sub>1</sub> and &xi;<sub>2</sub>. When the user is an agent with &epsilon; &asymp; 0:"
    )

    make_table(
        [
            [Paragraph("<b>Regime</b>", styles["Body"]),
             Paragraph("<b>Condition</b>", styles["Body"]),
             Paragraph("<b>Human User</b>", styles["Body"]),
             Paragraph("<b>Agent User</b>", styles["Body"])],
            [Paragraph("1", styles["Body"]),
             Paragraph("&xi;<sub>1</sub>, &xi;<sub>2</sub> &gt; 0", styles["Body"]),
             Paragraph("User stays regardless of routing", styles["Body"]),
             Paragraph("<b>Always active.</b> Agent stays and re-prompts.", styles["Body"])],
            [Paragraph("2", styles["Body"]),
             Paragraph("&xi;<sub>1</sub>, &xi;<sub>2</sub> &lt; 0", styles["Body"]),
             Paragraph("User leaves regardless of routing", styles["Body"]),
             Paragraph("<b>Effectively eliminated.</b> Agent's low t makes both &xi; positive.", styles["Body"])],
            [Paragraph("3", styles["Body"]),
             Paragraph("&xi;<sub>1</sub> &lt; 0 &lt; &xi;<sub>2</sub>", styles["Body"]),
             Paragraph("User stays only if cascade chance is high enough", styles["Body"]),
             Paragraph("<b>Effectively eliminated.</b> Collapses to Regime 1.", styles["Body"])],
            [Paragraph("4", styles["Body"]),
             Paragraph("&xi;<sub>1</sub> &gt; 0 &gt; &xi;<sub>2</sub>", styles["Body"]),
             Paragraph("User stays only if cascade chance is low enough", styles["Body"]),
             Paragraph("<b>Effectively eliminated.</b> Collapses to Regime 1.", styles["Body"])],
        ],
        col_widths=[W*0.08, W*0.18, W*0.35, W*0.39],
    )

    body(
        "This regime collapse has a major implication: <b>the provider can no longer use routing "
        "to influence the agent's behavior</b>. When dealing with human users, providers could "
        "manipulate the cascade rate s to push users into favorable regimes. Against agents, this "
        "lever disappears. The provider's optimization problem simplifies to pure cost minimization, "
        "since the agent will always re-prompt."
    )

    sub("4.2", "Throttling Fails Against Agents")
    body(
        "Mahmood (2026, Proposition 2) shows that when P &le; min{c<sub>1</sub>/p<sub>1</sub>, "
        "c<sub>2</sub>/p<sub>2</sub>}, providers benefit from inflating latency to "
        "t&#770;<sub>i</sub> &gt; Vp<sub>i</sub>, making both models latency-dominated and "
        "encouraging user abandonment. We expect to show this strategy fails against agents for "
        "two reasons:"
    )

    bullet(
        "<b>Agents are latency-insensitive.</b> Inflating t<sub>i</sub> does not change the "
        "agent's &xi;<sub>i</sub><sup>A</sup> because the agent's delay cost is near zero. "
        "The provider would need to inflate latency to extreme levels (where the agent's own "
        "compute costs of waiting exceed Vp<sub>i</sub>) before the agent abandons."
    )
    bullet(
        "<b>Competition creates an outside option.</b> Even if one provider throttles, the agent "
        "simply routes to a competitor. The effective churn penalty P<sub>j</sub> is no longer "
        "\"the user might unsubscribe\" — it is \"the user will immediately switch to a rival and "
        "never come back.\" This makes P<sub>j</sub> large, which Mahmood (2026) already shows "
        "eliminates the throttling incentive."
    )

    gap(4)
    shaded(
        "<b>Key expected result:</b> In the multi-provider agent setting, the conditions for "
        "profitable throttling (P &le; min{c<sub>i</sub>/p<sub>i</sub>}) are almost never "
        "satisfied, because competition endogenously inflates the effective churn penalty P<sub>j</sub> "
        "above the throttling threshold."
    )

    sub("4.3", "Misalignment Under Competition")
    body(
        "Mahmood (2026, Proposition 1) defines the misalignment gap &Delta;U as the difference "
        "between the user-optimal and provider-optimal routing policies. Under monopoly, "
        "misalignment arises when cost-of-pass rankings (c<sub>i</sub>/p<sub>i</sub>) disagree "
        "with user utility rankings (&xi;<sub>i</sub>/p<sub>i</sub>). Under competition, we "
        "expect the gap to behave differently depending on the number of providers:"
    )
    bullet(
        "<b>Duopoly (N=2):</b> Misalignment decreases but does not vanish. Each provider is "
        "constrained by the rival's offering but still optimizes for cost rather than user utility."
    )
    bullet(
        "<b>Many providers (N &rarr; &infin;):</b> Competition drives providers toward the "
        "user-optimal routing policy. In the limit, &Delta;U &rarr; 0 as any deviation from "
        "user-optimal routing causes the agent to switch providers."
    )
    bullet(
        "<b>Oligopoly (small N):</b> The most realistic case. Providers may implicitly coordinate "
        "on routing strategies — if all providers route to cheap models, the agent has no better "
        "alternative. This preserves misalignment despite nominal competition."
    )

    sub("4.4", "When Static Routing Is No Longer Optimal")
    body(
        "Mahmood (2026, Theorems 3-5) shows that optimal routing is almost always static (no "
        "cascading). We conjecture that under competition, this result may change. When providers "
        "compete for agent traffic, a provider might benefit from offering cascading as a "
        "<i>differentiation strategy</i> — \"we always escalate to our best model if the standard "
        "one fails\" — to attract agents away from competitors who only offer static routing. "
        "This introduces cascading as a competitive tool rather than a cost-optimization mechanism."
    )

    # ══════════════════════════════════════════════════════════════════
    # 5. METHODOLOGY
    # ══════════════════════════════════════════════════════════════════
    sec("5", "Methodology")

    sub("5.1", "Analytical Approach")
    body(
        "The primary methodology is game-theoretic analysis, following the approach of Mahmood (2026). "
        "We solve the multi-provider game in stages:"
    )
    bullet(
        "<b>Stage 1 — Agent best response:</b> Given provider policies {(i<sub>j</sub>, s<sub>j</sub>)}, "
        "characterize the agent's optimal allocation &alpha;<sup>*</sup> and per-provider abandonment "
        "policies q<sub>j</sub><sup>*</sup>. This extends Theorems 1-2 of Mahmood (2026) to the "
        "multi-provider setting."
    )
    bullet(
        "<b>Stage 2 — Provider equilibrium:</b> Given the agent's best response, characterize "
        "the Nash equilibrium among providers choosing routing policies simultaneously. This extends "
        "Theorems 3-5 to a competitive setting."
    )
    bullet(
        "<b>Stage 3 — Welfare analysis:</b> Compare the equilibrium outcomes to the social optimum "
        "(maximizing total surplus) and to the single-provider Stackelberg equilibrium, quantifying "
        "how competition affects misalignment and efficiency."
    )

    sub("5.2", "Numerical Experiments")
    body(
        "To complement the analytical results, we plan numerical experiments that:"
    )
    bullet(
        "Simulate the multi-provider game under realistic parameter values drawn from published "
        "LLM pricing data (e.g., OpenAI, Anthropic, and Google API pricing as of 2026)."
    )
    bullet(
        "Compute equilibria for varying N (number of providers) to trace how the misalignment gap, "
        "throttling incentive, and regime structure evolve as the market becomes more competitive."
    )
    bullet(
        "Compare agent-user equilibria with human-user equilibria from Mahmood (2026) under "
        "identical provider parameters, isolating the effect of user type."
    )

    sub("5.3", "Data Sources")
    body(
        "All data required for calibration is publicly available:"
    )
    bullet("LLM API pricing: published by OpenAI, Anthropic, Google, and others.")
    bullet("Inference latency benchmarks: reported by ArtificialAnalysis.ai, LMSys, and similar platforms.")
    bullet(
        "Agent usage patterns: published reports on API call volumes and routing behavior from "
        "agent framework documentation and industry benchmarks."
    )

    # ══════════════════════════════════════════════════════════════════
    # 6. TIMELINE
    # ══════════════════════════════════════════════════════════════════
    sec("6", "Proposed Timeline")

    make_table(
        [
            [Paragraph("<b>Phase</b>", styles["Body"]),
             Paragraph("<b>Weeks</b>", styles["Body"]),
             Paragraph("<b>Deliverable</b>", styles["Body"])],
            [Paragraph("1. Literature review", styles["Body"]),
             Paragraph("1–3", styles["Body"]),
             Paragraph("Comprehensive review of routing, agentic AI, and platform competition literature", styles["Body"])],
            [Paragraph("2. Agent best response", styles["Body"]),
             Paragraph("3–7", styles["Body"]),
             Paragraph("Formal derivation of agent behavior under multi-provider access (extends Theorems 1-2)", styles["Body"])],
            [Paragraph("3. Provider equilibrium", styles["Body"]),
             Paragraph("6–10", styles["Body"]),
             Paragraph("Nash equilibrium characterization among competing providers (extends Theorems 3-5)", styles["Body"])],
            [Paragraph("4. Welfare analysis", styles["Body"]),
             Paragraph("9–13", styles["Body"]),
             Paragraph("Misalignment and throttling under competition (extends Propositions 1-2)", styles["Body"])],
            [Paragraph("5. Numerical experiments", styles["Body"]),
             Paragraph("11–14", styles["Body"]),
             Paragraph("Simulations with real pricing data, sensitivity analysis", styles["Body"])],
            [Paragraph("6. Writing and revision", styles["Body"]),
             Paragraph("13–16", styles["Body"]),
             Paragraph("Full paper draft, feedback from Prof. Mahmood, final revision", styles["Body"])],
        ],
        col_widths=[W*0.30, W*0.12, W*0.58],
    )

    # ══════════════════════════════════════════════════════════════════
    # 7. CONNECTION TO EXISTING RESEARCH
    # ══════════════════════════════════════════════════════════════════
    sec("7", "Connection to Supervisor's Research Program")

    body(
        "This proposal is designed to complement and extend the research program of Prof. Mahmood "
        "across several dimensions:"
    )

    body("<b>Routing and user behavior (Mahmood, 2026).</b>")
    bodyindent(
        "The proposed work directly builds on the Stackelberg routing game by generalizing the "
        "single-provider, single-user setting. Every theorem and proposition in the original paper "
        "has a corresponding result in our multi-provider, agent-user framework. The comparison "
        "between these results constitutes a central contribution of the proposed work."
    )

    body("<b>Pricing and competition (Mahmood, 2024).</b>")
    bodyindent(
        "The NeurIPS paper on pricing competition for generative AI provides the economic foundation "
        "for our multi-provider model. While that paper studies price competition, our work studies "
        "routing competition — a complementary dimension of provider strategy that operates even "
        "when prices are fixed."
    )

    body("<b>Equity and access (SSHRC research program).</b>")
    bodyindent(
        "Prof. Mahmood's SSHRC-funded work on using synthetic data for labor market equality "
        "reflects a broader commitment to studying how AI systems affect different populations. "
        "Our work contributes to this agenda by studying how the market structure of AI inference "
        "shapes the quality of service that different types of users (human vs. agent, high-volume "
        "vs. low-volume) receive."
    )

    body("<b>Societal implications of AI systems.</b>")
    bodyindent(
        "Prof. Mahmood's research consistently examines how optimization decisions in AI systems "
        "create unintended consequences for users and society. The throttling result in the ICLR "
        "paper is a prime example — a cost-optimal strategy that harms users. Our work extends "
        "this lens to the multi-provider market, asking whether competition cures or compounds "
        "such misalignment."
    )

    # ══════════════════════════════════════════════════════════════════
    # 8. CONCLUSION
    # ══════════════════════════════════════════════════════════════════
    sec("8", "Conclusion")

    body(
        "The transition from human users to AI agents as the primary consumers of LLM inference "
        "represents a fundamental shift in the structure of the routing game. Combined with "
        "increasing provider competition, this shift alters every major result in the existing "
        "single-provider framework: user regimes collapse, throttling loses its economic rationale, "
        "and the misalignment gap becomes a function of market concentration rather than individual "
        "provider incentives."
    )
    body(
        "This research agenda is both timely (the shift to agentic AI consumption is happening now) "
        "and foundational (it provides the game-theoretic framework for understanding multi-provider "
        "AI markets). The proposed work directly extends the most recent contributions of "
        "Prof. Mahmood while opening new questions about the economics of AI inference that are "
        "relevant to providers, regulators, and the broader AI research community."
    )

    # ══════════════════════════════════════════════════════════════════
    # REFERENCES
    # ══════════════════════════════════════════════════════════════════
    sec("", "References")

    refs = [
        "Armstrong, M. (2006). Competition in two-sided markets. <i>The RAND Journal of Economics</i>, 37(3), 668-691.",
        "Chen, L., Zaharia, M., & Zou, J. (2023). FrugalGPT: How to use large language models while reducing cost and improving performance. <i>arXiv preprint arXiv:2305.05176</i>.",
        "Dekoninck, J., Baader, M., & Vechev, M. (2025). A unified approach to routing and cascading for LLMs. In <i>ICML 2025</i>.",
        "Ding, D., Mallick, A., Wang, C., et al. (2024). Hybrid LLM: Cost-efficient and quality-aware query routing. In <i>ICLR 2024</i>.",
        "Erol, M. H., El, B., Suzgun, M., et al. (2025). Cost-of-pass: An economic framework for evaluating language models. <i>arXiv preprint arXiv:2504.13359</i>.",
        "Hu, Q. J., Bieker, J., Li, X., et al. (2024). RouterBench: A benchmark for multi-LLM routing system. <i>arXiv preprint arXiv:2403.12031</i>.",
        "Mahmood, R. (2024). Pricing and competition for generative AI. <i>Advances in Neural Information Processing Systems</i>, 37, 75727-75748.",
        "Mahmood, R. (2026). Routing, cascades, and user choice for LLMs. Under review at <i>ICLR 2026</i>.",
        "Park, J. S., O'Brien, J. C., Cai, C. J., et al. (2023). Generative agents: Interactive simulacra of human behavior. In <i>UIST 2023</i>.",
        "Rochet, J.-C., & Tirole, J. (2003). Platform competition in two-sided markets. <i>Journal of the European Economic Association</i>, 1(4), 990-1029.",
        "Significant Gravitas. (2023). AutoGPT: An autonomous GPT-4 experiment. <i>GitHub repository</i>.",
        "Wang, L., Ma, C., Feng, X., et al. (2024). A survey on large language model based autonomous agents. <i>Frontiers of Computer Science</i>, 18(6).",
        "Yue, M., Zhao, J., Zhang, M., et al. (2023). Large language model cascades with mixture of thoughts representations. <i>arXiv preprint arXiv:2310.03094</i>.",
    ]
    for ref in refs:
        story.append(Paragraph(ref, styles["RefItem"]))

    # ── build ────────────────────────────────────────────────────────
    doc.build(story)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
