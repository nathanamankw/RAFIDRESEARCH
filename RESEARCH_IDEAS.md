# Research Proposals — Building on Mahmood (ICLR 2026)

Three research directions that build on "Routing, Cascades, and User Choice for LLMs" with a focus on real societal problems.

---

## IDEA 1: Who Gets the Good Model? — How AI Routing Creates Rich vs. Poor Service

### The Problem in Plain English

Rafid's paper looks at ONE user interacting with a provider. But in reality, millions of different people use ChatGPT, Claude, Gemini — and they're all different. A corporate lawyer using AI to draft a $10M contract cares a LOT about quality. A broke college student using the free tier for homework help does not have the same leverage.

When AI companies decide which model to send your question to, they're making that choice based on what saves THEM money. The result? **Rich, high-value users get the smart model. Poor, low-value users get the dumb model.** AI routing quietly creates a two-tier system that mirrors the inequality already in society.

### How It Builds on Rafid's Paper

Rafid assumes one identical user. We say: **people are different.** We group users by "type" — think of it as their economic profile. Each type has:

- **V(θ)** = how much the task is worth to them (a lawyer's contract vs. a student's essay)
- **P(θ)** = how much the company loses if this user leaves (a $200/month enterprise client vs. a free-tier user)
- **t(θ)** = how much the wait time costs them (a surgeon's time vs. a teenager's time)

The Greek letter θ (theta) just means "user type" — think of it as a sliding scale from low-income to high-income.

### The Key Equation — Net Value Becomes Personal

In Rafid's paper, the "net value per pass" tells you if a model is worth using:

**ξ_i = V × p_i − t_i**

(Task value times success chance, minus the wait time cost)

In our version, this becomes personal to each user type:

**ξ_i(θ) = V(θ) × p_i − t_i(θ)**

This means the SAME model can be "worth it" for a rich user but "not worth it" for a poor user, because their V and t are different.

### What Happens — The Four Tiers of Service

Because V goes up as income goes up, there are cutoff points where users flip from "this model isn't worth my time" to "this model is worth it":

```
Low-income users          Middle users              High-income users
Both models feel slow     One model works,          Both models are
and useless to them       one doesn't               worth using
→ They give up            → Depends on routing      → They're always patient
→ Provider doesn't care   → Provider optimizes       → Provider gives best service
→ WORST service           → MIXED service            → BEST service
```

### The Inequality Measure

We define a simple gap:

**Inequality Gap = Utility of richest users − Utility of poorest users**

If this gap is zero, routing is fair. If it's large, routing is making inequality worse.

### The Throttling Problem Gets Worse

Rafid showed providers can deliberately slow down models to save money (Proposition 2). That trick works when the penalty for losing a user is low. Since low-income users have low penalty (the company barely cares if they leave), **providers are most tempted to throttle service for poor users specifically.**

### Why This Matters in the Real World

- Free ChatGPT users get GPT-4o mini. Paying users get GPT-4o and o1.
- API rate limits mean small startups get slower responses than enterprise clients
- Users in developing countries face higher latency from distant servers
- This isn't a bug — it's the math of cost-minimizing routing applied to unequal users

### How It Connects to Rafid's Broader Work

- **ICLR paper**: We take his single-user game and open it up to a whole population
- **NeurIPS pricing paper**: His pricing tiers directly create the user types we study
- **SSHRC equity grant**: Same equity lens, applied to who gets good AI vs. bad AI

---

## IDEA 2: Can Governments Fix This? — A Regulator vs. Provider vs. User Game

### The Problem in Plain English

Rafid's paper has a scary finding: providers can deliberately make their models slower to discourage users from re-prompting, saving the company money at the user's expense. And nothing stops them.

The obvious question: **what if the government steps in?**

Right now, governments worldwide are scrambling to regulate AI — the EU AI Act, Canada's AIDA bill, US executive orders. But they're doing it without a mathematical model of what actually works. We build that model. We add a **regulator** as a third player who moves first, setting rules that the provider must follow before the provider picks their routing strategy.

### How It Builds on Rafid's Paper

Rafid has two players: the company moves first (picks routing), then the user responds. We add a third layer on top:

1. **Government** sets rules (moves first)
2. **Company** picks routing strategy within those rules (moves second)
3. **User** decides whether to stay or leave (moves last)

This is a "three-level leader-follower game" — the same Stackelberg structure Rafid uses, just with one more level.

### Three Types of Rules the Government Can Set

**Rule 1: Quality Floor — "Your AI must actually work"**

The government says: your model must successfully complete at least X% of tasks.

In math: **Success rate ≥ S_min**

