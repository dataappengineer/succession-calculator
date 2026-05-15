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

QUESTION_RISK_DETAILS = {
    "run_without_owner": {
        "risk_label": "Operations are owner-dependent",
        "implication": (
            "Buyers insert earnout clauses or reduce headline price when a business cannot run 30 days "
            "without the seller. This is the single heaviest discount factor in SME M&A — it signals "
            "that the business stops when the owner stops. SBA lenders and private equity buyers treat "
            "this as a fundamental underwriting risk."
        ),
        "buyer_flag": "Post-closing business continuity risk",
        "context_layer_fixes": False,
    },
    "pricing_documented": {
        "risk_label": "Pricing logic exits with you at closing",
        "implication": (
            "Your margin decisions, discount thresholds, and pricing exceptions live in your head. "
            "A buyer cannot replicate your pricing without you — creating immediate revenue risk "
            "the moment you leave. Buyers price this in as revenue uncertainty, not just a process gap."
        ),
        "buyer_flag": "Undocumented pricing \u2192 margin erosion risk",
        "context_layer_fixes": True,
    },
    "supplier_documented": {
        "risk_label": "Supplier relationships are personal, not institutional",
        "implication": (
            "Without documented terms, contact history, and negotiation context, a buyer has no "
            "guarantee supplier relationships survive the ownership change. Preferred pricing, "
            "extended payment terms, and informal understandings built over years do not transfer automatically."
        ),
        "buyer_flag": "Supplier continuity risk post-close",
        "context_layer_fixes": True,
    },
    "processes_written": {
        "risk_label": "Core workflows live in people's heads, not on paper",
        "implication": (
            "Integration risk is high. A buyer's team will require an extended transition period "
            "to learn how to run the business — and the earnout structure will reflect that dependency. "
            "Undocumented processes are also a liability if key employees leave post-close."
        ),
        "buyer_flag": "High integration complexity \u2192 extended earnout",
        "context_layer_fixes": True,
    },
    "mgmt_team": {
        "risk_label": "No operational layer below the owner",
        "implication": (
            "From a buyer's risk model, this is effectively a one-person operation. The business "
            "stops when the owner stops. This profile generates the largest multiple discounts in "
            "SME M&A — consistently cited in IBBA research as the primary driver of deal failure "
            "and re-trading after LOI."
        ),
        "buyer_flag": "Key man risk \u2014 no operational depth",
        "context_layer_fixes": False,
    },
    "customer_relationships": {
        "risk_label": "Customers may follow the owner, not the business",
        "implication": (
            "A buyer is paying for a customer base that could walk out the door at closing. "
            "If key clients have a personal relationship with you — not a documented, institutional "
            "one — the buyer is effectively paying for relationships they may not inherit. "
            "This is particularly acute in service businesses and professional practices."
        ),
        "buyer_flag": "Customer attrition risk post-close",
        "context_layer_fixes": True,
    },
    "financials_clean": {
        "risk_label": "Financial records may not survive due diligence scrutiny",
        "implication": (
            "Messy books stall due diligence and give buyers leverage to renegotiate after "
            "the LOI is signed — a practice known as 're-trading'. It is one of the most common "
            "deal killers in the $500k\u2013$5M transaction range and a major source of lost seller value."
        ),
        "buyer_flag": "Due diligence exposure \u2192 re-trading risk",
        "context_layer_fixes": False,
    },
    "has_succession_plan": {
        "risk_label": "No transition framework signals seller unpreparedness",
        "implication": (
            "A seller without a written transition plan raises a red flag with experienced buyers: "
            "if the owner has not thought through how they will hand over the business, what else "
            "has not been thought through? Buyers treat seller preparedness as a proxy for overall "
            "deal reliability and business quality."
        ),
        "buyer_flag": "Seller readiness concern \u2014 deal reliability signal",
        "context_layer_fixes": False,
    },
}

QUESTION_YES_NOTES = {
    "run_without_owner": "Business can operate independently \u2014 a key buyer confidence signal that commands premium multiples.",
    "pricing_documented": "Documented pricing rules reduce post-close margin uncertainty and accelerate buyer confidence.",
    "supplier_documented": "Institutional supplier relationships are transferable assets \u2014 buyers value this explicitly.",
    "processes_written": "Written SOPs reduce integration complexity and transition costs \u2014 a genuine valuation driver.",
    "mgmt_team": "Management depth is a premium multiple factor. Buyers pay more for businesses that do not need babysitting.",
    "customer_relationships": "Institutionalised customer relationships reduce post-close attrition risk significantly.",
    "financials_clean": "Clean financials accelerate due diligence, signal credibility, and eliminate re-trading risk.",
    "has_succession_plan": "A written transition plan signals a prepared seller \u2014 rare and genuinely valued by buyers.",
}

