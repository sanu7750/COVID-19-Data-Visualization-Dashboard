"""
COVID-19 Data Cleaning & Feature Engineering Pipeline
Uses Pandas to clean, transform, validate, and compute vital epidemiological KPIs:
- 7-Day Moving Averages (Daily Cases, Deaths, Recoveries)
- Normalized Metrics (Cases/Deaths per Million, Tests per Thousand)
- Case Fatality Rate (CFR %) & Recovery Rate (%)
- Vaccination Coverage & Booster Rates
- Global and Continental Aggregations
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def clean_and_transform_covid_data():
    print("=" * 65)
    print(" [Data Cleaning & Transformation] Processing Raw COVID-19 Data")
    print("=" * 65)

    raw_ts_file = os.path.join(RAW_DATA_DIR, "covid_19_global_timeseries.csv")
    if not os.path.exists(raw_ts_file):
        print("[Warning] Raw timeseries not found. Generating fresh data...")
        from generate_data import generate_epidemic_curves
        generate_epidemic_curves()

    print("[1/5] Loading raw timeseries and metadata...")
    df = pd.read_csv(raw_ts_file)
    print(f"      Loaded {len(df):,} records across {df['country'].nunique()} countries.")

    # Convert datatypes
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['country', 'date']).reset_index(drop=True)

    # Impute missing values and enforce non-negative numbers
    numeric_cols = [
        'daily_cases', 'cumulative_cases', 'daily_deaths', 'cumulative_deaths',
        'active_cases', 'daily_tests', 'cumulative_tests', 'positivity_rate',
        'daily_vaccinations', 'total_vaccinations', 'people_vaccinated',
        'people_fully_vaccinated', 'total_boosters', 'hospital_patients',
        'icu_patients', 'stringency_index'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).clip(lower=0)

    # Derived daily recoveries & cumulative recoveries
    # Standard epidemiological recovery estimate: cumulative cases minus deaths minus active
    print("[2/5] Computing recovery rates and active cases dynamics...")
    df['cumulative_recovered'] = np.maximum(0, df['cumulative_cases'] - df['cumulative_deaths'] - df['active_cases'])
    # Daily recovered estimation from differential
    df['daily_recovered'] = df.groupby('country')['cumulative_recovered'].diff().fillna(0).clip(lower=0)

    # 7-Day Moving Averages per country (smoothing out weekend reporting noise)
    print("[3/5] Calculating 7-day and 14-day rolling moving averages...")
    df['daily_cases_7d_avg'] = df.groupby('country')['daily_cases'].transform(
        lambda s: s.rolling(window=7, min_periods=1).mean().round(1)
    )
    df['daily_deaths_7d_avg'] = df.groupby('country')['daily_deaths'].transform(
        lambda s: s.rolling(window=7, min_periods=1).mean().round(1)
    )
    df['daily_recovered_7d_avg'] = df.groupby('country')['daily_recovered'].transform(
        lambda s: s.rolling(window=7, min_periods=1).mean().round(1)
    )

    # Feature Engineering: Normalized Per-Capita and Ratio KPIs
    print("[4/5] Engineering normalized epidemiological KPIs...")
    df['cases_per_million'] = (df['cumulative_cases'] / df['population'] * 1_000_000).round(2)
    df['deaths_per_million'] = (df['cumulative_deaths'] / df['population'] * 1_000_000).round(2)
    df['tests_per_thousand'] = (df['cumulative_tests'] / df['population'] * 1_000).round(2)
    
    # Case Fatality Rate (CFR %)
    df['case_fatality_rate_pct'] = np.where(
        df['cumulative_cases'] > 0,
        ((df['cumulative_deaths'] / df['cumulative_cases']) * 100).round(2),
        0.0
    )
    
    # Recovery Rate (%)
    df['recovery_rate_pct'] = np.where(
        df['cumulative_cases'] > 0,
        ((df['cumulative_recovered'] / df['cumulative_cases']) * 100).round(2),
        0.0
    )

    # Vaccination percentages
    df['vaccination_rate_pct'] = ((df['people_vaccinated'] / df['population']) * 100).round(2).clip(upper=100.0)
    df['fully_vaccinated_pct'] = ((df['people_fully_vaccinated'] / df['population']) * 100).round(2).clip(upper=100.0)
    df['booster_rate_pct'] = ((df['total_boosters'] / df['population']) * 100).round(2).clip(upper=100.0)

    # Save cleaned master timeseries
    out_master = os.path.join(PROCESSED_DATA_DIR, "covid_19_cleaned_timeseries.csv")
    df.to_csv(out_master, index=False)
    print(f"      ✓ Cleaned timeseries saved to: {out_master}")

    # Generate Aggregations:
    # A) Country Latest Snapshot Summary
    print("[5/5] Generating aggregation tables...")
    latest_df = df.sort_values('date').groupby('country').last().reset_index()
    latest_df = latest_df[[
        'country', 'iso_code', 'continent', 'population',
        'cumulative_cases', 'cumulative_deaths', 'cumulative_recovered', 'active_cases',
        'cases_per_million', 'deaths_per_million', 'case_fatality_rate_pct', 'recovery_rate_pct',
        'cumulative_tests', 'tests_per_thousand', 'positivity_rate',
        'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'total_boosters',
        'vaccination_rate_pct', 'fully_vaccinated_pct', 'booster_rate_pct',
        'hospital_patients', 'icu_patients', 'stringency_index', 'predominant_variant'
    ]]
    out_country_summary = os.path.join(PROCESSED_DATA_DIR, "covid_19_country_summary.csv")
    latest_df.to_csv(out_country_summary, index=False)
    print(f"      ✓ Country latest summary saved to: {out_country_summary}")

    # B) Daily Global Aggregate
    global_daily = df.groupby('date').agg({
        'daily_cases': 'sum',
        'daily_deaths': 'sum',
        'daily_recovered': 'sum',
        'cumulative_cases': 'sum',
        'cumulative_deaths': 'sum',
        'cumulative_recovered': 'sum',
        'active_cases': 'sum',
        'daily_vaccinations': 'sum',
        'total_vaccinations': 'sum',
        'people_vaccinated': 'sum',
        'people_fully_vaccinated': 'sum',
        'total_boosters': 'sum',
        'hospital_patients': 'sum',
        'icu_patients': 'sum'
    }).reset_index()

    global_daily['daily_cases_7d_avg'] = global_daily['daily_cases'].rolling(window=7, min_periods=1).mean().round(1)
    global_daily['daily_deaths_7d_avg'] = global_daily['daily_deaths'].rolling(window=7, min_periods=1).mean().round(1)
    global_daily['daily_recovered_7d_avg'] = global_daily['daily_recovered'].rolling(window=7, min_periods=1).mean().round(1)
    global_daily['global_cfr_pct'] = ((global_daily['cumulative_deaths'] / global_daily['cumulative_cases']) * 100).round(2)
    global_daily['global_recovery_rate_pct'] = ((global_daily['cumulative_recovered'] / global_daily['cumulative_cases']) * 100).round(2)

    out_global = os.path.join(PROCESSED_DATA_DIR, "covid_19_global_summary.csv")
    global_daily.to_csv(out_global, index=False)
    print(f"      ✓ Global daily summary saved to: {out_global}")

    # C) Daily Continental Aggregate
    continent_daily = df.groupby(['date', 'continent']).agg({
        'daily_cases': 'sum',
        'daily_deaths': 'sum',
        'daily_recovered': 'sum',
        'cumulative_cases': 'sum',
        'cumulative_deaths': 'sum',
        'cumulative_recovered': 'sum',
        'active_cases': 'sum',
        'total_vaccinations': 'sum',
        'people_vaccinated': 'sum',
        'people_fully_vaccinated': 'sum'
    }).reset_index()
    out_cont = os.path.join(PROCESSED_DATA_DIR, "covid_19_continental_summary.csv")
    continent_daily.to_csv(out_cont, index=False)
    print(f"      ✓ Continental daily summary saved to: {out_cont}")

    print("\n[Done] All data cleaning & feature engineering completed successfully!")
    return df, latest_df, global_daily


if __name__ == "__main__":
    clean_and_transform_covid_data()
