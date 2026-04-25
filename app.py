import streamlit as st

# ─── Data ────────────────────────────────────────────────────────────────────

INDUSTRY_MULTIPLES = {
    "Auto Dealer":                  {"low": 2.5, "mid": 3.2, "high": 3.8, "metric": "SDE"},
    "Restaurant / Food Service":    {"low": 1.8, "mid": 2.3, "high": 2.8, "metric": "SDE"},
    "Retail (general)":             {"low": 1.5, "mid": 2.1, "high": 2.6, "metric": "SDE"},
    "Medical / Dental Practice":    {"low": 3.0, "mid": 4.0, "high": 5.5, "metric": "SDE"},
    "Legal Practice":               {"low": 2.5, "mid": 3.5, "high": 5.0, "metric": "SDE"},
    "Accounting / CPA Firm":        {"low": 1.0, "mid": 1.3, "high": 1.5, "metric": "Revenue"},
    "Manufacturing":                {"low": 3.0, "mid": 4.2, "high": 5.5, "metric": "EBITDA"},
    "Distribution / Wholesale":     {"low": 2.5, "mid": 3.5, "high": 4.5, "metric": "EBITDA"},
    "IT Services / MSP":            {"low": 4.0, "mid": 5.5, "high": 7.0, "metric": "EBITDA"},
    "Landscaping / Home Services":  {"low": 2.0, "mid": 2.8, "high": 3.5, "metric": "SDE"},
    "Construction / Contracting":   {"low": 2.0, "mid": 2.8, "high": 3.5, "metric": "SDE"},
    "Trucking / Logistics":         {"low": 2.5, "mid": 3.3, "high": 4.0, "metric": "EBITDA"},
    "Staffing / Recruiting":        {"low": 3.0, "mid": 4.0, "high": 5.0, "metric": "EBITDA"},
    "E-commerce":                   {"low": 2.0, "mid": 3.0, "high": 4.5, "metric": "SDE"},
    "Other":                        {"low": 2.0, "mid": 2.8, "high": 3.5, "metric": "SDE"},
}

DEPENDENCY_QUESTIONS = [
    {
        "id": "run_without_owner",
        "question": "Can the business run for 30 days without you making decisions?",
        "weight": 20,
        "tooltip": "Buyers discount heavily when day-to-day operations require the seller's presence.",
    },
    {
        "id": "pricing_documented",
        "question": "Are your pricing rules and discount policies written down anywhere?",
        "weight": 15,
        "tooltip": "Undocumented pricing strategy walks out the door at closing.",
    },
    {
        "id": "supplier_documented",
        "question": "Are your key supplier relationships and terms documented (not just in your contacts)?",
        "weight": 15,
        "tooltip": "Personal supplier relationships are non-transferable without documentation.",
    },
    {
        "id": "processes_written",
        "question": "Do you have written SOPs (standard operating procedures) for your core workflows?",
        "weight": 15,
        "tooltip": "Undocumented processes create integration risk for the buyer.",
    },
    {
        "id": "mgmt_team",
        "question": "Do you have a management team that can operate without you day-to-day?",
        "weight": 15,
        "tooltip": "Owner-operators without a management layer face the steepest dependency discounts.",
    },
    {
        "id": "customer_relationships",
        "question": "Are customer relationships documented and tied to the business (not to you personally)?",
        "weight": 10,
        "tooltip": "If clients follow the owner out the door, the buyer is paying for relationships that leave.",
    },
    {
        "id": "financials_clean",
        "question": "Are your last 3 years of financials clean, organized, and easy to share in a data room?",
        "weight": 5,
        "tooltip": "Messy books are a red flag and create re-trading risk after LOI.",
    },
    {
        "id": "has_succession_plan",
        "question": "Do you have any written succession or transition plan?",
        "weight": 5,
        "tooltip": "Even a basic transition plan signals seller readiness and reduces closing risk.",
    },
]

CONTEXT_LAYER_IMPROVEMENTS = [
    "pricing_documented",
    "supplier_documented",
    "processes_written",
    "customer_relationships",
]

# ─── Calculation Logic ────────────────────────────────────────────────────────