CONTEXT_LAYER_DETAIL = {
    "pricing_documented": {
        "what": "Pricing rules and margin logic",
        "how": (
            "We conduct structured interviews to extract your pricing decision tree \u2014 discount thresholds, "
            "margin targets, exception handling, and the reasoning behind each rule. The output is a "
            "queryable knowledge base a buyer's team can use from day one."
        ),
        "buyer_view": "They can now replicate your pricing decisions without you. The margin erosion risk evaporates.",
    },
    "supplier_documented": {
        "what": "Supplier relationships and negotiation context",
        "how": (
            "We document key supplier contacts, historical terms, negotiation history, payment norms, "
            "and the relationship dynamics that currently live only in your head. This becomes a "
            "structured, transferable asset in the data room."
        ),
        "buyer_view": "The relationship is now institutional, not personal. They are buying a documented supply chain, not a gamble.",
    },
    "processes_written": {
        "what": "Core operational workflows and SOPs",
        "how": (
            "We capture how your business actually runs \u2014 not an idealised flowchart, but the real "
            "decision logic, exception handling, and the things your team does because that is how "
            "the owner wants it. These become structured SOPs a new team can follow independently."
        ),
        "buyer_view": "They can integrate the business without a 12-month earnout just to figure out how things work.",
    },
    "customer_relationships": {
        "what": "Customer relationship context and history",
        "how": (
            "We encode key customer context \u2014 relationship history, communication preferences, "
            "decision-maker maps, past issues and how you resolved them \u2014 into the business's "
            "CRM and knowledge base, not your personal memory or inbox."
        ),
        "buyer_view": "They are buying relationships that survive the ownership change. Client attrition risk drops materially.",
    },
}


# ─── Tier System ─────────────────────────────────────────────────────────────