This stops providers from routing everyone to the cheap, bad model. But if set too high, the company might raise prices or shut down — so the government has to balance.

**Rule 2: Speed Limit — "You can't deliberately slow things down"**

The government says: your model must respond within a maximum time.

In math: **Wait time ≤ t_max**

This directly blocks the throttling trick from Rafid's Proposition 2. The company can no longer inflate wait times to push users away.

**Rule 3: Transparency — "Tell users what you're doing"**

The government says: you must tell users which model they're getting and the chance of being switched to another model.

In math: **The cascade rate s must be public**

Rafid's paper assumes users can see the routing strategy. In reality, they can't. This rule makes the assumption true.

### The Government's Goal

The government wants to maximize overall wellbeing — a blend of user happiness and company health:

**Welfare = (weight on users) × User Utility − (weight on companies) × Company Cost**

Or in math: **W(r) = λ × E[U] − (1−λ) × E[J]**

where λ is how much the government prioritizes users vs. companies. λ = 1 means the government only cares about users. λ = 0.5 means equal weight.

### Key Findings to Aim For

**Finding 1: Quality floors can backfire.** If the government sets the bar too high, companies are forced to use only the expensive model. They raise prices. Some users can't afford it. Net effect: fewer people have access to AI at all.

**Finding 2: Anti-throttling rules have a sweet spot.** Too loose and companies still throttle. Too strict and companies can't manage server load. There's an optimal speed limit that depends on the model costs and success rates.

**Finding 3: Transparency is always good (or at least never bad).** When users know what they're getting, they make better decisions. This never hurts overall welfare. It's the safest regulation to implement.

### Why This Matters in the Real World

- The **EU AI Act** (passed 2024) mandates transparency for AI systems — does it actually help?
- **Canada's AIDA** proposes quality standards — this model can evaluate them
- Companies like OpenAI and Anthropic make voluntary commitments — are they enough?
- Every government regulator asking "what should we do about AI?" needs this framework

### How It Connects to Rafid's Broader Work

- **ICLR paper**: His Proposition 2 (throttling) is the problem this paper solves
- **NeurIPS pricing paper**: Regulation constrains the pricing game he modeled
- **SSHRC equity work**: Regulation is a tool for equity — this tells you which tool works
- **Operations research roots**: Regulation design IS an optimization problem

---

## IDEA 3: Humans vs. AI at Work — When Companies Choose Between Workers and Algorithms

### The Problem in Plain English

This is the big one. Forget routing between two AI models — the most important routing decision happening right now is **companies deciding which tasks go to humans and which go to AI.**

Every company is asking: "Should we hire a person or use an AI for this?" That decision has the exact same structure as Rafid's paper. The company (provider) picks whether to route a task to a human (Model 1) or AI (Model 2). The worker (user) decides whether to stay at the job or leave.

And just like Rafid showed that providers can deliberately slow down models to push users away, **companies can deliberately make jobs worse to push workers out before replacing them with AI.**

### How It Builds on Rafid's Paper

The mapping is almost perfect — we just swap the labels:

| Rafid's Paper | This Paper | Plain English |
|---|---|---|
| M1 (standard model) | H (human worker) | The "basic" option |
| M2 (reasoning model) | A (AI system) | The "advanced" option |
| Provider | Firm / employer | The one making routing decisions |
| User | Worker | The one who can stay or leave |
| Success rate p_i | Task quality q_H, q_A | How well each option completes the task |
| Wait time t_i | Wage w_H / compute cost c_A | What each option costs |
| User gives up (q) | Worker quits (σ) | The "abandonment" decision |
| Lost subscription revenue (P) | Cost to replace/retrain (R) | The penalty for losing them |
| Cascade rate (s) | Escalation rate (e) | AI fails → send to human |
| Task value (V) | Revenue from completed task (V) | What a finished task is worth |

### The Key Equations — Translated

**Is the job worth it for the worker?**

In Rafid's paper: ξ_i = V × p_i − t_i (value times success rate minus wait cost)

Here: **ξ_H = w_H − e_H** (wage minus effort cost — is this job worth doing?)

If positive, the job is "worth it" (like a value-dominated model). If negative, the worker is better off leaving (like a latency-dominated model).

**What does the company pay?**

The company's total cost for a task depends on the automation rate **a** (what fraction of tasks go to AI):

**Company cost = a × (AI compute cost) + (1−a) × (human wage) + (escalation costs when AI fails) + (replacement cost if worker quits)**

Or in math: **J = a × c_A + (1−a) × w_H + a(1−q_A) × e × w_H + R × σ***

### The Four Worker Regimes — Same Structure as Rafid's Theorem 2

