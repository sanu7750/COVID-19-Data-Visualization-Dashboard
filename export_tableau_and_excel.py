"""
Export Module: Tableau-Ready Datasets & Executive Multi-Sheet Excel Workbook
Produces:
1. Specially formatted CSV datasets optimized for direct import into Tableau Desktop / Tableau Public.
2. An executive-grade multi-sheet Excel report styled with professional corporate themes via openpyxl.
"""

import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
TABLEAU_DIR = os.path.join(BASE_DIR, "data", "tableau_ready")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
os.makedirs(TABLEAU_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


def export_tableau_datasets():
    print("=" * 65)
    print(" [Tableau Export] Preparing Tableau-Optimized Datasets")
    print("=" * 65)

    country_summary_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_country_summary.csv")
    cleaned_ts_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_cleaned_timeseries.csv")
    global_summary_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_global_summary.csv")

    df_country = pd.read_csv(country_summary_path)
    df_ts = pd.read_csv(cleaned_ts_path)
    df_global = pd.read_csv(global_summary_path)

    # 1. Country Comparative Dataset (Tableau Map & Ranking Visuals)
    tableau_country = df_country.copy()
    tableau_country['Tableau_Geo_Role'] = 'Country/Region'
    tableau_country_path = os.path.join(TABLEAU_DIR, "tableau_country_comparative.csv")
    tableau_country.to_csv(tableau_country_path, index=False)
    print(f"[1/4] Saved Tableau Country Comparative Dataset: {tableau_country_path}")

    # 2. Daily Trends Timeseries (Tableau Dual-Axis & Wave Visuals)
    tableau_trends = df_ts[[
        'date', 'country', 'iso_code', 'continent',
        'daily_cases', 'daily_cases_7d_avg',
        'daily_deaths', 'daily_deaths_7d_avg',
        'daily_recovered', 'daily_recovered_7d_avg',
        'active_cases', 'cumulative_cases', 'cumulative_deaths', 'cumulative_recovered',
        'daily_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
        'predominant_variant', 'stringency_index'
    ]].copy()
    tableau_trends_path = os.path.join(TABLEAU_DIR, "tableau_daily_trends_timeseries.csv")
    tableau_trends.to_csv(tableau_trends_path, index=False)
    print(f"[2/4] Saved Tableau Daily Trends Timeseries: {tableau_trends_path}")

    # 3. Global Summary Daily (Tableau Worldwide Timeline)
    tableau_global_path = os.path.join(TABLEAU_DIR, "tableau_covid19_global_summary.csv")
    df_global.to_csv(tableau_global_path, index=False)
    print(f"[3/4] Saved Tableau Global Daily Summary: {tableau_global_path}")

    # 4. Vaccine Impact & Decoupling Dataset (Tableau Scatter & Correlation Visuals)
    tableau_vax = df_country[[
        'country', 'iso_code', 'continent', 'population',
        'cumulative_cases', 'cumulative_deaths', 'case_fatality_rate_pct',
        'cases_per_million', 'deaths_per_million',
        'fully_vaccinated_pct', 'vaccination_rate_pct', 'booster_rate_pct',
        'total_vaccinations'
    ]].copy()
    tableau_vax_path = os.path.join(TABLEAU_DIR, "tableau_vaccination_vs_mortality.csv")
    tableau_vax.to_csv(tableau_vax_path, index=False)
    print(f"[4/4] Saved Tableau Vaccine vs Mortality Dataset: {tableau_vax_path}")


def export_styled_excel_report():
    print("\n" + "=" * 65)
    print(" [Excel Export] Generating Executive Multi-Sheet Excel Workbook")
    print("=" * 65)

    country_summary_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_country_summary.csv")
    cleaned_ts_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_cleaned_timeseries.csv")
    df_country = pd.read_csv(country_summary_path)
    df_ts = pd.read_csv(cleaned_ts_path)
    df_ts['date'] = pd.to_datetime(df_ts['date'])

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styling Palettes
    navy_header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    accent_blue_fill = PatternFill(start_color="2E75B6", end_color="2E75B6", fill_type="solid")
    kpi_card_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    zebra_light = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    font_title = Font(name="Calibri", size=16, bold=True, color="1F4E79")
    font_subtitle = Font(name="Calibri", size=11, italic=True, color="595959")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_kpi_num = Font(name="Calibri", size=18, bold=True, color="1F4E79")
    font_kpi_lbl = Font(name="Calibri", size=10, bold=True, color="595959")
    font_regular = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)

    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # -------------------------------------------------------------
    # SHEET 1: Executive KPI Summary
    # -------------------------------------------------------------
    ws_exec = wb.create_sheet(title="Executive Summary")
    ws_exec.views.sheetView[0].showGridLines = True

    ws_exec["A1"] = "GLOBAL COVID-19 EXECUTIVE PERFORMANCE REPORT"
    ws_exec["A1"].font = font_title
    ws_exec["A2"] = "Comprehensive Epidemiological KPIs, Country Benchmarking & Vaccination Dynamics"
    ws_exec["A2"].font = font_subtitle

    total_cases = df_country['cumulative_cases'].sum()
    total_deaths = df_country['cumulative_deaths'].sum()
    total_recovered = df_country['cumulative_recovered'].sum()
    total_vax = df_country['total_vaccinations'].sum()
    global_cfr = (total_deaths / total_cases) * 100
    global_rec_rate = (total_recovered / total_cases) * 100

    kpis = [
        ("Total Confirmed Cases", f"{total_cases:,.0f}", "B4", "C5"),
        ("Total Fatalities", f"{total_deaths:,.0f}", "D4", "E5"),
        ("Estimated Recoveries", f"{total_recovered:,.0f}", "F4", "G5"),
        ("Total Doses Administered", f"{total_vax:,.0f}", "H4", "I5"),
        ("Global Case Fatality Rate", f"{global_cfr:.2f}%", "B7", "C8"),
        ("Global Recovery Rate", f"{global_rec_rate:.2f}%", "D7", "E8"),
    ]

    for title, val, top_left, bot_right in kpis:
        ws_exec.merge_cells(f"{top_left}:{bot_right}")
        cell = ws_exec[top_left]
        cell.value = f"{title}\n{val}"
        cell.fill = kpi_card_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.font = font_bold
        cell.border = border_thin

    # Continental Breakdown Table
    ws_exec["B11"] = "CONTINENTAL DISTRIBUTION BREAKDOWN"
    ws_exec["B11"].font = Font(name="Calibri", size=12, bold=True, color="1F4E79")

    cont_summary = df_country.groupby('continent').agg({
        'cumulative_cases': 'sum',
        'cumulative_deaths': 'sum',
        'cumulative_recovered': 'sum',
        'total_vaccinations': 'sum',
        'population': 'sum'
    }).reset_index()

    cont_summary['cfr_pct'] = (cont_summary['cumulative_deaths'] / cont_summary['cumulative_cases'] * 100).round(2)
    cont_summary['recovery_pct'] = (cont_summary['cumulative_recovered'] / cont_summary['cumulative_cases'] * 100).round(2)
    cont_summary['cases_per_million'] = (cont_summary['cumulative_cases'] / cont_summary['population'] * 1_000_000).round(0)

    cont_headers = ["Continent", "Confirmed Cases", "Fatalities", "Recoveries", "Total Doses", "CFR (%)", "Recovery (%)", "Cases / Million"]
    for col_idx, h in enumerate(cont_headers, start=2):
        cell = ws_exec.cell(row=13, column=col_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center")

    for r_idx, row in enumerate(cont_summary.to_dict('records'), start=14):
        ws_exec.cell(row=r_idx, column=2, value=row['continent'])
        ws_exec.cell(row=r_idx, column=3, value=row['cumulative_cases']).number_format = '#,##0'
        ws_exec.cell(row=r_idx, column=4, value=row['cumulative_deaths']).number_format = '#,##0'
        ws_exec.cell(row=r_idx, column=5, value=row['cumulative_recovered']).number_format = '#,##0'
        ws_exec.cell(row=r_idx, column=6, value=row['total_vaccinations']).number_format = '#,##0'
        ws_exec.cell(row=r_idx, column=7, value=row['cfr_pct']).number_format = '0.00"%"'
        ws_exec.cell(row=r_idx, column=8, value=row['recovery_pct']).number_format = '0.00"%"'
        ws_exec.cell(row=r_idx, column=9, value=row['cases_per_million']).number_format = '#,##0'

        for c_idx in range(2, 10):
            cell = ws_exec.cell(row=r_idx, column=c_idx)
            cell.font = font_regular
            cell.border = border_thin
            if r_idx % 2 == 1:
                cell.fill = zebra_light

    # -------------------------------------------------------------
    # SHEET 2: Country Comparative Rankings
    # -------------------------------------------------------------
    ws_rank = wb.create_sheet(title="Country Rankings")
    ws_rank.views.sheetView[0].showGridLines = True

    rank_headers = [
        "Rank", "Country", "ISO Code", "Continent", "Population",
        "Cumulative Cases", "Cumulative Deaths", "Estimated Recoveries", "Active Cases",
        "CFR (%)", "Recovery Rate (%)", "Cases/Million", "Deaths/Million",
        "Doses Administered", "Fully Vaccinated (%)"
    ]

    for col_idx, h in enumerate(rank_headers, start=1):
        cell = ws_rank.cell(row=1, column=col_idx, value=h)
        cell.fill = navy_header_fill
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center")

    sorted_df = df_country.sort_values('cumulative_cases', ascending=False)
    for r_idx, row in enumerate(sorted_df.itertuples(), start=2):
        ws_rank.cell(row=r_idx, column=1, value=r_idx-1)
        ws_rank.cell(row=r_idx, column=2, value=row.country)
        ws_rank.cell(row=r_idx, column=3, value=row.iso_code)
        ws_rank.cell(row=r_idx, column=4, value=row.continent)
        ws_rank.cell(row=r_idx, column=5, value=row.population).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=6, value=row.cumulative_cases).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=7, value=row.cumulative_deaths).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=8, value=row.cumulative_recovered).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=9, value=row.active_cases).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=10, value=row.case_fatality_rate_pct).number_format = '0.00"%"'
        ws_rank.cell(row=r_idx, column=11, value=row.recovery_rate_pct).number_format = '0.00"%"'
        ws_rank.cell(row=r_idx, column=12, value=row.cases_per_million).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=13, value=row.deaths_per_million).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=14, value=row.total_vaccinations).number_format = '#,##0'
        ws_rank.cell(row=r_idx, column=15, value=row.fully_vaccinated_pct).number_format = '0.0"%"'

        for c_idx in range(1, 16):
            cell = ws_rank.cell(row=r_idx, column=c_idx)
            cell.font = font_regular
            cell.border = border_thin
            if r_idx % 2 == 1:
                cell.fill = zebra_light

    # Auto-adjust column widths
    for ws in [ws_exec, ws_rank]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if '\n' in val_str:
                    val_str = max(val_str.split('\n'), key=len)
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    excel_file = os.path.join(REPORTS_DIR, "COVID19_Global_Executive_Report.xlsx")
    wb.save(excel_file)
    print(f"[Done] Executive Excel Report generated: {excel_file}")
    return excel_file


if __name__ == "__main__":
    export_tableau_datasets()
    export_styled_excel_report()