def get_tier(score: int) -> dict:
    if score >= 85:
        return {
            "label": "BUYER-READY",
            "color": "#1b5e20",
            "bg": "#e8f5e9",
            "border": "#4caf50",
            "icon": "\U0001f7e2",
            "headline": "Your business is genuinely buyer-ready \u2014 you are in the top tier of market-prepared SMEs",
            "narrative": (
                "Your responses indicate a business with real documentation depth. You have done the work most "
                "owners avoid entirely. Complete documentation across the key dimensions means buyers will see "
                "a business that can operate independently of its founder \u2014 the single most important factor "
                "in commanding a premium multiple. At this score level, the context layer is not a rescue "
                "operation; it is a certification layer that makes your existing documentation verifiable "
                "and auditable for the buyer's advisors. Buyers will still scrutinise \u2014 but they will be "
                "looking for growth risk, not operational risk."
            ),
            "symptoms": [
                "Buyers' advisors will focus on growth story rather than operational continuity risk",
                "You are positioned to command the top end of your industry's multiple range",
                "Due diligence is likely to be straightforward, accelerating time to close",
                "Any earnout provisions will be performance-based rather than transition-based",
                "You have real leverage in negotiations \u2014 motivated buyers compete for well-documented businesses",
            ],
        }
    elif score >= 70:
        return {
            "label": "LOW RISK",
            "color": "#2e7d32",
            "bg": "#f1f8e9",
            "border": "#8bc34a",
            "icon": "\U0001f7e2",
            "headline": "Your business is well-prepared \u2014 closing the remaining gaps could push you above market",
            "narrative": (
                "Your responses paint a picture of a business with meaningful documentation and operational structure. "
                "You are ahead of most SMEs that go to market. The remaining gaps, however, are visible to any "
                "experienced buyer or M&A advisor running a thorough due diligence process. The specific areas "
                "you have not yet documented tend to be where the deepest institutional knowledge sits \u2014 which "
                "is exactly why they are hard to write down, and exactly why buyers discount for them. "
                "A focused effort on the missing dimensions could move you from a good price to a full price."
            ),
            "symptoms": [
                "Buyers will identify remaining gaps but view them as addressable, not deal-breaking",
                "Earnout provisions may be included but should be manageable in scope",
                "Due diligence will surface the undocumented areas \u2014 expect targeted follow-up questions",
                "You have the foundation \u2014 the last mile separates a good outcome from a great one",
            ],
        }
    elif score >= 55:
        return {
            "label": "MILD RISK",
            "color": "#e65100",
            "bg": "#fff8e1",
            "border": "#ffc107",
            "icon": "\U0001f7e1",
            "headline": "Owner dependency is costing you on the multiple \u2014 and the gap is closable",
            "narrative": (
                "Your responses indicate a business that operates well, but where a meaningful portion of how "
                "decisions get made, relationships get managed, and pricing gets set lives primarily with you. "
                "Buyers and their advisors are trained to find exactly these gaps \u2014 and when they find them, "
                "they price them in. The good news: you are close to the threshold where the multiple discount "
                "disappears entirely. Most businesses at this profile can move to the next tier with two to "
                "three months of focused knowledge capture and documentation work."
            ),
            "symptoms": [
                "Buyers will identify dependency risk but view you as a fixable opportunity",
                "Expect a longer due diligence process as advisors probe undocumented areas",
                "Price negotiations will likely centre on transition risk and earnout structure",
                "You may be asked to remain involved for 6\u201312 months post-close to bridge the knowledge gap",
            ],
        }
    elif score >= 40:
        return {
            "label": "MODERATE RISK",
            "color": "#bf360c",
            "bg": "#fff3e0",
            "border": "#ff5722",
            "icon": "\U0001f7e0",
            "headline": "A buyer today would apply a material owner dependency discount \u2014 this is costing you right now",
            "narrative": (
                "Your responses show a business with some operational foundations but significant gaps in documented "
                "knowledge. Buyers conducting due diligence on businesses at this profile routinely flag owner "
                "dependency as a material risk factor \u2014 and adjust their offers accordingly. The most common "
                "outcomes at this level: a discounted purchase price, an extended earnout tying you to the "
                "business for 2\u20133 years post-close, or a failed deal when the buyer's advisors cannot get "
                "comfortable with what is undocumented. The IBBA consistently identifies owner dependency as "
                "one of the top three reasons SME deals fall through or close below seller expectations."
            ),
            "symptoms": [
                "Buyers will flag multiple dependency risk factors in their due diligence report",
                "Earnout provisions of 2\u20133 years are common at this risk profile",
                "SBA lenders who finance most SME acquisitions will scrutinise owner dependency closely",
                "The business value on paper versus what you receive at closing can diverge significantly",
                "Deals may stall at the LOI stage when buyers see the full due diligence picture",
            ],
        }
    elif score >= 25:
        return {
            "label": "HIGH RISK",
            "color": "#b71c1c",
            "bg": "#ffebee",
            "border": "#f44336",
            "icon": "\U0001f534",
            "headline": "Your business would face a significant discount at closing \u2014 the gap between expectation and offer is large",
            "narrative": (
                "Your responses point to a business where the owner is deeply embedded in operations, client "
                "relationships, and institutional knowledge across multiple dimensions. This is the profile "
                "that buyers discount most aggressively \u2014 not because the business is not good, but because "
                "a buyer cannot verify it will continue to be good after you leave. M&A advisors report that "
                "businesses at this dependency level receive effective multiple discounts of 25\u201340% from "
                "their industry baseline. Many simply do not close at all \u2014 the gap between seller expectations "
                "and buyer risk-adjusted offers is too wide to bridge without documentation work."
            ),
            "symptoms": [
                "Buyers will require a long transition period \u2014 often 12\u201324 months \u2014 eroding your post-sale freedom",
                "Multiple due diligence red flags across operational, financial, and relationship dimensions",
                "SBA financing may be difficult to secure \u2014 lenders apply the same risk lens as buyers",
                "Earnout provisions will likely represent 30\u201350% of the headline price",
                "Deals at this dependency level fall through at 2\u20133x the average rate",
                "Advisors may recommend a delay-to-prepare strategy rather than going to market now",
            ],
        }
    else:
        return {
            "label": "CRITICAL RISK",
            "color": "#7f0000",
            "bg": "#ffcdd2",
            "border": "#d32f2f",
            "icon": "\U0001f534",
            "headline": "The business and the owner are effectively the same entity \u2014 a buyer will see this within the first week of due diligence",
            "narrative": (
                "Your responses indicate a business where institutional knowledge, operational decisions, customer "
                "relationships, and financial management are all concentrated in the owner. This is the most "
                "common profile among businesses that are listed but never actually close \u2014 not because the "
                "business is not valuable, but because the value cannot be separated from the person. "
                "A buyer's core concern is simple: what happens after you leave? When the answer to most "
                "due diligence questions is 'ask the owner', there is no transferable business to buy \u2014 "
                "only a job offer disguised as an acquisition. The theoretical multiple for your industry "
                "is real. Achieving it requires first separating the business from the owner operationally."
            ),
            "symptoms": [
                "Due diligence will surface fundamental operational dependency within the first week",
                "Buyers who proceed will do so at a steep discount or with aggressive multi-year earnout structures",
                "SBA and conventional acquisition financing will be difficult to obtain at standard terms",
                "Most advisors will recommend a delay-to-prepare strategy before taking the business to market",
                "The gap between your expected price and what the market will actually pay is likely $200k\u2013$800k+",
                "Even motivated buyers will walk when they see the full dependency picture in due diligence",
            ],
        }


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
    return f"{val:.2f}x"


