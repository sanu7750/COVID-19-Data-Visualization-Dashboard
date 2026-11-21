# 📊 Tableau COVID-19 Analytics Dashboard – Implementation Guide

This guide provides exact step-by-step instructions to build the **COVID-19 Data Visualization Dashboard** in **Tableau Desktop / Tableau Public**, covering data connections, calculated fields, worksheet builds, interactive dashboard actions, and formatting.

---

## 📂 1. Tableau Data Sources

The Python pipeline automatically generates optimized CSV files inside `data/tableau_ready/`:

| Dataset File | Primary Purpose in Tableau | Key Fields |
| :--- | :--- | :--- |
| **`tableau_country_comparative.csv`** | Choropleth Map & Country Ranking sheets | `country`, `iso_code`, `continent`, `cumulative_cases`, `cumulative_deaths`, `cumulative_recovered`, `active_cases`, `cases_per_million`, `deaths_per_million`, `case_fatality_rate_pct`, `recovery_rate_pct`, `fully_vaccinated_pct` |
| **`tableau_daily_trends_timeseries.csv`** | Dual-axis time series & wave trajectory | `date`, `country`, `continent`, `daily_cases`, `daily_cases_7d_avg`, `daily_deaths`, `daily_deaths_7d_avg`, `daily_recovered`, `predominant_variant`, `stringency_index` |
| **`tableau_vaccination_vs_mortality.csv`** | Scatter plots & correlation analytics | `country`, `continent`, `population`, `fully_vaccinated_pct`, `case_fatality_rate_pct`, `cases_per_million` |

---

## 📐 2. Tableau Calculated Fields (Copy-Paste Formulas)

Create these calculated fields in Tableau for dynamic analysis:

### A. Case Fatality Rate (CFR %)
```tableau
(SUM([Cumulative Deaths]) / SUM([Cumulative Cases])) * 100
```
*Format: Number (Custom), 2 decimals, Suffix `%`*

### B. Recovery Rate (%)
```tableau
(SUM([Cumulative Recovered]) / SUM([Cumulative Cases])) * 100
```
*Format: Number (Custom), 2 decimals, Suffix `%`*

### C. Active Infection Rate (%)
```tableau
(SUM([Active Cases]) / SUM([Cumulative Cases])) * 100
```
*Format: Number (Custom), 2 decimals, Suffix `%`*

### D. Dynamic Metric Selector (Parameter Driven)
1. Create a Parameter: `Select Metric` (Data type: String, List of values: `Total Cases`, `Total Deaths`, `Total Recoveries`, `Cases per Million`, `Vaccination %`).
2. Create Calculated Field `Selected Metric Value`:
```tableau
CASE [Select Metric]
  WHEN 'Total Cases' THEN SUM([Cumulative Cases])
  WHEN 'Total Deaths' THEN SUM([Cumulative Deaths])
  WHEN 'Total Recoveries' THEN SUM([Cumulative Recovered])
  WHEN 'Cases per Million' THEN SUM([Cases Per Million])
  WHEN 'Vaccination %' THEN AVG([Fully Vaccinated Pct])
END
```

---

## 🛠️ 3. Step-by-Step Worksheet Construction

### Sheet 1: 🗺️ Global Epidemiological Choropleth Map
1. **Data Source:** `tableau_country_comparative.csv`
2. Ensure `iso_code` or `country` has Geographic Role: `Country/Region`.
3. Double-click `iso_code` (Tableau automatically generates Latitude and Longitude).
4. Drag `[Selected Metric Value]` (or `[Cumulative Cases]`) to **Color** in the Marks card.
5. In Marks card, select **Map**.
6. Edit Colors: Choose **Red-Blue Diverging** or **Viridis** gradient.
7. Drag `country`, `Cumulative Cases`, `Cumulative Deaths`, `Recovery Rate (%)`, and `Fully Vaccinated Pct` to **Tooltip**.

---

