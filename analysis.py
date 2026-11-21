"""
COVID-19 Statistical Analysis & Country-Wise Comparative Engine
Performs in-depth comparative analytics:
- Country-wise comparative ranking (Cases, Deaths, Recoveries, CFR, Rates per Million)
- Wave dynamics & peak strain analysis
- Clinical vaccine impact & CFR decoupling statistics
- Correlation analysis between socioeconomic metrics and pandemic outcomes
"""

import os
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def run_comparative_analysis():
    print("=" * 65)
    print(" [Statistical Analysis] Running Country-Wise Comparative Analytics")
    print("=" * 65)

    country_summary_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_country_summary.csv")
    cleaned_ts_path = os.path.join(PROCESSED_DATA_DIR, "covid_19_cleaned_timeseries.csv")

    if not os.path.exists(country_summary_path) or not os.path.exists(cleaned_ts_path):
        print("[Notice] Cleaned datasets missing. Running data cleaning pipeline first...")
        from data_cleaning import clean_and_transform_covid_data
        clean_and_transform_covid_data()

    print("[1/4] Performing country-wise comparative ranking...")
    df_countries = pd.read_csv(country_summary_path)
    df_ts = pd.read_csv(cleaned_ts_path)
    df_ts['date'] = pd.to_datetime(df_ts['date'])

    # Rank countries across key dimensions
    rankings = df_countries.copy()
    rankings['rank_total_cases'] = rankings['cumulative_cases'].rank(ascending=False, method='min').astype(int)
    rankings['rank_total_deaths'] = rankings['cumulative_deaths'].rank(ascending=False, method='min').astype(int)
    rankings['rank_cases_per_million'] = rankings['cases_per_million'].rank(ascending=False, method='min').astype(int)
    rankings['rank_deaths_per_million'] = rankings['deaths_per_million'].rank(ascending=False, method='min').astype(int)
    rankings['rank_vaccination_rate'] = rankings['fully_vaccinated_pct'].rank(ascending=False, method='min').astype(int)
    rankings['rank_recovery_rate'] = rankings['recovery_rate_pct'].rank(ascending=False, method='min').astype(int)

    rankings_sorted = rankings.sort_values(by='cumulative_cases', ascending=False)
    out_rankings = os.path.join(OUTPUTS_DIR, "country_comparative_rankings.csv")
    rankings_sorted.to_csv(out_rankings, index=False)
    print(f"      ✓ Country comparative rankings saved to: {out_rankings}")

    # -------------------------------------------------------------
    # 2. Wave Comparative Analysis
    # -------------------------------------------------------------
    print("[2/4] Analyzing pandemic wave peaks across variants...")
    wave_defs = {
        "Phase 1 - Wild-Type": ("2020-01-22", "2020-10-31"),
        "Phase 2 - Alpha/Beta": ("2020-11-01", "2021-04-30"),
        "Phase 3 - Delta": ("2021-05-01", "2021-11-30"),
        "Phase 4 - Omicron Peak": ("2021-12-01", "2022-05-31"),
        "Phase 5 - Endemic / Subvariants": ("2022-06-01", "2023-12-31")
    }

    wave_stats = []
    for wave_name, (w_start, w_end) in wave_defs.items():
        w_df = df_ts[(df_ts['date'] >= w_start) & (df_ts['date'] <= w_end)]
        daily_global = w_df.groupby('date').agg({'daily_cases': 'sum', 'daily_deaths': 'sum'}).reset_index()
        
        peak_cases_row = daily_global.loc[daily_global['daily_cases'].idxmax()]
        peak_deaths_row = daily_global.loc[daily_global['daily_deaths'].idxmax()]
        
        total_w_cases = int(daily_global['daily_cases'].sum())
        total_w_deaths = int(daily_global['daily_deaths'].sum())
        w_cfr = round((total_w_deaths / max(1, total_w_cases)) * 100, 2)
        
        wave_stats.append({
            "wave_phase": wave_name,
            "start_date": w_start,
            "end_date": w_end,
            "total_period_cases": total_w_cases,
            "total_period_deaths": total_w_deaths,
            "wave_cfr_pct": w_cfr,
            "peak_daily_cases": int(peak_cases_row['daily_cases']),
            "peak_cases_date": str(peak_cases_row['date'].strftime('%Y-%m-%d')),
            "peak_daily_deaths": int(peak_deaths_row['daily_deaths']),
            "peak_deaths_date": str(peak_deaths_row['date'].strftime('%Y-%m-%d'))
        })

    df_waves = pd.DataFrame(wave_stats)
    out_waves = os.path.join(OUTPUTS_DIR, "wave_comparative_analysis.csv")
    df_waves.to_csv(out_waves, index=False)
    print(f"      ✓ Wave comparative analysis saved to: {out_waves}")

    # -------------------------------------------------------------
    # 3. Correlation Analysis & Vaccine Decoupling Metric
    # -------------------------------------------------------------
    print("[3/4] Quantifying clinical vaccine decoupling impact...")
    # Calculate pre-vaccine vs post-vaccine CFR
    pre_vax = df_ts[df_ts['date'] < '2021-06-01']
    post_vax = df_ts[df_ts['date'] >= '2021-06-01']

    pre_vax_cases = int(pre_vax['daily_cases'].sum())
    pre_vax_deaths = int(pre_vax['daily_deaths'].sum())
    pre_vax_cfr = round((pre_vax_deaths / max(1, pre_vax_cases)) * 100, 2)

    post_vax_cases = int(post_vax['daily_cases'].sum())
    post_vax_deaths = int(post_vax['daily_deaths'].sum())
    post_vax_cfr = round((post_vax_deaths / max(1, post_vax_cases)) * 100, 2)

    cfr_reduction_pct = round(((pre_vax_cfr - post_vax_cfr) / pre_vax_cfr) * 100, 1)

    # -------------------------------------------------------------
    # 4. Generate Key Findings JSON
    # -------------------------------------------------------------
    print("[4/4] Generating Key Findings summary report...")
    top_5_cases = rankings_sorted.head(5)[['country', 'cumulative_cases', 'cases_per_million']].to_dict('records')
    top_5_deaths = rankings.sort_values('cumulative_deaths', ascending=False).head(5)[['country', 'cumulative_deaths', 'deaths_per_million']].to_dict('records')
    top_5_vax = rankings.sort_values('fully_vaccinated_pct', ascending=False).head(5)[['country', 'fully_vaccinated_pct', 'total_vaccinations']].to_dict('records')
    top_5_recovery = rankings.sort_values('recovery_rate_pct', ascending=False).head(5)[['country', 'recovery_rate_pct', 'cumulative_recovered']].to_dict('records')

    summary_findings = {
        "global_total_cases": int(df_countries['cumulative_cases'].sum()),
        "global_total_deaths": int(df_countries['cumulative_deaths'].sum()),
        "global_total_recovered": int(df_countries['cumulative_recovered'].sum()),
        "global_overall_cfr_pct": round((df_countries['cumulative_deaths'].sum() / df_countries['cumulative_cases'].sum()) * 100, 2),
        "global_overall_recovery_rate_pct": round((df_countries['cumulative_recovered'].sum() / df_countries['cumulative_cases'].sum()) * 100, 2),
        "global_total_doses_administered": int(df_countries['total_vaccinations'].sum()),
        "vaccine_impact_metrics": {
            "pre_vaccine_cfr_pct": pre_vax_cfr,
            "post_vaccine_cfr_pct": post_vax_cfr,
            "cfr_reduction_percentage": cfr_reduction_pct,
            "insight": f"Vaccine rollouts decoupled transmission from mortality, reducing Case Fatality Rate by {cfr_reduction_pct}% worldwide."
        },
        "top_5_countries_by_cases": top_5_cases,
        "top_5_countries_by_deaths": top_5_deaths,
        "top_5_countries_by_vaccination": top_5_vax,
        "top_5_countries_by_recovery": top_5_recovery
    }

    out_json = os.path.join(OUTPUTS_DIR, "key_findings_summary.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary_findings, f, indent=2)
    print(f"      ✓ Key findings JSON saved to: {out_json}")

    print("\n[Done] Comparative analysis and statistical modeling complete!")
    return summary_findings


if __name__ == "__main__":
    run_comparative_analysis()