def compute_owner_dependency_score(answers: dict) -> int:
    score = 0
    for q in DEPENDENCY_QUESTIONS:
        if answers.get(q["id"], False):
            score += q["weight"]
    return score


def score_to_multiple_adjustment(score: int) -> float:
    if score >= 85:
        return +0.3
    elif score >= 70:
        return 0.0
    elif score >= 55:
        return -0.4
    elif score >= 40:
        return -0.8
    elif score >= 25:
        return -1.2
    else:
        return -1.8


def concentration_adjustment(top_customer_pct: float) -> float:
    if top_customer_pct > 50:
        return -0.5
    elif top_customer_pct > 25:
        return -0.2
    else:
        return 0.0


def compute_improved_score(original_answers: dict) -> int:
    improved_answers = original_answers.copy()
    for q_id in CONTEXT_LAYER_IMPROVEMENTS:
        improved_answers[q_id] = True
    return compute_owner_dependency_score(improved_answers)


def estimate_context_layer_cost(earnings: float) -> tuple:
    if earnings < 100_000:
        return 8_000, 15_000
    elif earnings < 300_000:
        return 15_000, 25_000
    elif earnings < 600_000:
        return 25_000, 40_000
    else:
        return 40_000, 65_000


def fmt_currency(val: float) -> str:
    return f"${val:,.0f}"


def fmt_multiple(val: float) -> str:
    return f"{val:.2f}\u00d7"


def fmt_adjustment(val: float) -> str:
    sign = "+" if val >= 0 else ""
    return f"{sign}{val:.2f}\u00d7"


# ─── App ──────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Ctrl Shift — Business Succession Calculator",
    page_icon="📊",
    layout="centered",
)

# ── Header ──
st.title("Ctrl Shift — Business Succession Calculator")
st.subheader(
    "How much more could you sell your business for if your knowledge was "
    "documented and certified for the buyer?"
)
st.caption(
    "This calculator estimates the owner dependency discount a buyer will apply "
    "— and the premium you could recover."
)

st.divider()

# ── Section 2: Business Basics ──
st.header("Your Business")

industry = st.selectbox("Industry", options=list(INDUSTRY_MULTIPLES.keys()))
metric = INDUSTRY_MULTIPLES[industry]["metric"]

earnings_label = f"Annual {metric} (USD)"
if metric == "SDE":
    earnings_help = (
        "Seller's Discretionary Earnings = net profit + owner's salary + add-backs. "
        "This is the single most important number in your sale."
    )
elif metric == "EBITDA":
    earnings_help = (
        "Earnings Before Interest, Taxes, Depreciation & Amortization. "
        "Standard valuation basis for this industry."
    )
else:
    earnings_help = (
        "Annual revenue. This industry is typically valued on a revenue multiple."
    )

earnings = st.number_input(
    earnings_label,
    min_value=0,
    value=400_000,
    step=10_000,
    help=earnings_help,
)

top_customer_pct = st.slider(
    "Top customer % of revenue",
    min_value=0,
    max_value=100,
    value=20,
    step=1,
    help="What percentage of your total revenue comes from your single largest customer?",
)

years_in_business = st.number_input(
    "Years in business",
    min_value=1,
    value=10,
    step=1,
)

st.divider()

# ── Section 3: Owner Knowledge Assessment ──
st.header("How documented is your business knowledge?")
st.caption("Answer honestly. Every 'No' is a risk a buyer will price into their offer.")

answers = {}
for q in DEPENDENCY_QUESTIONS:
    answers[q["id"]] = st.checkbox(q["question"], help=q["tooltip"])

live_score = compute_owner_dependency_score(answers)
score_color = (
    "green" if live_score >= 70
    else "orange" if live_score >= 40
    else "red"
)
st.markdown(f"**Current dependency score: :{score_color}[{live_score}/100]**")
st.progress(live_score / 100)

st.divider()

# ── Section 4: Calculate ──
calculate = st.button("Calculate My Valuation Gap", type="primary", use_container_width=True)

