"""
================================================================================
    IRON BANK — AUTOMATED CREDIT RISK ASSESSMENT SYSTEM
    Version: 3.2 (Production Safe - IDE Ready)
================================================================================
    Architecture:
        Layer 1 — Borrower          : Data storage and profile summary
        Layer 2 — RiskEngine        : DSCR, DTI calculation and risk classification
        Layer 3 — CreditPersistence : Bulk CSV and SQLite persistence
        Layer 4 — CreditDecision    : Formal loan decision from risk verdict
        Layer 5 — GenerateCreditMemo: Terminal credit report output
        Layer 6 — Visualisation     : Portfolio analysis charts (Matplotlib)

    Author : Somanjan Saha
    Degree : B.Sc. Economics Honours, Calcutta University (2025-2029)
    Target : Credit Risk Analyst — HSBC Kolkata | Risk Advisory — Big 4
================================================================================
"""

# --- IMPORTS ---
from datetime import datetime
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# ==============================================================================
# LAYER 1 — BORROWER (Data Layer)
# ==============================================================================

class Borrower:
    """
    Layer 1 - Data Layer
    Stores all applicant information collected during the loan application process.
    Acts as the single source of truth for borrower attributes throughout the system.
    """

    def __init__(self, business_name, cash_flow, monthly_income, credit_score,
                 interest_rate, loan_amount, loan_term_years):

        if not (300 <= credit_score <= 850):
            raise ValueError("Credit score must be between 300 and 850.")

        self.business_name = business_name
        self.cash_flow = cash_flow
        self.monthly_income = monthly_income
        self.credit_score = credit_score
        self.interest_rate = interest_rate
        self.loan_amount = loan_amount
        self.loan_term_years = loan_term_years

    def get_profile_summary(self):
        """Prints a formatted summary of the borrower's profile."""

        print(f"--- Borrower Profile : {self.business_name} ---")
        print(f"--- Cash Flow        : ${self.cash_flow:.2f} ---")
        print(f"--- Monthly Income   : ${self.monthly_income:.2f} ---")
        print(f"--- Credit Score     : {self.credit_score} ---")
        print(f"--- Interest Rate    : {self.interest_rate * 100:.2f}% ---")
        print(f"--- Loan Amount      : ${self.loan_amount:.2f} ---")
        print(f"--- Loan Term (Yrs)  : {self.loan_term_years} ---")


# ==============================================================================
# LAYER 2 — RISK ENGINE (Math Layer)
# ==============================================================================

class RiskEngine:
    """
    Layer 2 - Math Engine
    Performs all financial ratio calculations (DSCR, DTI) on a Borrower object.
    Produces a risk verdict based on industry-standard thresholds.
    Does not store data or make final decisions — only calculates and classifies.
    """

    def __init__(self, borrower_data):
        self.borrower_data = borrower_data

    def calculate_monthly_payment(self):
        """Calculates monthly EMI payment for the loan using standard amortization formula."""

        p = self.borrower_data.loan_amount
        r = self.borrower_data.interest_rate / 12
        n = self.borrower_data.loan_term_years * 12

        if p <= 0:
            raise ValueError("Loan amount must be greater than zero.")

        if n <= 0:
            raise ValueError("Loan term must be greater than zero.")

        if r == 0:
            return p / n

        emi = ((p * r) * (1 + r) ** n) / (((1 + r) ** n) - 1)

        return emi

    def calculate_dti(self):
        """Calculates Debt To Income Ratio: Monthly Payment / Monthly Income"""

        if self.borrower_data.monthly_income <= 0:
            raise ValueError("Monthly income must be greater than zero.")

        return self.calculate_monthly_payment() / self.borrower_data.monthly_income

    def calculate_dscr(self):
        """Calculates Debt Service Coverage Ratio: Cash Flow / Monthly Payment"""

        monthly_payment = self.calculate_monthly_payment()

        if monthly_payment <= 0:
            raise ValueError("Monthly payment must be greater than zero.")

        return self.borrower_data.cash_flow / monthly_payment

    def get_dti_signal(self):
        """Returns Low / Medium / High signal based on DTI threshold."""

        dti = self.calculate_dti()

        if dti < 0.36:
            return "LOW RISK"
        elif dti <= 0.45:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    def get_dscr_signal(self):
        """Returns Low / Medium / High signal based on DSCR threshold."""

        dscr = self.calculate_dscr()

        if dscr > 1.25:
            return "LOW RISK"
        elif dscr >= 1.15:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    def get_score_signal(self):
        """Returns Low / Medium / High signal based on Credit Score threshold."""

        score = self.borrower_data.credit_score

        if score >= 700:
            return "LOW RISK"
        elif score >= 620:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    def get_overall_risk_verdict(self):
        """
        Majority voting across three signals.
        2 or more signals must agree for a verdict.
        All three different = UNDETERMINED RISK.
        """

        signals = [
            self.get_dti_signal(),
            self.get_dscr_signal(),
            self.get_score_signal()
        ]

        if signals.count("HIGH RISK") >= 2:
            return "HIGH RISK"
        elif signals.count("MEDIUM RISK") >= 2:
            return "MEDIUM RISK"
        elif signals.count("LOW RISK") >= 2:
            return "LOW RISK"
        else:
            return "UNDETERMINED RISK"