Workers behave exactly like users in Rafid's paper:

**Regime 1: Good job, bad outside options (ξ_H > 0, outside option low)**
Workers stay no matter how much the company automates. Think: well-paid specialist with no equivalent jobs elsewhere. "I'll deal with AI taking some of my tasks — the pay is still good."

**Regime 2: Bad job, good outside options (ξ_H < 0, outside option high)**
Workers leave no matter what. Think: underpaid gig worker who can easily switch platforms. "This job isn't worth it and I have other options."

**Regime 3: Bad job, bad outside options (ξ_H < 0, outside option low)**
Workers stay ONLY if the company keeps sending them meaningful tasks (low automation rate). Think: factory worker who can't easily retrain. "I hate this job but I need it — unless they automate everything, then I'm forced out."

**Regime 4: Good job, good outside options (ξ_H > 0, outside option high)**
Workers stay ONLY if the automation rate stays below a threshold. Think: senior software engineer who could go elsewhere. "I like this job, but if they replace too much of my work with AI, I'll leave for a company that values me."

### The "Worker Throttling" Problem — The Scariest Result

Just like Rafid showed companies can deliberately slow down AI to push users away, we show:

**If replacing a worker is cheap (R is low), companies are tempted to deliberately make jobs worse to push workers out.**

This means: cutting hours, removing interesting tasks, increasing monitoring, reducing autonomy — not because it's efficient, but because it makes workers quit "voluntarily" so the company avoids severance and bad press.

The math: **If R ≤ min{w_H/q_H, c_A/q_A}, then degrading working conditions is profitable.**

In plain English: if it's cheap to replace workers (lots of people in the job market, or AI is nearly ready), companies benefit from making the job miserable.

### The Misalignment Gap — Workers Get a Raw Deal

Just like Rafid measures the gap between what's best for the user vs. what the provider actually does:

**Worker welfare gap = Best possible worker outcome − Actual outcome under company's cost-cutting routing**

When the company optimizes purely for cost, workers almost always get less than what would be optimal for them. The gap is largest when:
- AI is almost as good as humans but much cheaper
- Replacing workers is easy (large labor pool)
- Workers have few outside options

### Why This Matters in the Real World

This is THE social issue of AI:
- **McKinsey estimates** 30% of work hours could be automated by 2030
- **"Quiet firing"** is already happening — companies degrade roles until people quit
- **Amazon warehouses** use algorithmic routing between human workers and robots right now
- **Hollywood strikes (2023)** were specifically about AI-human task allocation in creative work
- **Call centers** route between AI chatbots and human agents — identical to this model
- **Uber/Lyft** decide when to show you a human driver vs. autonomous vehicle

### How It Connects to Rafid's Broader Work

- **ICLR paper**: Exact same math, swapping AI models for humans and AI
- **NeurIPS pricing paper**: Wage competition between human labor and AI compute costs
- **SSHRC labor equity grant**: This IS labor market equity research — directly in his funded lane
- **Healthcare work**: His milk bank optimization is about routing resources to people in need — this does the same for workers

---

## How All Three Ideas Connect

```
                        Rafid's ICLR Paper
                     (Provider routes between
                      two models, user reacts)
                              |
              ________________|________________
             |                |                |
         IDEA 1           IDEA 2           IDEA 3
     "Who gets the     "Can government    "Humans vs AI
      good model?"      fix routing?"      at work"
             |                |                |
        Different         Add a third       Swap AI models
        users get         player: the       for human workers
        different         regulator         and AI systems
        service                |                |
             |           Sets rules that    Same math,
        Creates an       constrain the      real-world labor
        AI digital       company before     displacement
        divide           it can route       crisis
             |                |                |
             |________________|________________|
                              |
                     SOCIETAL IMPACT:
                  Inequality, governance,
                     labor displacement
```

---

## Strength of Each Idea

| What matters | Idea 1: AI Digital Divide | Idea 2: Regulation Game | Idea 3: Humans vs. AI at Work |
|---|---|---|---|
| **New math** | Many users instead of one | Three players instead of two | Swap in humans for one model |
| **How urgent** | High — AI access gap growing | Very high — governments writing laws NOW | Highest — jobs are THE AI worry |
| **Fits Rafid** | Extends his game to populations | Solves the problem his paper exposes | Mirrors his math + his SSHRC grant |
| **Where to publish** | ICLR, NeurIPS, EC | Management Science, Operations Research | Management Science, NeurIPS |
| **Data available** | API pricing is public | Policy documents are public | Labor statistics, platform data |
| **Own your lane** | Yes — nobody has done this | Yes — nobody has done this | Yes — nobody has done this |
