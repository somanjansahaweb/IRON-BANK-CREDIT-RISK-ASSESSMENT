# 🏦 IRON BANK
**Automated Credit Risk Assessment & Portfolio Analytics Engine**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visuals-11557c?style=for-the-badge&logo=python&logoColor=white)

---

## 📌 Project Overview
Iron Bank is a production-ready credit risk evaluation pipeline that ingests borrower data, calculates core financial metrics, classifies risk, stores results in SQLite, and generates portfolio visualizations. 

This project bridges the gap between theoretical econometrics and applied data engineering, simulating the automated decisioning engines used in commercial banking and risk advisory.

## 📋 Table of Contents
* [Features](#features)
* [System Architecture](#system-architecture)
* [Financial Modeling Logic](#financial-modeling-logic)
* [Portfolio Analytics](#portfolio-analytics)
* [Industry Application & Theory](#industry-application--theory)
* [Future Roadmap](#future-roadmap)
* [Project Structure](#project-structure)
* [Author](#author)

---

## ✨ Features
* Borrower data validation and structured input handling.
* Financial metric calculation for DTI, DSCR, and EMI.
* Risk classification using multiple financial signals.
* SQLite persistence for evaluated borrower records and audit trails.
* CSV export for secondary analysis and review.
* Portfolio visualization with automated Matplotlib dashboards.

---

## 🏗️ System Architecture 
The engine is built using a strict 6-layer pipeline to ensure clean code and easy maintenance:

* **Borrower (Data Layer):** Stores applicant data and handles basic validation.
* **RiskEngine (Math Layer):** Computes amortized monthly payments, DTI, and DSCR.
* **CreditPersistence (Storage Layer):** Saves bulk evaluations to SQLite and CSV files.
* **CreditDecision (Business Logic):** Translates the risk score into a final loan decision.
* **GenerateCreditMemo (Reporting):** Formats terminal summaries for individual reviews.
* **Visualisation (Analytics):** Generates a Matplotlib dashboard for portfolio risk.

---

## 🧮 Financial Modeling Logic
The decision engine uses a deterministic "majority voting" system across three key financial metrics to predict default probability:

**Debt-to-Income (DTI)**
* Low Risk: Under 36% | Medium Risk: 36% to 45% | High Risk: Over 45%

**Debt Service Coverage Ratio (DSCR)**
* Low Risk: Over 1.25 | Medium Risk: 1.15 to 1.25 | High Risk: Under 1.15

**Credit Score**
* Low Risk: 700 or higher | Medium Risk: 620 to 699 | High Risk: Under 620

**Verdict Engine:** If two or more metrics return High Risk, the final verdict is High Risk. If the metrics heavily conflict, the system flags the application as "Undetermined Risk" for manual review.

---

## 📊 Portfolio Analytics
The system automatically plots the dataset to provide a macro-level view of portfolio health.

![Iron Bank Portfolio Dashboard](https://github.com/user-attachments/assets/f67378f8-0970-400d-a322-e20450a7d977)

**Dashboard Breakdown:**
* **Risk Verdict Distribution (Bar Chart):** Shows the total count of safe vs. high-risk applicants, informing macro-lending strategy.
* **Credit Score Distribution (Histogram):** Shows the applicant pool's credit scores against the 620 floor and 700 target thresholds.
* **DTI vs. DSCR by Risk Tier (Scatter Plot):** Maps individual borrowers to isolate high-risk outliers. Safe applications cluster in high-cash-flow/low-debt zones.

---

## 🏦 Industry Application & Theory
This engine mirrors the architecture of risk assessment systems running inside modern financial institutions:

* **Econometrics (Solvency vs. Liquidity):** The system evaluates both solvency via DTI (how much wealth is owed) and liquidity via DSCR (the ability to generate cash flow to cover the EMI). This creates a composite risk profile where a single strong metric cannot mask a fatal financial flaw.
* **Straight-Through Processing (STP):** Simulates institutional "automated triage." The engine automatically filters guaranteed approvals and obvious rejections, routing complex edge cases (Undetermined Risk) to human Risk Analysts.
* **Regulatory Audit Trails:** The `CreditPersistence` layer logging data into an SQLite database with timestamped CSVs reflects the strict compliance reporting required by commercial banks to justify lending decisions.

---

## 🚀 Future Roadmap
The layered architecture allows for scalable future integrations:
* **Machine Learning Migration:** Replacing hard-coded threshold voting with predictive models (e.g., Logistic Regression) to estimate precise Probability of Default (PD).
* **Macroeconomic Stress Testing:** Integrating external variables (e.g., inflation rates, central bank interest rates) into the Math Layer to dynamically adjust lending thresholds.
* **Live API Integration:** Transitioning from static `.csv` ingestion to pulling live borrower credit data via financial APIs.

--- 



## Installation

```bash
git clone https://github.com/somanjansahaweb/IRON-BANK-CREDIT-RISK-ASSESSMENT.git
cd IRON-BANK-CREDIT-RISK-ASSESSMENT
pip install pandas matplotlib
python Banking\ Program.py
```


## 📁 Project Structure
```text
iron-bank-risk-engine/
│
├── iron_bank.py                   # Main application script (6-Layer Architecture)
├── loanset.csv                    # Raw borrower input dataset
├── credit_risk_assessment.db      # SQLite database for bulk evaluations
├── CREDIT_RISK_ASSESSMENT_*.csv   # Time-stamped output logs
└── README.md                      # Project documentation




