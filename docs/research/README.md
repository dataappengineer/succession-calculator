# Succession Calculator — Methodology Research

This folder contains the supporting research used to validate and document the
valuation algorithm in the Ctrl Shift succession calculator.

The goal is not to claim precise accuracy, but to demonstrate that the direction
and magnitude of the owner dependency adjustments are consistent with documented
M&A practitioner literature.

---

## Research Documents

| # | Topic | File | Status |
|---|---|---|---|
| 1 | Owner dependency discount range (15–40% claim) | [01-owner-dependency-discount-validation.md](01-owner-dependency-discount-validation.md) | ✅ Complete |
| 2 | δ(S) breakpoint values (-1.8× to +0.3×) | [02-delta-breakpoints-validation.md](02-delta-breakpoints-validation.md) | ✅ Complete |
| 3 | Customer concentration thresholds (25%, 50%) | [03-customer-concentration-threshold.md](03-customer-concentration-threshold.md) | ✅ Complete |
| 4 | Context layer documentation impact | [04-context-layer-documentation-impact.md](04-context-layer-documentation-impact.md) | ✅ Complete |
| 5 | Methodology defense summary (client-facing) | [05-methodology-defense-summary.md](05-methodology-defense-summary.md) | ✅ Complete |

---

## How to Use This

- **For client conversations:** Start with document 5 (methodology defense summary)
- **For technical deep-dives:** Documents 1–4 contain primary citations and quoted passages
- **For algorithm changes:** Any revision to `score_to_multiple_adjustment()` or `concentration_adjustment()` should be re-validated against documents 2 and 3

---

## Sources Referenced Across All Documents

- BizBuySell 2024 Insight Report — https://bizbuysell.com/news/insight
- IBBA Market Pulse Q4 2024 — https://ibba.org
- Exit Planning Institute — https://exit-planning-institute.org
- Pepperdine Private Capital Markets Survey (annual)
- Alexandra Dawson (Concordia University) — family business succession research