# ==============================================================================
# LAYER 3 — CREDIT PERSISTENCE (Persistence Layer)
# ==============================================================================

class CreditPersistence:
    """
    Layer 3 - Persistence Layer
    Saves bulk evaluated borrower records to CSV and SQLite database.
    """

    @staticmethod
    def save_batch(df):
        """Saves bulk evaluated borrower records to CSV and SQLite database."""

        # --- CSV SAVE ---
        try:
            datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CREDIT_RISK_ASSESSMENT_{datetime_str}.csv"
            df.to_csv(filename, index=False)
            print(f"[LOG] Batch saved to {filename}")

        except PermissionError:
            print("[ERROR] Permission denied: Unable to save CSV. Check if file is open.")
        except OSError:
            print("[ERROR] OS error: Unable to save CSV. Check disk space and file path.")
        except Exception as e:
            print(f"[ERROR] Failed to save CSV: {e}")

        # --- SQLITE SAVE ---
        try:
            # Using Context Manager (with statement) ensures connection auto-closes
            with sqlite3.connect("credit_risk_assessment.db") as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS borrowers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        business_name TEXT NOT NULL,
                        monthly_income REAL NOT NULL,
                        cash_flow REAL DEFAULT 0,
                        credit_score INTEGER NOT NULL,
                        interest_rate REAL NOT NULL,
                        loan_amount REAL NOT NULL,
                        loan_term_years INTEGER NOT NULL,
                        risk_verdict TEXT,
                        evaluated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                df.to_sql(
                    "borrowers",
                    conn,
                    if_exists="append",
                    index=False
                )

            print("[LOG] Batch saved to SQLite database successfully.")

        except sqlite3.Error as e:
            print(f"[ERROR] SQLite error: {e}")
        except Exception as e:
            print(f"[ERROR] Failed to save to SQLite: {e}")


# ==============================================================================
# LAYER 4 — CREDIT DECISION (Decision Layer)
# ==============================================================================

class CreditDecision:
    """
    Layer 4 - Decision Layer
    Translates the RiskEngine verdict into a clear, actionable loan decision.
    Exists so that any non-technical stakeholder can read the final outcome directly.
    """

    def __init__(self, risk_verdict):
        self.risk_verdict = risk_verdict

    def make_decision(self):
        """Converts risk verdict into a formal Loan Decision."""

        if self.risk_verdict == "LOW RISK":
            return "ACCEPT"
        elif self.risk_verdict == "MEDIUM RISK":
            return "ACCEPT WITH FURTHER REVIEW"
        elif self.risk_verdict == "HIGH RISK":
            return "REJECT"
        elif self.risk_verdict == "UNDETERMINED RISK":
            return "REQUIRES MANUAL REVIEW"
        else:
            return "INVALID RISK VERDICT"


# ==============================================================================
# LAYER 5 — GENERATE CREDIT MEMO (Report Layer)
# ==============================================================================

