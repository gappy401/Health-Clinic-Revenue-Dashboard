# Behavioral Health Clinic Analytics Dashboard

A revenue cycle and operations dashboard built to simulate what a behavioral health clinic would need to monitor daily — built as a portfolio project.

## What it tracks

**Revenue Cycle**
- Monthly billed vs. collected with 12-month trend
- Collection rate % vs. prior month
- Average days to payment

**Claim Denials**
- 12-week denial trend broken down by reason: Authorization, Eligibility, Coding Error
- Automated insight callout for top denial driver

**Authorization Workflows**
- Pending / approved / denied authorizations by payer
- Average days waiting for authorization per payer vs. 10-day target
- Automated flag for payers exceeding target wait time

## Stack
- Python · Plotly Dash · Pandas · NumPy
- Fully simulated data (no PHI)

## Run locally

```bash
pip install dash plotly pandas numpy
python app.py
```

Then open `http://localhost:8050`

Built by **Nandita Ghildyal** · [LinkedIn](https://linkedin.com/in/nanditaghildyal) · [nanditaghildyal@gmail.com](mailto:nanditaghildyal@gmail.com)
