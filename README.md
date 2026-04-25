# Ctrl Shift — Business Succession Calculator

> *"You don't sell your business for the price you think you can get. You sell for the price you can prove."*

A free, shareable web calculator that shows SME owners the owner-dependency discount a buyer will apply at closing — and the premium they could recover by encoding their institutional knowledge before the sale.

Built by **[Ctrl Shift](https://ctrl-shift.ai)** (Evan Pitchie + Giovanni Brucoli), an AI consulting company focused on the SME succession planning market.

---

## What It Does

The calculator takes a business owner through two scenarios:

- **Scenario A — What a buyer sees today:** business value based on documented data only, with an owner dependency discount applied based on how much institutional knowledge lives only in the owner's head.
- **Scenario B — After encoding your knowledge:** same business, same financials, but the owner dependency risk is reduced because pricing rules, supplier relationships, SOPs, and customer context are now in a certified context layer.

**The gap between A and B is the ROI argument for a Ctrl Shift engagement.**

### Example output

```
Auto Dealer · $400,000 SDE · top customer 20% · all questions "No"

Scenario A (today):             $960,000   (2.4× effective multiple)
Scenario B (context layer):  $1,200,000   (3.0× effective multiple)

Delta:                          +$240,000
Context layer cost:             $15k–$25k
ROI:                            9.6–16×
```

---

## Run Locally

```bash
git clone https://github.com/dataappengineer/succession-calculator.git
cd succession-calculator
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Deploy to Streamlit Community Cloud (one click)

1. Fork or push this repo to your GitHub account (must be public).
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Click **"New app"** → select your repo → set the **main file path** to `app.py`.
4. Click **"Deploy"**. No secrets, no environment variables required.

You'll get a shareable URL like `https://your-app-name.streamlit.app` within ~2 minutes.

---

## Data Sources

Industry SDE/EBITDA multiples and owner dependency discount methodology are sourced from:

- **BizBuySell 2024 Insight Report** — annual survey of closed small business transactions in the US
- **IBBA Market Pulse Q4 2024** — International Business Brokers Association quarterly benchmark report

All numbers are rule-based and fully traceable. No ML models. No random numbers. Every adjustment is explainable.

---

## Stack

| Layer | Technology |
|---|---|
| UI & logic | Python + Streamlit |
| Hosting | Streamlit Community Cloud (free) |
| Data | Hardcoded lookup tables — no database |
| Dependencies | `streamlit`, `pandas` |

---

## Contact

Questions or partnership inquiries: **evan@ctrl-shift.ai**  
Website: [ctrl-shift.ai](https://ctrl-shift.ai)
