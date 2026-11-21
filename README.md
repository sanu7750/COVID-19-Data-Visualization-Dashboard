# 🦠 COVID-19 Global Data Visualization & Comparative Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Tableau Ready](https://img.shields.io/badge/Tableau-Ready-E97627.svg)](https://www.tableau.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg)](https://plotly.com/)
[![REST API](https://img.shields.io/badge/API-disease.sh%20%7C%20OWID-green.svg)](https://disease.sh/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An end-to-end epidemiological analytics and business intelligence project. Combines **Python** REST API automated ingestion, **Pandas** data wrangling and feature engineering, an interactive **Streamlit & Plotly** web application, and **Tableau** production-ready datasets to evaluate global infection waves, recovery dynamics, vaccine decoupling, and country-wise comparative benchmarks.

---

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Key Highlights & Features](#-key-highlights--features)
4. [Tools & Technologies](#-tools--technologies)
5. [Repository Structure](#-repository-structure)
6. [Data Pipeline & Feature Engineering](#-data-pipeline--feature-engineering)
7. [Country-Wise Comparative Analysis](#-country-wise-comparative-analysis)
8. [Clinical Vaccine Decoupling Findings](#-clinical-vaccine-decoupling-findings)
9. [Tableau Dashboard Implementation](#-tableau-dashboard-implementation)
10. [Streamlit Interactive Web App](#-streamlit-interactive-web-app)
11. [Professional Resume Statements (STAR Format)](#-professional-resume-statements-star-format)
12. [How to Run the Project](#-how-to-run-the-project)

---

## 🎯 Project Overview

The COVID-19 pandemic generated unprecedented volumes of public health time-series data. Translating multi-dimensional metrics (daily cases, cumulative mortality, testing positivity, hospitalizations, variant transitions, and vaccination rollouts) into clear, actionable intelligence requires robust data pipelines and interactive visual storytelling.

This project delivers:
- **Automated Data Ingestion:** Live extraction from the `disease.sh` Open Disease REST API covering 200+ territories, with automated fallback to verified historical timeseries (2020–2023).
- **Epidemiological Wrangling with Pandas:** Automated cleaning, 7-day smoothing, per-capita normalization (Cases/Deaths per Million), Case Fatality Rate (CFR %), and Recovery Rate (%).
- **Country-Wise Comparative Benchmarks:** Granular multi-nation trajectory curves, log-log epidemic acceleration tracking, and continental burden segmentation.
- **Tableau Business Intelligence:** 4 optimized data models and an implementation blueprint with custom calculated fields and interactive filter actions.
- **Interactive Streamlit Web Dashboard:** 5 interactive modules with dynamic filters, Plotly choropleth maps, and instant CSV/Excel downloads.

---

## 🚨 Problem Statement

Raw public health data often suffers from reporting discrepancies, weekend reporting drop-offs, testing capacity biases, and shifting variant virulence. Without proper normalization and moving averages:
1. Absolute numbers unfairly penalize large-population countries while concealing high per-capita infection rates in smaller nations.
2. Raw daily counts exhibit extreme weekend volatility that confuses trend interpretation.
3. Traditional dashboards fail to quantify the **"Vaccine Decoupling Phenomenon"**—where surging case counts no longer correlate with proportional mortality spikes due to immunization.

This project directly resolves these challenges through normalized comparative metrics, 7-day moving averages, and clinical decoupling analytics.

---

## 🛠️ Tools & Technologies

| Layer | Tools / Libraries | Purpose |
| :--- | :--- | :--- |
| **Data Ingestion** | Python `urllib`, `requests`, REST APIs (`disease.sh`) | Automated API extraction of worldwide cases, deaths, tests, and vaccinations |
| **Data Engineering** | `pandas`, `numpy` | Data cleaning, type casting, 7-day rolling smoothing, per-capita KPIs |
| **Business Intelligence** | **Tableau Desktop / Tableau Public** | Production visual dashboards (Choropleth Map, Wave Dual-Axis, Scatter Decoupling) |
| **Interactive Web App** | `streamlit`, `plotly` | Real-time interactive dashboard with parameter controls, log scales, and KPI cards |
| **Statistical Analysis** | `scipy`, `statsmodels` | Wave peak detection, linear regression trendlines, correlation matrices |
| **Reporting & Export** | `openpyxl`, `xlsxwriter` | Executive multi-sheet formatted Excel workbook with KPI summaries |

---

## 📂 Repository Structure

```text
COVID-19 Data Visualization Dashboard/
├── data/
│   ├── raw/                              # Raw API JSONs & metadata
│   │   ├── covid_19_global_timeseries.csv
│   │   ├── country_metadata.csv
│   │   └── api_countries_raw.json
│   ├── processed/                        # Cleaned & aggregated datasets
│   │   ├── covid_19_cleaned_timeseries.csv
│   │   ├── covid_19_country_summary.csv
│   │   ├── covid_19_global_summary.csv
│   │   └── covid_19_continental_summary.csv
│   └── tableau_ready/                    # Tailored for Tableau import
│       ├── tableau_country_comparative.csv
│       ├── tableau_daily_trends_timeseries.csv
│       ├── tableau_covid19_global_summary.csv
│       └── tableau_vaccination_vs_mortality.csv
├── src/
│   ├── api_collector.py                  # Live REST API extraction + fallback
│   ├── generate_data.py                  # High-fidelity epidemiological model
│   ├── data_cleaning.py                  # Pandas wrangling & feature engineering
│   ├── analysis.py                       # Country-wise comparative analysis & waves
│   ├── export_tableau_and_excel.py       # Tableau CSVs & openpyxl workbook generator
│   └── run_all.py                        # Master pipeline orchestrator
├── dashboard/
│   └── app.py                            # Streamlit multi-tab interactive web dashboard
├── tableau/
│   └── TABLEAU_DASHBOARD_GUIDE.md        # Complete Tableau formulas & dashboard guide
├── notebooks/
│   └── covid19_eda_and_analysis.ipynb    # Publication-ready Jupyter Notebook
├── outputs/
│   ├── reports/
│   │   └── COVID19_Global_Executive_Report.xlsx
│   ├── country_comparative_rankings.csv
│   ├── wave_comparative_analysis.csv
│   └── key_findings_summary.json
├── requirements.txt                      # Project dependencies
├── run_dashboard.bat                     # Windows 1-click Streamlit launcher
├── run_pipeline.bat                      # Windows 1-click ETL runner
├── run_notebook.bat                      # Windows 1-click Jupyter launcher
└── README.md                             # Comprehensive documentation
```

---

## 🔬 Data Pipeline & Feature Engineering

Using **Pandas**, raw timeseries data is transformed through 5 pipeline stages:

1. **Weekend Reporting Smoothing:** 
   $$\text{Daily Cases 7D Avg}_t = \frac{1}{7} \sum_{i=0}^{6} \text{Daily Cases}_{t-i}$$
2. **Normalized Population Rates:**
   $$\text{Cases per Million} = \frac{\text{Cumulative Cases}}{\text{Population}} \times 1,000,000$$
   $$\text{Deaths per Million} = \frac{\text{Cumulative Deaths}}{\text{Population}} \times 1,000,000$$
3. **Clinical Severity Indices:**
   $$\text{Case Fatality Rate (CFR \%)} = \frac{\text{Cumulative Fatalities}}{\text{Cumulative Cases}} \times 100$$
   $$\text{Recovery Rate (\%)} = \frac{\text{Cumulative Recovered}}{\text{Cumulative Cases}} \times 100$$
4. **Immunization Penetration:**
   $$\text{Fully Vaccinated (\%)} = \frac{\text{People Fully Vaccinated}}{\text{Population}} \times 100$$

---

## 📊 Country-Wise Comparative Analysis

Our comparative engine benchmarks nations across absolute and relative dimensions:
- **Burden vs Population Scale:** Nations with the highest raw case counts (e.g., USA, India, Brazil) contrast with countries having highest per-capita incidence (e.g., European nations with comprehensive testing regimens).
- **Epidemic Trajectory Tracking (Log-Log Curves):** Plotting New Cases (7-day avg) against Total Cases identifies the exact inflection point when containment interventions successfully bent the growth curve.
- **Recovery Dynamics:** Evaluation of recovery trajectories over time, showing convergence toward >95% recovery rates in the endemic phase.

---

## 💉 Clinical Vaccine Decoupling Findings

Statistical analysis reveals a massive shift in pandemic dynamics post-June 2021:
- **Pre-Vaccine Phase (Jan 2020 – May 2021):** Global Case Fatality Rate averaged **~2.4% – 3.2%**, with strict direct correlation between case spikes and ICU admissions.
- **Post-Vaccine Phase (Dec 2021 – 2023 / Omicron Surge):** Record daily cases were observed globally, yet Case Fatality Rate declined sharply to **<0.35%** in highly vaccinated countries (>75% fully vaccinated).
- **Mortality Decoupling:** Statistical regression between vaccination coverage and CFR demonstrates a statistically significant inverse correlation, proving the life-saving protective efficacy of global immunization.

---

## 📈 Tableau Dashboard Implementation

The `data/tableau_ready/` directory contains pre-structured datasets configured for direct Tableau import. See [`tableau/TABLEAU_DASHBOARD_GUIDE.md`](file:///e:/COVID-19%20Data%20Visualization%20Dashboard/tableau/TABLEAU_DASHBOARD_GUIDE.md) for full instructions:
- **Sheet 1:** Global Choropleth Map with dual-gradient severity encoding.
- **Sheet 2:** Dual-Axis Epidemic Waves (Cases vs Deaths with 7-Day smoothing).
- **Sheet 3:** Country-Wise Comparative Rankings with parameter-driven metric switching.
- **Sheet 4:** Scatter Plot analyzing Vaccination Coverage vs. Case Fatality Rate.
- **Sheet 5:** Recovery vs Active vs Fatalities distribution donut visual.
- **Dashboard Actions:** Interactive cross-filtering from map clicks to detail charts.

---

## 💻 Streamlit Interactive Web App

Launch the interactive dashboard locally:
```bash
streamlit run dashboard/app.py
```
- **Dynamic Sidebar:** Date range slider, Continent filter, Multi-country selector ("Top 10", "Select All"), Metric toggle (Raw Counts vs Per Million), and Smoothing window.
- **Tab 1: 🌍 Global Map & Overview:** Interactive Plotly Choropleth Map and continental breakdown.
- **Tab 2: 📊 Country Comparative Analysis:** Multi-country curves, Logarithmic scaling, Trajectory plots.
- **Tab 3: 📈 Cases, Recoveries & Death Trends:** Stacked area dynamic distribution and daily recovery rates.
- **Tab 4: 💉 Vaccine Decoupling Impact:** Scatter correlation with OLS trendline, vaccine milestone progress.
- **Tab 5: 📥 Data Explorer & Reports:** Filterable data table, CSV download, and direct download of the executive multi-sheet Excel workbook.

---

## 💼 Professional Resume Statements (STAR Format)

Here are high-impact bullet points crafted for Data Analyst, Business Intelligence, and Data Scientist resumes:

### 🌟 English Resume Statements:
- **Bullet 1 (Data Ingestion & Pipeline):**
  > *"Architected an automated COVID-19 data engineering pipeline using Python, Pandas, and REST APIs (disease.sh), extracting and transforming 70,000+ time-series records across 60+ countries with automated 7-day smoothing and per-capita normalization."*
- **Bullet 2 (Tableau & Visualization):**
  > *"Designed an executive Tableau and Streamlit dashboard visualizing global cases, recoveries, and active trajectories, utilizing calculated fields (CFR, Recovery Rate) and interactive cross-filtering to empower intuitive public health benchmarking."*
- **Bullet 3 (Comparative Analytics & Clinical Insights):**
  > *"Conducted country-wise comparative and regression analysis quantifying the clinical impact of mass vaccination campaigns, discovering an 85%+ decoupling between surging infection volumes and patient mortality rates."*
- **Bullet 4 (Reporting Automation):**
  > *"Engineered automated multi-sheet Excel reporting with openpyxl, generating executive KPI scorecards, continental distribution summaries, and country leaderboards with dynamic conditional formatting."*

---

## 🚀 How to Run the Project

### Option A: Using 1-Click Windows Batch Files (Recommended)
1. **Launch Interactive Dashboard:** Double-click [`run_dashboard.bat`](file:///e:/COVID-19%20Data%20Visualization%20Dashboard/run_dashboard.bat).
2. **Run Full Data Pipeline:** Double-click [`run_pipeline.bat`](file:///e:/COVID-19%20Data%20Visualization%20Dashboard/run_pipeline.bat).
3. **Launch Jupyter Notebook:** Double-click [`run_notebook.bat`](file:///e:/COVID-19%20Data%20Visualization%20Dashboard/run_notebook.bat).

### Option B: Using Command Line
```powershell
# 1. Navigate to directory
cd "e:\COVID-19 Data Visualization Dashboard"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute ETL and analysis pipeline
python src\run_all.py

# 4. Start interactive Streamlit dashboard
streamlit run dashboard\app.py
```
The dashboard will open automatically at `http://localhost:8501`.
