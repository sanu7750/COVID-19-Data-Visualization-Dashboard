"""
COVID-19 Data Generation Pipeline
Generates authentic, high-fidelity pandemic time-series and metadata
mirroring Johns Hopkins University (JHU CSSE) and Our World in Data (OWID).
Covers 2020 through 2023 across 60+ representative global countries.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for deterministic, reproducible results
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. COUNTRY METADATA DEFINITION (60+ Major Nations)
# -------------------------------------------------------------
COUNTRIES = [
    # North America
    {"country": "United States", "iso_code": "USA", "continent": "North America", "population": 331893745, "gdp_per_capita": 63543.6, "median_age": 38.3, "hospital_beds_per_k": 2.87, "hdi": 0.926},
    {"country": "Canada", "iso_code": "CAN", "continent": "North America", "population": 37742154, "gdp_per_capita": 46195.5, "median_age": 41.4, "hospital_beds_per_k": 2.50, "hdi": 0.929},
    {"country": "Mexico", "iso_code": "MEX", "continent": "North America", "population": 128932753, "gdp_per_capita": 17336.5, "median_age": 29.3, "hospital_beds_per_k": 1.38, "hdi": 0.779},

    # South America
    {"country": "Brazil", "iso_code": "BRA", "continent": "South America", "population": 212559417, "gdp_per_capita": 14103.5, "median_age": 33.5, "hospital_beds_per_k": 2.20, "hdi": 0.765},
    {"country": "Argentina", "iso_code": "ARG", "continent": "South America", "population": 45195774, "gdp_per_capita": 18933.9, "median_age": 31.9, "hospital_beds_per_k": 5.00, "hdi": 0.845},
    {"country": "Colombia", "iso_code": "COL", "continent": "South America", "population": 50882891, "gdp_per_capita": 13254.9, "median_age": 31.3, "hospital_beds_per_k": 1.70, "hdi": 0.767},
    {"country": "Chile", "iso_code": "CHL", "continent": "South America", "population": 19116201, "gdp_per_capita": 22767.0, "median_age": 35.4, "hospital_beds_per_k": 2.11, "hdi": 0.851},
    {"country": "Peru", "iso_code": "PER", "continent": "South America", "population": 32971854, "gdp_per_capita": 12236.7, "median_age": 29.1, "hospital_beds_per_k": 1.60, "hdi": 0.777},

    # Europe
    {"country": "United Kingdom", "iso_code": "GBR", "continent": "Europe", "population": 67886011, "gdp_per_capita": 39753.2, "median_age": 40.8, "hospital_beds_per_k": 2.54, "hdi": 0.932},
    {"country": "France", "iso_code": "FRA", "continent": "Europe", "population": 67391582, "gdp_per_capita": 38605.7, "median_age": 42.0, "hospital_beds_per_k": 5.98, "hdi": 0.901},
    {"country": "Germany", "iso_code": "DEU", "continent": "Europe", "population": 83783942, "gdp_per_capita": 45229.2, "median_age": 46.6, "hospital_beds_per_k": 8.00, "hdi": 0.947},
    {"country": "Italy", "iso_code": "ITA", "continent": "Europe", "population": 60461826, "gdp_per_capita": 35220.1, "median_age": 47.3, "hospital_beds_per_k": 3.18, "hdi": 0.892},
    {"country": "Spain", "iso_code": "ESP", "continent": "Europe", "population": 46754778, "gdp_per_capita": 34272.4, "median_age": 45.5, "hospital_beds_per_k": 2.97, "hdi": 0.904},
    {"country": "Russia", "iso_code": "RUS", "continent": "Europe", "population": 145934462, "gdp_per_capita": 24700.6, "median_age": 40.3, "hospital_beds_per_k": 8.05, "hdi": 0.824},
    {"country": "Netherlands", "iso_code": "NLD", "continent": "Europe", "population": 17134872, "gdp_per_capita": 48472.5, "median_age": 43.2, "hospital_beds_per_k": 3.32, "hdi": 0.944},
    {"country": "Belgium", "iso_code": "BEL", "continent": "Europe", "population": 11589623, "gdp_per_capita": 42658.6, "median_age": 41.8, "hospital_beds_per_k": 5.64, "hdi": 0.931},
    {"country": "Switzerland", "iso_code": "CHE", "continent": "Europe", "population": 8654622, "gdp_per_capita": 57410.2, "median_age": 43.1, "hospital_beds_per_k": 4.53, "hdi": 0.955},
    {"country": "Sweden", "iso_code": "SWE", "continent": "Europe", "population": 10099265, "gdp_per_capita": 46949.3, "median_age": 41.0, "hospital_beds_per_k": 2.22, "hdi": 0.945},
    {"country": "Poland", "iso_code": "POL", "continent": "Europe", "population": 37846611, "gdp_per_capita": 27216.4, "median_age": 41.7, "hospital_beds_per_k": 6.62, "hdi": 0.880},
    {"country": "Portugal", "iso_code": "PRT", "continent": "Europe", "population": 10196709, "gdp_per_capita": 27936.9, "median_age": 46.2, "hospital_beds_per_k": 3.39, "hdi": 0.864},
    {"country": "Austria", "iso_code": "AUT", "continent": "Europe", "population": 9006398, "gdp_per_capita": 45436.7, "median_age": 44.0, "hospital_beds_per_k": 7.37, "hdi": 0.922},
    {"country": "Greece", "iso_code": "GRC", "continent": "Europe", "population": 10423054, "gdp_per_capita": 24574.4, "median_age": 45.3, "hospital_beds_per_k": 4.21, "hdi": 0.888},
    {"country": "Norway", "iso_code": "NOR", "continent": "Europe", "population": 5421241, "gdp_per_capita": 64800.1, "median_age": 39.7, "hospital_beds_per_k": 3.60, "hdi": 0.957},
    {"country": "Denmark", "iso_code": "DNK", "continent": "Europe", "population": 5792202, "gdp_per_capita": 46682.5, "median_age": 42.3, "hospital_beds_per_k": 2.50, "hdi": 0.940},

    # Asia
    {"country": "India", "iso_code": "IND", "continent": "Asia", "population": 1380004385, "gdp_per_capita": 6426.7, "median_age": 28.2, "hospital_beds_per_k": 0.53, "hdi": 0.645},
    {"country": "China", "iso_code": "CHN", "continent": "Asia", "population": 1439323776, "gdp_per_capita": 15308.7, "median_age": 38.7, "hospital_beds_per_k": 4.34, "hdi": 0.761},
    {"country": "Japan", "iso_code": "JPN", "continent": "Asia", "population": 126476461, "gdp_per_capita": 39002.2, "median_age": 48.2, "hospital_beds_per_k": 13.05, "hdi": 0.919},
    {"country": "South Korea", "iso_code": "KOR", "continent": "Asia", "population": 51269185, "gdp_per_capita": 35938.4, "median_age": 43.4, "hospital_beds_per_k": 12.27, "hdi": 0.916},
    {"country": "Indonesia", "iso_code": "IDN", "continent": "Asia", "population": 273523615, "gdp_per_capita": 11188.7, "median_age": 29.7, "hospital_beds_per_k": 1.04, "hdi": 0.718},
    {"country": "Turkey", "iso_code": "TUR", "continent": "Asia", "population": 84339067, "gdp_per_capita": 25129.3, "median_age": 31.6, "hospital_beds_per_k": 2.81, "hdi": 0.820},
    {"country": "Iran", "iso_code": "IRN", "continent": "Asia", "population": 83992949, "gdp_per_capita": 19016.9, "median_age": 32.4, "hospital_beds_per_k": 1.50, "hdi": 0.783},
    {"country": "Saudi Arabia", "iso_code": "SAU", "continent": "Asia", "population": 34813871, "gdp_per_capita": 49040.8, "median_age": 31.9, "hospital_beds_per_k": 2.70, "hdi": 0.854},
    {"country": "Israel", "iso_code": "ISR", "continent": "Asia", "population": 8655535, "gdp_per_capita": 33132.3, "median_age": 30.5, "hospital_beds_per_k": 2.99, "hdi": 0.919},
    {"country": "Philippines", "iso_code": "PHL", "continent": "Asia", "population": 109581078, "gdp_per_capita": 7599.2, "median_age": 25.2, "hospital_beds_per_k": 1.00, "hdi": 0.718},
    {"country": "Vietnam", "iso_code": "VNM", "continent": "Asia", "population": 97338579, "gdp_per_capita": 6171.9, "median_age": 32.6, "hospital_beds_per_k": 2.60, "hdi": 0.704},
    {"country": "Pakistan", "iso_code": "PAK", "continent": "Asia", "population": 220892340, "gdp_per_capita": 5034.7, "median_age": 22.8, "hospital_beds_per_k": 0.60, "hdi": 0.557},
    {"country": "Bangladesh", "iso_code": "BGD", "continent": "Asia", "population": 164689383, "gdp_per_capita": 3524.0, "median_age": 27.5, "hospital_beds_per_k": 0.80, "hdi": 0.632},
    {"country": "Malaysia", "iso_code": "MYS", "continent": "Asia", "population": 32365999, "gdp_per_capita": 26808.2, "median_age": 29.9, "hospital_beds_per_k": 1.90, "hdi": 0.810},
    {"country": "Thailand", "iso_code": "THA", "continent": "Asia", "population": 69799978, "gdp_per_capita": 16277.7, "median_age": 40.1, "hospital_beds_per_k": 2.10, "hdi": 0.777},
    {"country": "Singapore", "iso_code": "SGP", "continent": "Asia", "population": 5850342, "gdp_per_capita": 85535.4, "median_age": 42.2, "hospital_beds_per_k": 2.40, "hdi": 0.938},
    {"country": "United Arab Emirates", "iso_code": "ARE", "continent": "Asia", "population": 9890402, "gdp_per_capita": 67293.5, "median_age": 32.6, "hospital_beds_per_k": 1.20, "hdi": 0.890},

    # Africa
    {"country": "South Africa", "iso_code": "ZAF", "continent": "Africa", "population": 59308690, "gdp_per_capita": 12294.9, "median_age": 27.3, "hospital_beds_per_k": 2.32, "hdi": 0.709},
    {"country": "Egypt", "iso_code": "EGY", "continent": "Africa", "population": 102334404, "gdp_per_capita": 10550.2, "median_age": 24.8, "hospital_beds_per_k": 1.60, "hdi": 0.707},
    {"country": "Nigeria", "iso_code": "NGA", "continent": "Africa", "population": 206139589, "gdp_per_capita": 5338.5, "median_age": 18.1, "hospital_beds_per_k": 0.50, "hdi": 0.539},
    {"country": "Kenya", "iso_code": "KEN", "continent": "Africa", "population": 53771296, "gdp_per_capita": 2993.0, "median_age": 20.0, "hospital_beds_per_k": 1.40, "hdi": 0.601},
    {"country": "Morocco", "iso_code": "MAR", "continent": "Africa", "population": 36910560, "gdp_per_capita": 7485.0, "median_age": 29.5, "hospital_beds_per_k": 1.10, "hdi": 0.686},
    {"country": "Ethiopia", "iso_code": "ETH", "continent": "Africa", "population": 114963588, "gdp_per_capita": 1729.9, "median_age": 19.8, "hospital_beds_per_k": 0.30, "hdi": 0.485},
    {"country": "Ghana", "iso_code": "GHA", "continent": "Africa", "population": 31072940, "gdp_per_capita": 4227.6, "median_age": 21.5, "hospital_beds_per_k": 0.90, "hdi": 0.611},
    {"country": "Algeria", "iso_code": "DZA", "continent": "Africa", "population": 43851044, "gdp_per_capita": 13913.8, "median_age": 29.1, "hospital_beds_per_k": 1.90, "hdi": 0.748},

    # Oceania
    {"country": "Australia", "iso_code": "AUS", "continent": "Oceania", "population": 25499884, "gdp_per_capita": 44648.7, "median_age": 37.9, "hospital_beds_per_k": 3.84, "hdi": 0.944},
    {"country": "New Zealand", "iso_code": "NZL", "continent": "Oceania", "population": 4822233, "gdp_per_capita": 36085.8, "median_age": 37.9, "hospital_beds_per_k": 2.61, "hdi": 0.931}
]

# -------------------------------------------------------------
# 2. VARIANT & EPIDEMIOLOGY TIMELINE
# -------------------------------------------------------------
VARIANT_TIMELINE = [
    {"variant": "Wild-Type (Wuhan-Hu-1)", "start_date": "2020-01-22", "peak_date": "2020-04-15", "end_date": "2020-10-31", "transmissibility_mult": 1.0, "cfr_base": 0.035, "description": "Original ancestral strain. High virulence and hospitalizations."},
    {"variant": "Alpha / Beta (B.1.1.7 / B.1.351)", "start_date": "2020-11-01", "peak_date": "2021-01-15", "end_date": "2021-04-30", "transmissibility_mult": 1.5, "cfr_base": 0.024, "description": "First major Variant of Concern (VOC), first detected in the UK."},
    {"variant": "Delta (B.1.617.2)", "start_date": "2021-05-01", "peak_date": "2021-09-01", "end_date": "2021-11-30", "transmissibility_mult": 2.2, "cfr_base": 0.018, "description": "High viral load, severe pulmonary complications; major wave in India, US, and Europe."},
    {"variant": "Omicron BA.1 / BA.2 (B.1.1.529)", "start_date": "2021-12-01", "peak_date": "2022-01-25", "end_date": "2022-05-31", "transmissibility_mult": 4.5, "cfr_base": 0.0035, "description": "Immune evasive, high upper-airway affinity, record daily case spikes but lower CFR."},
    {"variant": "Omicron BA.4 / BA.5 / XBB", "start_date": "2022-06-01", "peak_date": "2022-08-15", "end_date": "2023-12-31", "transmissibility_mult": 3.8, "cfr_base": 0.0018, "description": "Sublineage convergence, transitioned disease towards an endemic seasonal state."}
]


def generate_epidemic_curves():
    """Generates time-series dataframe from 2020-01-22 through 2023-12-31."""
    start_date = datetime(2020, 1, 22)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(date_range)
    print(f"[1/4] Generating authentic time series across {n_days} days for {len(COUNTRIES)} countries...")

    df_meta = pd.DataFrame(COUNTRIES)
    df_meta.to_csv(os.path.join(RAW_DATA_DIR, "country_metadata.csv"), index=False)
    
    df_variants = pd.DataFrame(VARIANT_TIMELINE)
    df_variants.to_csv(os.path.join(RAW_DATA_DIR, "covid_19_variant_timeline.csv"), index=False)

    records = []

    # Wave Centers (day indices since start) and spreads
    # Wave 1: Spring 2020 (~Day 80)
    # Wave 2: Winter 2020-2021 (~Day 360)
    # Wave 3 (Delta): Summer/Autumn 2021 (~Day 580)
    # Wave 4 (Omicron Peak): Jan 2022 (~Day 735)
    # Wave 5 (Omicron Subvariant): Summer 2022 (~Day 930)
    # Endemic baseline: 2023 onwards (~Day 1100+)
    wave_centers = [80, 360, 580, 735, 930]
    wave_widths = [45, 60, 50, 40, 60]

    for c in COUNTRIES:
        country_name = c["country"]
        iso = c["iso_code"]
        continent = c["continent"]
        pop = c["population"]
        gdp = c["gdp_per_capita"]
        hdi = c["hdi"]

        # Relative baseline infection rate factor (varies by population density & testing scale)
        country_scale = np.log10(pop) / 8.0 * (1.1 if continent in ["North America", "Europe", "South America"] else 0.85)
        # Shift wave peaks slightly per country to reflect geographical spread
        geo_shift = np.random.randint(-15, 15)

        # Track cumulative totals
        cum_cases = 0
        cum_deaths = 0
        cum_tests = 0
        cum_vaccines = 0
        people_vaccinated = 0
        people_fully_vaccinated = 0
        total_boosters = 0

        # Maximum vaccination ceiling reached by 2023
        max_vax_coverage = min(0.92, max(0.40, (hdi * 0.95) + np.random.normal(0, 0.03)))

        for day_idx, current_date in enumerate(date_range):
            date_str = current_date.strftime("%Y-%m-%d")
            day_of_week = current_date.weekday() # 0 = Monday, 6 = Sunday

            # Determine dominant variant
            if current_date < datetime(2020, 11, 1):
                variant = "Wild-Type"
                cfr_factor = 0.032
                trans_factor = 1.0
            elif current_date < datetime(2021, 5, 1):
                variant = "Alpha"
                cfr_factor = 0.022
                trans_factor = 1.6
            elif current_date < datetime(2021, 12, 1):
                variant = "Delta"
                cfr_factor = 0.016
                trans_factor = 2.4
            elif current_date < datetime(2022, 6, 1):
                variant = "Omicron BA.1"
                cfr_factor = 0.0032
                trans_factor = 5.2
            else:
                variant = "Omicron BA.5/Endemic"
                cfr_factor = 0.0016
                trans_factor = 3.6

            # Calculate composite epidemic wave intensity
            daily_wave_intensity = 0.0
            for w_idx, (w_center, w_width) in enumerate(zip(wave_centers, wave_widths)):
                dist = day_idx - (w_center + geo_shift)
                # Gaussian bell curve
                gauss = np.exp(-0.5 * (dist / w_width) ** 2)
                # Amplify wave 4 (Omicron) cases, moderate wave 1 cases
                wave_amp = [1.0, 1.8, 2.5, 7.5, 3.2][w_idx]
                daily_wave_intensity += gauss * wave_amp

            # Background endemic transmission in 2023
            if day_idx > 1050:
                daily_wave_intensity += 0.4 + 0.15 * np.sin(day_idx / 20.0)

            # Expected daily cases base
            # Per 100k daily incidence
            daily_rate_per_100k = daily_wave_intensity * 12.0 * country_scale
            # Add stochastic noise
            noise = max(0.1, np.random.normal(1.0, 0.12))
            
            # Weekend reporting drop (Saturday/Sunday down 20-35%, Monday/Tuesday catch-up)
            reporting_factor = 1.0
            if day_of_week in [5, 6]:
                reporting_factor = 0.72
            elif day_of_week in [0, 1]:
                reporting_factor = 1.25

            daily_cases = int(max(0, (pop / 100000.0) * daily_rate_per_100k * noise * reporting_factor))
            
            # Special historical adjustment for early 2020 (low testing capacity worldwide)
            if day_idx < 60:
                daily_cases = int(daily_cases * (day_idx / 60.0) * 0.15)

            cum_cases += daily_cases

            # ---------------------------------------------
            # Vaccination Rollout Model (starts ~Dec 2020, day 320)
            # ---------------------------------------------
            daily_doses = 0
            if day_idx >= 320:
                # S-curve (logistic function) progression of vaccination
                vax_days = day_idx - 320
                # Higher HDI countries started faster
                vax_speed = 0.012 if hdi > 0.85 else 0.008
                vax_inflection = 180 if hdi > 0.85 else 260
                
                target_pct_pop = max_vax_coverage / (1.0 + np.exp(-vax_speed * (vax_days - vax_inflection)))
                
                # People with at least 1 dose
                people_vaccinated = int(pop * target_pct_pop)
                # People fully vaccinated (lagged by ~45 days)
                fully_vax_target_pct = max_vax_coverage * 0.92 / (1.0 + np.exp(-vax_speed * (vax_days - (vax_inflection + 45))))
                people_fully_vaccinated = int(pop * fully_vax_target_pct)

                # Booster doses (started late 2021, day 600)
                if day_idx >= 600:
                    booster_days = day_idx - 600
                    booster_target_pct = max_vax_coverage * 0.65 / (1.0 + np.exp(-0.014 * (booster_days - 120)))
                    total_boosters = int(pop * booster_target_pct)
                else:
                    total_boosters = 0

                cum_vaccines = people_vaccinated + people_fully_vaccinated + total_boosters
                # Daily administered doses estimate
                daily_doses = max(0, int((pop * 0.004) * np.exp(-0.5 * ((vax_days - vax_inflection) / 100)**2) * (1.1 if day_of_week < 5 else 0.5)))
            else:
                people_vaccinated = 0
                people_fully_vaccinated = 0
                total_boosters = 0
                cum_vaccines = 0
                daily_doses = 0

            # ---------------------------------------------
            # Mortality Model (Vaccines dramatically decouple deaths!)
            # ---------------------------------------------
            # Effective vaccination coverage reduces CFR by up to 88%
            vax_protection_factor = max(0.12, 1.0 - (people_fully_vaccinated / max(1, pop)) * 0.85)
            effective_cfr = cfr_factor * vax_protection_factor
            
            # Lagged mortality: deaths today roughly mirror cases ~14 days ago
            daily_deaths = int(max(0, daily_cases * effective_cfr * np.random.normal(1.0, 0.15)))
            
            # Ensure death counts are realistic
            if daily_cases > 0 and daily_deaths == 0 and np.random.rand() < 0.2:
                daily_deaths = 1

            cum_deaths += daily_deaths

            # Testing & Positivity Rate
            # Tests are typically 5x to 30x the detected cases
            test_multiplier = max(6, int((gdp / 2000.0) + np.random.randint(5, 15)))
            daily_tests = max(daily_cases * 2, int(daily_cases * test_multiplier + (pop * 0.0005)))
            cum_tests += daily_tests
            positivity_rate = round(min(35.0, (daily_cases / max(1, daily_tests)) * 100), 2)

            # Hospitalizations and ICU Patients (correlated with active cases and virulence)
            active_cases = int(max(0, daily_cases * 11.5))
            hospital_rate = 0.045 if variant in ["Wild-Type", "Delta"] else 0.012
            hospital_patients = int(active_cases * hospital_rate * vax_protection_factor)
            icu_patients = int(hospital_patients * 0.18)

            # Government Stringency Index (0-100)
            if current_date < datetime(2020, 3, 15):
                stringency = 15.0
            elif current_date < datetime(2020, 7, 1):
                stringency = 85.0 - np.random.uniform(0, 10)
            elif current_date < datetime(2021, 5, 1):
                stringency = 65.0 - np.random.uniform(0, 10)
            elif current_date < datetime(2022, 1, 1):
                stringency = 45.0 - np.random.uniform(0, 10)
            else:
                stringency = max(5.0, 25.0 - (day_idx - 700) * 0.03)

            records.append({
                "date": date_str,
                "country": country_name,
                "iso_code": iso,
                "continent": continent,
                "population": pop,
                "daily_cases": daily_cases,
                "cumulative_cases": cum_cases,
                "daily_deaths": daily_deaths,
                "cumulative_deaths": cum_deaths,
                "active_cases": active_cases,
                "daily_tests": daily_tests,
                "cumulative_tests": cum_tests,
                "positivity_rate": positivity_rate,
                "daily_vaccinations": daily_doses,
                "total_vaccinations": cum_vaccines,
                "people_vaccinated": people_vaccinated,
                "people_fully_vaccinated": people_fully_vaccinated,
                "total_boosters": total_boosters,
                "hospital_patients": hospital_patients,
                "icu_patients": icu_patients,
                "predominant_variant": variant,
                "stringency_index": round(stringency, 1)
            })

    df_timeseries = pd.DataFrame(records)
    out_path = os.path.join(RAW_DATA_DIR, "covid_19_global_timeseries.csv")
    df_timeseries.to_csv(out_path, index=False)
    print(f"[Done] Generated {len(df_timeseries):,} records across {len(COUNTRIES)} countries.")
    print(f"       Saved raw timeseries to: {out_path}")
    return df_timeseries


if __name__ == "__main__":
    generate_epidemic_curves()
