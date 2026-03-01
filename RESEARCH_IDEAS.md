# Research Proposals — Extending Mahmood (ICLR 2026)

Three self-directed research directions building on "Routing, Cascades, and User Choice for LLMs" with societal impact focus.

---

## IDEA 1: Routing Inequality — How LLM Routing Creates a Digital Divide

### Thesis
When providers route to minimize aggregate cost across heterogeneous users, they systematically under-serve users with low task value and low churn risk — creating an AI service quality divide that mirrors socioeconomic inequality.

### Extension of ICLR Paper
- Single user → population of users indexed by type θ ~ F(θ)
- Each type has (V(θ), t(θ), P(θ))
- Net value becomes type-dependent: ξ_i(θ) = V(θ)·p_i − t_i(θ)

### Key Equations
- Provider population problem: min E_θ[J_{i(θ)}(s(θ), q*(i(θ), s(θ); θ))]
- Routing inequality gap: Δ_equity = U*(θ_H) − U*(θ_L)
- Type-dependent throttling: profitable when P(θ) ≤ min{c_i/p_i}
- Threshold types θ_1, θ_2 partition population into four service quality segments

### Societal Issue
AI subscription tiers, free vs. paid access, geographic latency disparities create systematic inequality in AI service quality along socioeconomic lines.

---

## IDEA 2: The Regulation Game — Three-Player Stackelberg for AI Governance

### Thesis
Extend the two-player game to Regulator → Provider → User. Characterize optimal regulatory instruments (quality floors, latency caps, transparency mandates) that maximize social welfare while accounting for provider strategic response.

### Extension of ICLR Paper
- Two players → three-player hierarchical Stackelberg
- Regulator sets constraints r before provider chooses routing
- Directly addresses unchecked throttling (Proposition 2)

### Key Equations
- Regulator welfare: W(r) = λ·E[U] − (1−λ)·E[J]
- Quality floor: S_i(s, q*) ≥ S_min (with provider participation constraint)
- Anti-throttling cap: t_i ≤ t_max
- Transparency gain: Δ_T = W(r_T) − W(no transparency) ≥ 0

### Societal Issue
Maps to EU AI Act, Canada's AIDA, and corporate self-regulation debates. Formally evaluates whether proposed regulations help or backfire.

---

## IDEA 3: The Human-AI Labor Routing Game

### Thesis
Model the firm's task allocation between AI and human workers as a Stackelberg game. Firms route tasks to minimize cost; workers respond by staying, quitting, or reskilling. Characterize equilibrium, worker welfare gap, and conditions for "worker throttling."

### Extension of ICLR Paper
- M1 (standard) → H (human worker), M2 (reasoning) → A (AI system)
- User abandonment q → worker exit σ
- Cascade s → escalation rate e (AI fails → human)
- Churn penalty P → replacement cost R
- Throttling latency → degrading working conditions

### Key Equations
- Worker net value: ξ_H = w_H − e_H (wage minus effort)
- Firm cost: J_firm = E[a·c_A + (1−a)·w_H + a(1−q_A)·e·w_H] + R·σ*
- Worker throttling condition: R ≤ min{w_H/q_H, c_A/q_A}
- Worker misalignment gap: Δ_W = max U_W − U_W(firm's choice)

### Societal Issue
AI labor displacement, "quiet firing," gig economy task routing, screenwriter/actor strike dynamics. The biggest societal AI question of the decade.

---

## Alignment Summary

| Rafid's Work | Idea 1 | Idea 2 | Idea 3 |
|---|---|---|---|
| Stackelberg game (ICLR) | Population extension | 3-player extension | Human-AI extension |
| Misalignment ΔU | Equity gap Δ_equity | Welfare function W(r) | Worker gap Δ_W |
| Throttling (Prop. 2) | Type-dependent throttling | Anti-throttling regulation | Worker condition degradation |
| Pricing (NeurIPS 2024) | Pricing tiers + inequality | Regulation of pricing | Wage vs. compute competition |
| SSHRC labor equity | AI access equity | Policy tools for equity | Direct labor market application |
