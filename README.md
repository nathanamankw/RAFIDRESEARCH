# RAFID RESEARCH

## Routing, Cascades, and User Choice for LLMs

This repository contains research materials for the paper "Routing, Cascades, and User Choice for LLMs" (under review at ICLR 2026).

### Overview

The paper studies the effect of LLM routing with respect to user behavior. It proposes a Stackelberg game between an LLM provider with two models (standard and reasoning) and a user who can re-prompt or abandon tasks if the routed model cannot solve them.

### Key Contributions

- **User best response characterization**: User patience depends on the net value (expected utility minus latency) of each model
- **Optimal routing policies**: In nearly all cases, the optimal routing policy is static with no cascading
- **Provider-user misalignment**: A gap exists when provider cost rankings and user utility rankings of models differ
- **Throttling risk**: Low churn penalties can incentivize providers to artificially inflate latency

### Files

- `7645_Routing_Cascades_and_User.pdf` — Full paper manuscript