def fmt_adj(val: float) -> str:
    return f"{val:+.2f}x"


# ─── App ──────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Ctrl Shift \u2014 Business Succession Calculator",
    page_icon="\U0001f4ca",
    layout="centered",
)

st.title("Ctrl Shift \u2014 Business Succession Calculator")
st.subheader(
    "How much more could you sell your business for if your knowledge was "
    "documented and certified for the buyer?"
)
st.caption(
    "This calculator estimates the owner dependency discount a buyer will apply "
    "\u2014 and the premium you could recover by encoding your institutional knowledge."
)

st.divider()

# ── Section 2: Business Basics ──────────────────────────────────────────────
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
        "Earnings Before Interest, Taxes, Depreciation and Amortization. "
        "Standard valuation basis for this industry."
    )
else:
    earnings_help = "Annual revenue. This industry is typically valued on a revenue multiple."

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

# ── Section 3: Owner Knowledge Assessment ───────────────────────────────────
st.header("How documented is your business knowledge?")
st.caption("Answer honestly. Every No is a risk a buyer will price into their offer.")

answers = {}
for q in DEPENDENCY_QUESTIONS:
    answers[q["id"]] = st.checkbox(q["question"], help=q["tooltip"])

live_score = compute_owner_dependency_score(answers)
score_color = "green" if live_score >= 70 else "orange" if live_score >= 40 else "red"
st.markdown(
    f"**Dependency score: :{score_color}[{live_score}/100]** \u2014 higher is better (70+ = no multiple penalty)"
)
st.progress(live_score / 100)

st.divider()

# ── Section 4: Calculate Button ─────────────────────────────────────────────
calculate = st.button("Calculate My Valuation Gap", type="primary", use_container_width=True)