class GenerateCreditMemo:
    """
    Layer 5 - Report Layer
    Prints a formatted terminal credit report for each borrower.
    Combines profile summary, risk verdict, and final decision.
    """

    def __init__(self, borrower, risk_verdict, loan_decision):
        self.borrower = borrower
        self.risk_verdict = risk_verdict
        self.loan_decision = loan_decision

    def print_report(self):
        """Prints a formatted credit report to the terminal."""

        print("\n" + "=" * 45)
        print("        IRON BANK — CREDIT REPORT")
        print("=" * 45)
        self.borrower.get_profile_summary()
        print(f"--- Risk Verdict     : {self.risk_verdict} ---")
        print(f"--- Loan Decision    : {self.loan_decision} ---")
        print("=" * 45 + "\n")


# ==============================================================================
# LAYER 6 — VISUALISATION (Chart Layer)
# ==============================================================================

def generate_charts(df, datetime_str):
    """
    Generates a three-panel portfolio analysis chart and saves as PNG.
    Panel 1 — Risk Verdict Distribution (Bar Chart)
    Panel 2 — Credit Score Distribution (Histogram)
    Panel 3 — DTI vs DSCR by Risk Tier (Scatter Plot)
    """

    try:
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle("IRON BANK — PORTFOLIO ANALYSIS", fontsize=14, fontweight='bold')

        colors = {
            "LOW RISK"         : "#2ecc71",
            "MEDIUM RISK"      : "#f39c12",
            "HIGH RISK"        : "#e74c3c",
            "UNDETERMINED RISK": "#95a5a6",
            "VALIDATION ERROR" : "#9b59b6",
            "SYSTEM ERROR"     : "#1abc9c"
        }

        # --- PANEL 1: RISK VERDICT DISTRIBUTION ---
        counts = df["risk_verdict"].value_counts()
        bar_colors = [colors.get(v, "#95a5a6") for v in counts.index]

        axes[0].bar(counts.index, counts.values, color=bar_colors, edgecolor='black', linewidth=0.5)
        axes[0].set_title("Risk Verdict Distribution", fontsize=11)
        axes[0].set_xlabel("Risk Verdict")
        axes[0].set_ylabel("Number of Borrowers")
        axes[0].tick_params(axis='x', rotation=15)

        for i, (verdict, count) in enumerate(counts.items()):
            axes[0].text(i, count + (counts.max() * 0.01), f"{count:,}", ha='center', fontsize=8)

        # --- PANEL 2: CREDIT SCORE DISTRIBUTION ---
        axes[1].hist(
            df["credit_score"].dropna(),
            bins=30,
            color="#3498db",
            edgecolor='black',
            linewidth=0.5
        )
        axes[1].set_title("Credit Score Distribution", fontsize=11)
        axes[1].set_xlabel("Credit Score")
        axes[1].set_ylabel("Number of Borrowers")
        axes[1].axvline(x=620, color='red', linestyle='--', linewidth=1, label='620 threshold')
        axes[1].axvline(x=700, color='green', linestyle='--', linewidth=1, label='700 threshold')
        axes[1].legend(fontsize=8)

        # --- PANEL 3: DTI vs DSCR SCATTER ---
        scatter_colors = df["risk_verdict"].map(colors).fillna("#95a5a6")

        axes[2].scatter(
            df["dti"],
            df["dscr"],
            c=scatter_colors,
            alpha=0.3,
            s=5
        )
        axes[2].set_title("DTI vs DSCR by Risk Tier", fontsize=11)
        axes[2].set_xlabel("DTI (Debt-to-Income Ratio)")
        axes[2].set_ylabel("DSCR (Debt Service Coverage Ratio)")
        axes[2].axvline(x=0.36, color='orange', linestyle='--', linewidth=1, label='DTI 36%')
        axes[2].axhline(y=1.25, color='green', linestyle='--', linewidth=1, label='DSCR 1.25')
        axes[2].legend(fontsize=8)

        plt.tight_layout()

        filename = f"IRON_BANK_CHARTS_{datetime_str}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"[LOG] Charts saved to {filename}")

    except Exception as e:
        print(f"[ERROR] Failed to generate charts: {e}")


