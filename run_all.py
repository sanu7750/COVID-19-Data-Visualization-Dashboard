"""
Master Pipeline Orchestration Script
Runs the complete COVID-19 Analytics ETL, Analysis, and Export workflow:
1. API Data Collection & Timeseries Compilation
2. Data Cleaning & Epidemiological Feature Engineering
3. Statistical Country-Wise Comparative Analysis
4. Export of Tableau-Ready Datasets & Executive Multi-Sheet Excel Workbook
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_collector import collect_covid_data
from data_cleaning import clean_and_transform_covid_data
from analysis import run_comparative_analysis
from export_tableau_and_excel import export_tableau_datasets, export_styled_excel_report


def run_full_pipeline():
    start_time = time.time()
    print("\n" + "=" * 70)
    print("      COVID-19 DATA VISUALIZATION & ANALYTICS PIPELINE")
    print("=" * 70)

    # Step 1: Data Collection / API
    print("\n>>> STAGE 1: API Collection & Data Extraction")
    collect_covid_data()

    # Step 2: Data Cleaning & Feature Engineering
    print("\n>>> STAGE 2: Data Cleaning & Feature Engineering")
    clean_and_transform_covid_data()

    # Step 3: Comparative Analysis & Insights
    print("\n>>> STAGE 3: Country-Wise Comparative Analysis")
    run_comparative_analysis()

    # Step 4: Tableau & Excel Export
    print("\n>>> STAGE 4: Tableau Datasets & Multi-Sheet Excel Workbook Export")
    export_tableau_datasets()
    export_styled_excel_report()

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f" [SUCCESS] Complete COVID-19 Pipeline Executed in {elapsed:.2f} seconds!")
    print("=" * 70)
    print("Outputs generated:")
    print("  - Tableau Datasets:  data/tableau_ready/")
    print("  - Executive Excel:    outputs/reports/COVID19_Global_Executive_Report.xlsx")
    print("  - Cleaned Datasets:   data/processed/")
    print("  - Statistical JSON:   outputs/key_findings_summary.json")
    print("\nTo launch the interactive web dashboard, run:")
    print("  streamlit run dashboard/app.py\n")


if __name__ == "__main__":
    run_full_pipeline()