# ── Section 5: Results ───────────────────────────────────────────────────────
if calculate:
    if earnings <= 0:
        st.error("Please enter a positive earnings figure.")
        st.stop()

    # Core calculations
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
    roi_low = delta / cost_high if cost_high > 0 and delta > 0 else 0
    roi_high = delta / cost_low if cost_low > 0 and delta > 0 else 0

    tier = get_tier(dep_score)
    no_answers = [q for q in DEPENDENCY_QUESTIONS if not answers.get(q["id"], False)]
    yes_answers = [q for q in DEPENDENCY_QUESTIONS if answers.get(q["id"], False)]

    # ── Report Badge ──────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        f"""<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:6px;">
  <span style="background:#e0f2f1; color:#00695c; font-size:11px; font-weight:700;
    letter-spacing:0.12em; padding:4px 12px; border-radius:4px;">
    &#10003; YOUR SUCCESSION READINESS REPORT
  </span>
  <span style="background:{tier['bg']}; color:{tier['color']}; font-size:11px; font-weight:700;
    letter-spacing:0.12em; padding:4px 12px; border-radius:4px; border:1px solid {tier['border']};">
    {tier['icon']} {tier['label']}
  </span>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Headline ──────────────────────────────────────────────────────────────
    st.markdown(f"### {tier['headline']}")
    st.caption(
        f"Industry: **{industry}** \u00b7 {metric}: **{fmt_currency(earnings)}** \u00b7 "
        f"Top customer: **{top_customer_pct}%** of revenue \u00b7 **{years_in_business}** years in business"
    )

    # ── Four Metric Cards ─────────────────────────────────────────────────────
    st.markdown("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            "Owner Dependency Score",
            f"{dep_score}/100",
            f"{dep_score - 70:+d}pts vs no-penalty threshold",
            delta_color="normal",
        )
    with m2:
        total_adj = dep_adj + conc_adj
        st.metric(
            "Effective Multiple Today",
            fmt_multiple(effective_multiple_A),
            f"{total_adj:+.2f}x from {base_multiple:.1f}x base",
            delta_color="normal",
        )
    with m3:
        st.metric("Estimated Sale Price Today", fmt_currency(scenario_A_value))
    with m4:
        if delta > 0:
            st.metric("Recoverable Value", fmt_currency(delta), "with context layer", delta_color="off")
        else:
            st.metric("Valuation Gap", "$0", "already at max multiple", delta_color="off")

    # ── Narrative ─────────────────────────────────────────────────────────────
    st.divider()
    st.markdown(tier["narrative"])
    st.markdown("")
    st.markdown("**Patterns at this risk level that buyers and their advisors typically find:**")
    for symptom in tier["symptoms"]:
        st.markdown(f"&bull; {symptom}")

    # Concentration risk callout
    if top_customer_pct > 25:
        conc_level = "significant" if top_customer_pct > 50 else "material"
        st.markdown(
            f"""<div style="border-left:4px solid #f57f17; background:#fff8e1; padding:10px 14px;
  border-radius:0 6px 6px 0; margin-top:12px;">
  <strong style="color:#e65100;">&#9888; Concentration risk flag:</strong>
  <span style="font-size:13px; color:#555;">
    Your top customer represents {top_customer_pct}% of revenue. This is a {conc_level} concentration
    risk that buyers apply a separate {fmt_adj(conc_adj)} multiple discount to \u2014 independent of owner
    dependency. Buyers will probe whether that customer relationship is personal or contractual, and
    whether it survives an ownership change.
  </span>
</div>""",
            unsafe_allow_html=True,
        )

    # ── Risk Flag Breakdown ───────────────────────────────────────────────────
    st.divider()
    st.subheader("Your Risk Profile \u2014 What a Buyer's Advisor Will Find")

    if no_answers:
        no_sorted = sorted(no_answers, key=lambda q: q["weight"], reverse=True)
        st.markdown(
            f"**{len(no_sorted)} risk flag{'s' if len(no_sorted) > 1 else ''} identified.** "
            "These are the dimensions a buyer will discount for, ordered by multiple impact:"
        )
        st.markdown("")
        for q in no_sorted:
            qd = QUESTION_RISK_DETAILS[q["id"]]
            fix_badge = (
                "<span style='font-size:10px; background:#e8f5e9; color:#2e7d32; "
                "padding:2px 7px; border-radius:3px; font-weight:700; margin-left:8px;'>"
                "&#10022; CONTEXT LAYER FIXES THIS</span>"
                if qd["context_layer_fixes"] else ""
            )
            st.markdown(
                f"""<div style="border-left:4px solid #f44336; background:#fff5f5; padding:14px 16px;
  margin-bottom:10px; border-radius:0 6px 6px 0;">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:6px;">
    <div>
      <span style="font-weight:700; color:#c62828; font-size:14px;">&#128681; {qd['risk_label']}</span>
      {fix_badge}
    </div>
    <span style="font-size:11px; color:#999; white-space:nowrap;">Weight: {q['weight']}pts</span>
  </div>
  <p style="margin:8px 0 6px; font-size:13px; color:#444; line-height:1.5;">{qd['implication']}</p>
  <span style="font-size:11px; background:#ffebee; color:#c62828; padding:2px 8px;
    border-radius:3px; font-weight:600;">Buyer flag: {qd['buyer_flag']}</span>
</div>""",
                unsafe_allow_html=True,
            )

    if yes_answers:
        st.markdown("")
        st.markdown(
            f"**{len(yes_answers)} strength{'s' if len(yes_answers) > 1 else ''} documented.** "
            "These reduce your risk profile and support the multiple:"
        )
        st.markdown("")
        for q in yes_answers:
            yn = QUESTION_YES_NOTES[q["id"]]
            st.markdown(
                f"""<div style="border-left:4px solid #4caf50; background:#f9fff9; padding:10px 16px;
  margin-bottom:8px; border-radius:0 6px 6px 0;">
  <span style="font-weight:700; color:#2e7d32;">&#10003; {q['question']}</span>
  <p style="margin:4px 0 0; font-size:13px; color:#555;">{yn}</p>
</div>""",
                unsafe_allow_html=True,
            )

    # ── Scenario Comparison ───────────────────────────────────────────────────
    st.divider()
    st.subheader("Your Valuation \u2014 The Full Picture")
    st.caption(
        "The only difference between Scenario A and B is what is documented. "
        "Financial performance, industry, and customer concentration are identical in both."
    )
    st.markdown("")

    col_a, col_b = st.columns(2)

    dep_adj_color_a = "#c62828" if dep_adj < 0 else "#2e7d32"
    dep_adj_color_b = "#c62828" if dep_adj_B < 0 else "#2e7d32"
    conc_color = "#c62828" if conc_adj < 0 else "#555"

    with col_a:
        st.markdown(
            f"""<div style="border:1px solid #ffccbc; background:#fff8f5; border-radius:8px; padding:18px;">
  <p style="font-size:11px; font-weight:700; letter-spacing:0.15em; color:#bf360c; margin:0 0 12px;">
    SCENARIO A &mdash; TODAY
  </p>
  <table style="width:100%; font-size:13px; border-collapse:collapse;">
    <tr>
      <td style="color:#666; padding:4px 0;">Industry base multiple</td>
      <td style="text-align:right; font-weight:600; color:#333;">{fmt_multiple(base_multiple)}</td>
    </tr>
    <tr>
      <td style="color:#666; padding:4px 0;">Owner dependency adj.</td>
      <td style="text-align:right; font-weight:600; color:{dep_adj_color_a};">{fmt_adj(dep_adj)}</td>
    </tr>
    <tr>
      <td style="color:#666; padding:4px 0;">Concentration adj.</td>
      <td style="text-align:right; font-weight:600; color:{conc_color};">{fmt_adj(conc_adj)}</td>
    </tr>
    <tr style="border-top:1px solid #ffccbc;">
      <td style="color:#333; padding:8px 0 4px; font-weight:700;">Effective multiple</td>
      <td style="text-align:right; font-weight:800; font-size:16px; color:#333; padding:8px 0 4px;">
        {fmt_multiple(effective_multiple_A)}
      </td>
    </tr>
  </table>
  <div style="background:#ffebee; border-radius:6px; padding:12px 14px; margin-top:12px;">
    <p style="font-size:11px; color:#888; margin:0 0 3px;">Estimated sale price</p>
    <p style="font-size:26px; font-weight:800; color:#b71c1c; margin:0;">{fmt_currency(scenario_A_value)}</p>
  </div>
  <p style="font-size:11px; color:#aaa; margin:8px 0 0;">Dependency score: {dep_score}/100</p>
</div>""",
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""<div style="border:1px solid #a5d6a7; background:#f5fff5; border-radius:8px; padding:18px;">
  <p style="font-size:11px; font-weight:700; letter-spacing:0.15em; color:#1b5e20; margin:0 0 12px;">
    SCENARIO B &mdash; AFTER CONTEXT LAYER
  </p>
  <table style="width:100%; font-size:13px; border-collapse:collapse;">
    <tr>
      <td style="color:#666; padding:4px 0;">Industry base multiple</td>
      <td style="text-align:right; font-weight:600; color:#333;">{fmt_multiple(base_multiple)}</td>
    </tr>
    <tr>
      <td style="color:#666; padding:4px 0;">Owner dependency adj. (improved)</td>
      <td style="text-align:right; font-weight:600; color:{dep_adj_color_b};">{fmt_adj(dep_adj_B)}</td>
    </tr>
    <tr>
      <td style="color:#666; padding:4px 0;">Concentration adj.</td>
      <td style="text-align:right; font-weight:600; color:{conc_color};">{fmt_adj(conc_adj)}</td>
    </tr>
    <tr style="border-top:1px solid #a5d6a7;">
      <td style="color:#333; padding:8px 0 4px; font-weight:700;">Effective multiple</td>
      <td style="text-align:right; font-weight:800; font-size:16px; color:#333; padding:8px 0 4px;">
        {fmt_multiple(effective_multiple_B)}
      </td>
    </tr>
  </table>
  <div style="background:#e8f5e9; border-radius:6px; padding:12px 14px; margin-top:12px;">
    <p style="font-size:11px; color:#888; margin:0 0 3px;">Estimated sale price</p>
    <p style="font-size:26px; font-weight:800; color:#1b5e20; margin:0;">{fmt_currency(scenario_B_value)}</p>
  </div>
  <p style="font-size:11px; color:#aaa; margin:8px 0 0;">Improved dependency score: {improved_score}/100</p>
</div>""",
            unsafe_allow_html=True,
        )

    # ── The Gap ───────────────────────────────────────────────────────────────
    st.divider()
    if delta > 0:
        st.markdown(
            f"""<div style="border:2px solid #2e7d32; border-radius:10px; padding:24px; background:#f5fff5;">
  <p style="font-size:11px; font-weight:700; letter-spacing:0.15em; color:#2e7d32; margin:0 0 4px;">
    YOUR VALUATION GAP
  </p>
  <h2 style="margin:0 0 18px; color:#1b5e20; font-size:20px;">
    Encoding your knowledge could recover
    <span style="font-size:1.4em; display:block; margin-top:4px;">{fmt_currency(delta)}</span>
  </h2>
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:16px;">
    <div style="background:white; border-radius:6px; padding:14px; border:1px solid #c8e6c9;">
      <p style="font-size:11px; color:#888; margin:0 0 4px;">Valuation gap</p>
      <p style="font-size:22px; font-weight:800; color:#1b5e20; margin:0;">{fmt_currency(delta)}</p>
    </div>
    <div style="background:white; border-radius:6px; padding:14px; border:1px solid #c8e6c9;">
      <p style="font-size:11px; color:#888; margin:0 0 4px;">Context layer investment</p>
      <p style="font-size:22px; font-weight:800; color:#1b5e20; margin:0;">${cost_low:,}&ndash;${cost_high:,}</p>
    </div>
    <div style="background:white; border-radius:6px; padding:14px; border:1px solid #c8e6c9;">
      <p style="font-size:11px; color:#888; margin:0 0 4px;">Estimated ROI</p>
      <p style="font-size:22px; font-weight:800; color:#1b5e20; margin:0;">{roi_low:.1f}&ndash;{roi_high:.1f}x</p>
    </div>
  </div>
  <p style="font-size:13px; color:#555; margin:0; line-height:1.6;">
    The context layer costs a fraction of what it recovers. For most businesses at this earnings level,
    the documentation work pays for itself the moment it shifts the effective multiple by even 0.1x.
    The engagement typically runs 6&ndash;10 weeks &mdash; well inside a standard M&A timeline.
  </p>
</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div style="border:2px solid #2e7d32; border-radius:10px; padding:24px; background:#f5fff5;">
  <p style="font-size:11px; font-weight:700; letter-spacing:0.15em; color:#2e7d32; margin:0 0 4px;">
    YOUR VALUATION POSITION
  </p>
  <h2 style="margin:0 0 10px; color:#1b5e20;">
    Your documentation already captures the full multiple premium.
  </h2>
  <p style="font-size:13px; color:#555; margin:0; line-height:1.6;">
    The four dimensions the context layer addresses are already documented in your business.
    Your effective multiple is at or near the premium for your industry. The remaining opportunity,
    if any, lies in the dimensions the context layer does not directly affect &mdash; such as
    building management team depth or adding a formal succession plan.
  </p>
</div>""",
            unsafe_allow_html=True,
        )

    # ── What the Context Layer Changes ───────────────────────────────────────
    cl_gaps = [
        q for q in DEPENDENCY_QUESTIONS
        if q["id"] in CONTEXT_LAYER_IMPROVEMENTS and not answers.get(q["id"], False)
    ]
    cl_done = [
        q for q in DEPENDENCY_QUESTIONS
        if q["id"] in CONTEXT_LAYER_IMPROVEMENTS and answers.get(q["id"], False)
    ]

    with st.expander("What exactly does the context layer change?", expanded=bool(cl_gaps)):
        st.markdown(
            "The context layer directly addresses **4 of the 8 owner dependency dimensions** \u2014 "
            "the ones most amenable to systematic knowledge capture. Here is what changes and why it matters:"
        )
        st.markdown("")

        if cl_gaps:
            st.markdown("**Gaps the context layer addresses in your case:**")
            st.markdown("")
            for q in cl_gaps:
                detail = CONTEXT_LAYER_DETAIL[q["id"]]
                st.markdown(
                    f"""<div style="border:1px solid #a5d6a7; border-radius:8px; padding:16px; margin-bottom:12px; background:#f5fff5;">
  <p style="font-weight:700; color:#1b5e20; margin:0 0 8px; font-size:14px;">&#10022; {detail['what']}</p>
  <p style="font-size:13px; color:#444; margin:0 0 6px; line-height:1.5;">
    <strong>How we document it:</strong> {detail['how']}
  </p>
  <p style="font-size:13px; color:#2e7d32; margin:0; line-height:1.5;">
    <strong>From a buyer's perspective:</strong> {detail['buyer_view']}
  </p>
</div>""",
                    unsafe_allow_html=True,
                )

        if cl_done:
            st.markdown("**Already documented \u2014 no change needed:**")
            for q in cl_done:
                detail = CONTEXT_LAYER_DETAIL[q["id"]]
                st.markdown(
                    f"&#10003; **{detail['what']}** \u2014 already in place. "
                    "This is a genuine valuation asset and will be highlighted positively in your data room."
                )

        st.markdown("")
        st.markdown(
            """**The 4 dimensions the context layer does NOT directly change:**

These require genuine operational changes, not documentation sprints:
- **Operational independence** \u2014 whether the business can function 30 days without you
- **Management team depth** \u2014 whether there is an operational layer below the owner
- **Financial record quality** \u2014 whether 3 years of clean, organised books exist
- **Succession plan** \u2014 whether a formal written transition plan exists

We advise on a path toward each of these, but they require structural work beyond knowledge capture."""
        )

    # ── What Buyers Look For ──────────────────────────────────────────────────
    with st.expander("What does a buyer's due diligence actually look for?"):
        st.markdown(
            """When a serious buyer submits a Letter of Intent and enters due diligence, their advisors
work through a structured checklist. Here is what they look for \u2014 and how your profile maps to each category.

---

**Financial Due Diligence**
- 3 years of P&L statements, balance sheets, and tax returns \u2014 and the ability to explain every material line
- SDE or EBITDA recasting: identifying which expenses are genuine add-backs vs. business expenses
- Working capital normalisation: how much cash needs to stay in the business post-close
- Revenue concentration: what percentage comes from the top 3\u20135 customers, and are those relationships contractual?

**Operational Due Diligence**
- Can the business operate without the owner for 30+ days? Who makes decisions?
- Are core processes documented? Can a new management team follow them without the seller?
- What is the management depth \u2014 who runs things when the owner is unavailable?
- Are there single points of failure in operations, technology, or people?

**Commercial Due Diligence**
- Are customer relationships institutional (tied to the business) or personal (tied to the owner)?
- Is revenue recurring, contracted, or transactional? What is the churn rate?
- Are supplier terms documented and transferable to a new owner?
- What is the competitive position and is it defensible post-close?

**Legal and Risk Due Diligence**
- Are there key man clauses in supplier or customer contracts that trigger on ownership change?
- Are employment agreements, IP assignments, and non-competes in order?
- Are there pending disputes, contingent liabilities, or undisclosed obligations?
- Are licenses, permits, and certifications transferable?

**Knowledge and Transition Due Diligence** *(where the context layer matters most)*
- Is there a written transition plan? What does the handover look like?
- Can institutional knowledge \u2014 pricing logic, supplier relationships, operational judgment \u2014 be transferred?
- Is the seller's involvement post-close necessary, and for how long?
- Are customer relationships documented and transferable, or will clients follow the owner out the door?

---

Businesses that close at the top of their multiple range are the ones that can answer yes to most of these
questions \u2014 with evidence in the data room, not just verbal assurances at the LOI stage."""
        )

    # ── CTA Card ──────────────────────────────────────────────────────────────
    st.divider()
    gap_text = (
        f"The {fmt_currency(delta)} gap between what your business is worth today and what it could be "
        f"worth after encoding your knowledge is recoverable. Most businesses complete the context layer "
        f"engagement in 6\u201310 weeks \u2014 well before a typical sale process closes."
        if delta > 0
        else (
            "Your documentation is already strong. If you want to validate your position, discuss deal "
            "structure, or explore how to push toward the premium end of your industry range, we can help."
        )
    )
    st.markdown(
        f"""<div style="border:1px solid #1565c0; border-radius:8px; padding:22px 26px; background:#e3f2fd;">
  <p style="font-weight:700; font-size:16px; color:#0d47a1; margin:0 0 8px;">Ready to close this gap?</p>
  <p style="font-size:13px; color:#444; margin:0 0 14px; line-height:1.6;">{gap_text}</p>
  <p style="font-size:13px; color:#333; margin:0; line-height:1.8;">
    &#128231; Book a discovery call:
    <strong><a href="mailto:evan@ctrl-shift.ai" style="color:#1565c0;">evan@ctrl-shift.ai</a></strong>
    &nbsp;&middot;&nbsp;
    &#127760; <strong><a href="https://ctrl-shift.ai" style="color:#1565c0;">ctrl-shift.ai</a></strong>
  </p>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Footer ────────────────────────────────────────────────────────────────
    st.divider()
    st.caption(
        "Estimates based on BizBuySell 2024 Insight Report and IBBA Market Pulse Q4 2024. "
        "This is an estimate, not a certified appraisal. Actual sale price depends on market "
        "conditions, deal structure, and buyer-specific factors."
    )
    st.caption("Built by Ctrl Shift \u00b7 ctrl-shift.ai \u00b7 Questions? evan@ctrl-shift.ai")

else:
    st.divider()
    st.caption(
        "*Industry multiples sourced from BizBuySell 2024 Insight Report and IBBA Market Pulse Q4 2024.*"
    )
    st.caption("Built by Ctrl Shift \u00b7 ctrl-shift.ai \u00b7 Questions? evan@ctrl-shift.ai")
