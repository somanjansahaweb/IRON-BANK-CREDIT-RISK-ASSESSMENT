<div align="center">
  <h1>🏦 IRON BANK</h1>
  <p><b>Automated Credit Risk Assessment & Portfolio Analytics Engine</b></p>

  ![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
  ![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)
  ![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
  ![Matplotlib](https://img.shields.io/badge/Matplotlib-Visuals-11557c?style=for-the-badge&logo=python&logoColor=white)
</div>

<br>

A production-ready credit risk evaluation pipeline that ingests borrower data, calculates core financial metrics, classifies risk, stores results in SQLite, and generates portfolio visualizations.

## Project Overview

Iron Bank simulates an automated decision engine for credit assessment and portfolio analytics. It computes key lending metrics such as DTI, DSCR, EMI, and credit-based risk tiers, then persists evaluations to a database and produces a visual dashboard.

## Features

- Borrower data validation and structured input handling.
- Financial metric calculation for DTI, DSCR, and EMI.
- Risk classification using multiple financial signals.
- SQLite persistence for evaluated borrower records.
- CSV export for audit and review.
- Portfolio visualization with Matplotlib charts.


## System Architecture 
The engine is built using a strict 6-layer pipeline to ensure clean code and easy maintenance:

* Borrower (Data Layer): Stores applicant data and handles basic validation.
* RiskEngine (Math Layer): Computes amortized monthly payments, DTI, and DSCR.
* CreditPersistence (Storage Layer): Saves bulk evaluations to SQLite and CSV files.
* CreditDecision (Business Logic): Translates the risk score into a final loan decision.
* GenerateCreditMemo (Reporting): Formats terminal summaries for individual reviews.
* Visualisation (Analytics): Generates a Matplotlib dashboard for portfolio risk.

---

## Financial Modeling Logic
The decision engine uses a majority voting system across three key financial metrics:

**Debt-to-Income (DTI)**
* Low Risk: Under 36%
* Medium Risk: 36% to 45%
* High Risk: Over 45%

**Debt Service Coverage Ratio (DSCR)**
* Low Risk: Over 1.25
* Medium Risk: 1.15 to 1.25
* High Risk: Under 1.15

**Credit Score**
* Low Risk: 700 or higher
* Medium Risk: 620 to 699
* High Risk: Under 620

**Verdict Engine:** If two or more metrics return High Risk, the final verdict is High Risk. If the metrics heavily conflict, the system flags the application as Undetermined Risk for manual review.

---

## Portfolio Analytics
The system automatically plots the dataset to provide a macro-level view of portfolio health.

![Iron Bank Portfolio Dashboard](https://github.com/user-attachments/assets/f67378f8-0970-400d-a322-e20450a7d977)

**Dashboard Breakdown:**
* Risk Verdict Distribution (Bar Chart): Shows the total count of safe vs. high-risk applicants.
* Credit Score Distribution (Histogram): Shows the applicant pool's credit scores against the 620 and 700 thresholds.
* DTI vs. DSCR by Risk Tier (Scatter Plot): Maps individual borrowers to easily isolate high-risk outliers.

## Project Structure

* **`iron_bank.py`** — Main application script containing the 6-Layer Architecture.
* **`loanset.csv`** — The raw borrower input dataset.
* **`credit_risk_assessment.db`** — SQLite database where bulk evaluations are stored (Auto-generated).
* **`CREDIT_RISK_ASSESSMENT_*.csv`** — Time-stamped output logs of the evaluations (Auto-generated).
* **`README.md`** — Project documentation.