### Sheet 2: 📈 Dual-Axis Epidemic Waves (Cases vs Deaths)
1. **Data Source:** `tableau_daily_trends_timeseries.csv`
2. Drag `[date]` to **Columns** (Set to `Continuous Day` or `Continuous Week`).
3. Drag `[Daily Cases 7d Avg]` to **Rows**.
4. Drag `[Daily Deaths 7d Avg]` to the right side of the canvas to create a **Dual Axis**.
5. Right-click the right Y-axis and select **Synchronize Axis** (optional, or uncheck to show independent scales).
6. Set Mark Type:
   - Daily Cases: **Area** or **Line** (Color: `#1F4E79` Navy Blue, 40% opacity).
   - Daily Deaths: **Line** (Color: `#C00000` Crimson Red, thicker width).
7. Add a Reference Line or colored background bands for Variant Phases (Wild-Type, Alpha, Delta, Omicron).

---

### Sheet 3: 📊 Country-Wise Comparative Rankings (Bar Chart)
1. **Data Source:** `tableau_country_comparative.csv`
2. Drag `[country]` to **Rows**.
3. Drag `[Cumulative Cases]` (or `[Cases Per Million]`) to **Columns**.
4. Click the **Sort Descending** button on the toolbar.
5. Drag `[continent]` to **Color** for continental segmentation.
6. Drag `[Cumulative Cases]` to **Label** to display readable count on each bar.
7. Add a Filter on `country` (Top 10 or Top 15 by `Cumulative Cases`).

---

### Sheet 4: 💉 Vaccine Decoupling Scatter Plot
1. **Data Source:** `tableau_vaccination_vs_mortality.csv`
2. Drag `[Fully Vaccinated Pct]` to **Columns**.
3. Drag `[Case Fatality Rate (%)]` to **Rows**.
4. Drag `[country]` to **Detail** in Marks card.
5. Drag `[continent]` to **Color**.
6. Drag `[population]` to **Size**.
7. Go to **Analytics Tab** on the left panel, drag **Trend Line** onto the view (Linear or Polynomial).
   - *Observation:* Shows clear negative slope, confirming that higher vaccination coverage substantially lowers clinical fatality rates.

---

### Sheet 5: 🟢 Outcome Distribution (Donut Chart)
1. Drag `[Measure Values]` to **Rows**; keep only `Cumulative Recovered`, `Active Cases`, and `Cumulative Deaths`.
2. Set Mark Type to **Pie**.
3. Drag `[Measure Names]` to **Color** (Recovered = Green `#27AE60`, Active = Orange `#F39C12`, Deaths = Red `#E74C3C`).
4. Dual-axis with a blank minimum measure to punch a center hole and create a modern Donut Chart with total case count in center.

---

## 🖥️ 4. Executive Dashboard Assembly & Actions

1. Create a new Dashboard: Size `1920 x 1080` (or `Automatic`).
2. Add a Header Container: Title `"Global COVID-19 Epidemiology & Comparative Dashboard"`.
3. Add Top KPI Cards:
   - Total Confirmed Cases
   - Total Fatalities (CFR %)
   - Total Recoveries (Recovery %)
   - Global Doses Administered
4. Place **Choropleth Map** (Top Left) and **Country Comparative Ranking** (Top Right).
5. Place **Dual-Axis Wave Trends** (Bottom Left) and **Vaccine Decoupling Scatter** (Bottom Right).
6. **Set Up Interactive Filter Action:**
   - Go to `Dashboard` > `Actions` > `Add Action` > `Filter`.
   - Name: `Country Filter Action`.
   - Source Sheet: `Global Map` and `Country Rankings`.
   - Target Sheets: `Wave Trends` and `Vaccine Scatter`.
   - Run Action On: **Select (Click)**.
   - Clearing the selection: **Show all values**.
   - *Result:* Clicking any country on the world map dynamically updates all trend charts for that specific nation!