# ── Section 5: Results ──
if calculate:
    if earnings <= 0:
        st.error("Please enter a positive earnings figure.")
        st.stop()

    base_multiple = INDUSTRY_MULTIPLES[industry]["mid"]
    dep_score = compute_owner_dependency_score(answers)
    dep_adj = score_to_multiple_adjustment(dep_score)
    conc_adj = concentration_adjustment(top_customer_pct)

    effective_multiple_A = max(base_multiple + dep_adj + conc_adj, 0.5)
    scenario_A_value = earnings * effective_multiple_A

    improved_score = compute_improved_score(answers)
    dep_adj_B = score_to_multiple_adjustment(improved_score)

    effective_multiple_B = max(base_multiple + dep_adj_B + conc_adj, 0.5)
    scenario_B_value = earnings * effective_multiple_B

    delta = scenario_B_value - scenario_A_value
    cost_low, cost_high = estimate_context_layer_cost(earnings)
    roi_low = delta / cost_high if cost_high > 0 else 0
    roi_high = delta / cost_low if cost_low > 0 else 0

    st.divider()
    st.header("Your Valuation Gap")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Scenario A — What a buyer sees today")
        st.markdown(
            f"""
| | |
|---|---|
| Industry multiple | {fmt_multiple(base_multiple)} |
| Owner dependency adj. | {fmt_adjustment(dep_adj)} |
| Concentration adj. | {fmt_adjustment(conc_adj)} |
| **Effective multiple** | **{fmt_multiple(effective_multiple_A)}** |
| **Estimated sale price** | **{fmt_currency(scenario_A_value)}** |
""",
            unsafe_allow_html=False,
        )

    with col_b:
        st.subheader("Scenario B — After encoding your knowledge")
        st.markdown(
            f"""
| | |
|---|---|
| Industry multiple | {fmt_multiple(base_multiple)} |
| Owner dependency adj. (improved) | {fmt_adjustment(dep_adj_B)} |
| Concentration adj. | {fmt_adjustment(conc_adj)} |
| **Effective multiple** | **{fmt_multiple(effective_multiple_B)}** |
| **Estimated sale price** | **{fmt_currency(scenario_B_value)}** |
""",
            unsafe_allow_html=False,
        )

    # ── Gap Box ──
    st.divider()
    st.markdown(
        f"""
<div style="border: 2px solid #4CAF50; border-radius: 8px; padding: 20px; background: #f9fff9;">
<h3 style="margin-top:0">\U0001f4b0 Encoding your knowledge could recover: <span style="color:#2e7d32">{fmt_currency(delta)}</span></h3>
<p><strong>Estimated context layer investment:</strong> ${cost_low:,}\u2013${cost_high:,}</p>
<p><strong>Estimated ROI:</strong> {roi_low:.1f}\u2013{roi_high:.1f}\u00d7</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # ── Expander ──
    with st.expander("What does the context layer actually document?"):
        st.markdown(
            """
**Pricing rules** — Your discount logic, margin targets, and exception handling are encoded into a queryable knowledge base so a buyer can replicate your decisions without you.

**Supplier relationships** — Contact terms, negotiation history, and relationship context are documented so these connections survive the ownership transition.

**Core processes (SOPs)** — Your operational workflows are captured in structured format, reducing integration risk and buyer uncertainty.

**Customer relationships** — Client history, preferences, and relationship context are tied to your CRM/business system — not to your personal contacts or memory.
"""
        )

    st.divider()
    st.caption(
        "Estimates based on BizBuySell 2024 Insight Report and IBBA Market Pulse Q4 2024. "
        "This is an estimate, not a certified appraisal. Actual sale price depends on "
        "market conditions, deal structure, and buyer-specific factors."
    )
    st.caption("Built by Ctrl Shift \u00b7 ctrl-shift.ai \u00b7 Questions? evan@ctrl-shift.ai")
else:
    st.divider()
    st.caption(
        "*Industry multiples sourced from BizBuySell 2024 Insight Report and IBBA Market Pulse Q4 2024.*"
    )
    st.caption("Built by Ctrl Shift \u00b7 ctrl-shift.ai \u00b7 Questions? evan@ctrl-shift.ai")