# ==============================================================================
# BULK PROCESSING — WORKER FUNCTION
# ==============================================================================

def evaluate_borrower_row(row):
    """
    Worker function for the Pandas assembly line.
    Takes one DataFrame row, creates a Borrower object,
    runs RiskEngine, and returns the risk verdict, DTI, and DSCR simultaneously.
    """
    try:
        borrower = Borrower(
            business_name=row["business_name"],
            cash_flow=row["cash_flow"],
            monthly_income=row["monthly_income"],
            credit_score=row["credit_score"],
            interest_rate=row["interest_rate"],
            loan_amount=row["loan_amount"],
            loan_term_years=row["loan_term_years"]
        )

        engine = RiskEngine(borrower)
        
        return pd.Series({
            "risk_verdict": engine.get_overall_risk_verdict(),
            "dti": engine.calculate_dti(),
            "dscr": engine.calculate_dscr()
        })

    except ValueError as e:
        print(f"[VALIDATION ERROR] {row['business_name']}: {e}")
        return pd.Series({"risk_verdict": "VALIDATION ERROR", "dti": None, "dscr": None})

    except Exception as e:
        print(f"[SYSTEM ERROR] {row['business_name']}: {e}")
        return pd.Series({"risk_verdict": "SYSTEM ERROR", "dti": None, "dscr": None})


# ==============================================================================
# ENTRY POINT — BULK EVALUATION
# ==============================================================================

def main():

    try:
        # --- LOAD BORROWER DATA ---
        datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Hardcoded file path
        filepath = r"C:\Users\USER\Downloads\loanset.csv"
        df = pd.read_csv(filepath)

        print(f"[LOG] Dataset loaded from '{filepath}': {len(df):,} borrowers found")

        # --- DATA CLEANING ---
        numeric_cols = [
            "monthly_income",
            "cash_flow",
            "credit_score",
            "interest_rate",
            "loan_amount",
            "loan_term_years"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # --- HANDLE MISSING VALUES ---
        df.dropna(
            subset=["credit_score", "monthly_income", "interest_rate", "loan_amount", "loan_term_years"],
            inplace=True
        )

        df["cash_flow"] = df["cash_flow"].fillna(0)

        print(f"[LOG] Clean records after validation: {len(df):,}")

        # --- BULK RISK EVALUATION & METRIC CALCULATION ---
        print("[LOG] Running bulk evaluation (Optimized)...")
        # Apply the optimized worker function that calculates everything in one pass
        df[["risk_verdict", "dti", "dscr"]] = df.apply(evaluate_borrower_row, axis=1)

        # --- GENERATE CHARTS ---
        print("[LOG] Generating portfolio charts...")
        generate_charts(df, datetime_str)

        # --- SAVE RESULTS --- 
        df_to_save = df.drop(columns=["dti", "dscr"])
        CreditPersistence.save_batch(df_to_save)
        
        # --- ANALYST SUMMARY REPORT ---
        print("\n" + "=" * 45)
        print("        IRON BANK — ANALYST REPORT")
        print("=" * 45)
        print(f"Total Borrowers Evaluated : {len(df):,}")
        print("-" * 45)

        counts = df["risk_verdict"].value_counts()
        percentages = df["risk_verdict"].value_counts(normalize=True) * 100

        for verdict in counts.index:
            print(f"{verdict:<25}: {counts[verdict]:>6,}  ({percentages[verdict]:.1f}%)")

        print("=" * 45 + "\n")

    except FileNotFoundError:
        print(f"[FATAL ERROR] Dataset file '{filepath}' not found. Check the file path.")

    except pd.errors.EmptyDataError:
        print("[FATAL ERROR] Dataset file is empty.")

    except KeyError as e:
        print(f"[FATAL ERROR] Missing column in dataset: {e}")

    except Exception as e:
        print(f"[FATAL ERROR] Unexpected error: {e}")


# ==============================================================================
# PROGRAM ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    main()
