"""
COVID-19 Global Data Visualization & Comparative Analytics Dashboard
Built with Streamlit & Plotly
Features:
- Global KPIs and Interactive Choropleth Map
- Country-Wise Comparative Analysis & Trajectory Curves
- Cases, Recoveries & Fatalities Dynamic Trends
- Vaccine Decoupling & Clinical Impact Analysis
- Live Data Explorer & Executive Excel Report Exporter
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="COVID-19 Global Analytics Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #F8F9FA;
        border-radius: 10px;
        padding: 15px 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        border-left: 5px solid #1F4E79;
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a252f;
        margin-top: 4px;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #28a745;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading with Caching
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")


@st.cache_data
def load_data():
    ts_file = os.path.join(PROCESSED_DIR, "covid_19_cleaned_timeseries.csv")
    country_file = os.path.join(PROCESSED_DIR, "covid_19_country_summary.csv")
    global_file = os.path.join(PROCESSED_DIR, "covid_19_global_summary.csv")

    if not os.path.exists(ts_file) or not os.path.exists(country_file):
        # Auto-run cleaning if files not pre-generated
        from src.data_cleaning import clean_and_transform_covid_data
        clean_and_transform_covid_data()

    df_ts = pd.read_csv(ts_file)
    df_ts['date'] = pd.to_datetime(df_ts['date'])
    df_country = pd.read_csv(country_file)
    df_global = pd.read_csv(global_file)
    df_global['date'] = pd.to_datetime(df_global['date'])

    return df_ts, df_country, df_global


try:
    df_ts, df_country, df_global = load_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}. Please run the pipeline script first.")
    st.stop()

# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/fluency/96/coronavirus.png", width=64)
st.sidebar.title("Dashboard Controls")

# Date range selection
min_date = df_ts['date'].min().to_pydatetime()
max_date = df_ts['date'].max().to_pydatetime()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_dt, end_dt = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_dt, end_dt = min_date, max_date

# Continent Filter
continents = sorted(df_country['continent'].dropna().unique().tolist())
selected_continents = st.sidebar.multiselect(
    "Filter Continents",
    options=continents,
    default=continents
)

# Country Selection
available_countries = df_country[df_country['continent'].isin(selected_continents)]['country'].sort_values().tolist()
top_10_default = df_country.sort_values('cumulative_cases', ascending=False)['country'].head(8).tolist()

col_btn1, col_btn2 = st.sidebar.columns(2)
if col_btn1.button("Top 10 Countries"):
    st.session_state['selected_countries'] = top_10_default
if col_btn2.button("Select All"):
    st.session_state['selected_countries'] = available_countries

default_selected = st.session_state.get('selected_countries', [c for c in top_10_default if c in available_countries])

selected_countries = st.sidebar.multiselect(
    "Select Countries for Deep Analysis",
    options=available_countries,
    default=default_selected
)

# Metric Mode Toggle
metric_mode = st.sidebar.radio(
    "Metric Display Mode",
    ["Absolute Counts", "Per Million Population"],
    index=0
)

# Smoothing
smoothing_opt = st.sidebar.selectbox(
    "Data Smoothing",
    ["7-Day Moving Average", "Raw Daily Numbers"],
    index=0
)

# Filter timeseries
filtered_ts = df_ts[
    (df_ts['date'] >= start_dt) &
    (df_ts['date'] <= end_dt) &
    (df_ts['continent'].isin(selected_continents))
]

filtered_country = df_country[
    (df_country['continent'].isin(selected_continents))
]

# -------------------------------------------------------------
# MAIN HEADER
# -------------------------------------------------------------
st.markdown('<div class="main-header">🦠 Global COVID-19 Epidemiology & Comparative Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive tracking of global cases, recoveries, fatalities, vaccination decoupling, and country-level benchmarking (2020 – 2023)</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# GLOBAL METRIC SCORECARDS
# -------------------------------------------------------------
tot_cases = filtered_country['cumulative_cases'].sum()
tot_deaths = filtered_country['cumulative_deaths'].sum()
tot_recovered = filtered_country['cumulative_recovered'].sum()
tot_active = filtered_country['active_cases'].sum()
tot_vax = filtered_country['total_vaccinations'].sum()
global_cfr = (tot_deaths / max(1, tot_cases)) * 100
global_rec_rate = (tot_recovered / max(1, tot_cases)) * 100

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #2b5797;">
        <div class="kpi-title">Total Cases</div>
        <div class="kpi-value">{tot_cases:,.0f}</div>
        <div class="kpi-sub">Across {len(filtered_country)} countries</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #e74c3c;">
        <div class="kpi-title">Total Fatalities</div>
        <div class="kpi-value">{tot_deaths:,.0f}</div>
        <div class="kpi-sub" style="color: #e74c3c;">CFR: {global_cfr:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #27ae60;">
        <div class="kpi-title">Recoveries</div>
        <div class="kpi-value">{tot_recovered:,.0f}</div>
        <div class="kpi-sub">Rate: {global_rec_rate:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #f39c12;">
        <div class="kpi-title">Active Cases</div>
        <div class="kpi-value">{tot_active:,.0f}</div>
        <div class="kpi-sub" style="color: #f39c12;">Current Burden</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #16a085;">
        <div class="kpi-title">Vaccine Doses</div>
        <div class="kpi-value">{tot_vax:,.0f}</div>
        <div class="kpi-sub">Global Rollout</div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    avg_vax_pct = filtered_country['fully_vaccinated_pct'].mean()
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #8e44ad;">
        <div class="kpi-title">Avg Fully Vaccinated</div>
        <div class="kpi-value">{avg_vax_pct:.1f}%</div>
        <div class="kpi-sub" style="color: #8e44ad;">Population Share</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB NAVIGATION
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Global Map & Overview",
    "📊 Country-Wise Comparative Analysis",
    "📈 Cases, Recoveries & Death Trends",
    "💉 Vaccine Decoupling Impact",
    "📥 Data Explorer & Reports"
])

# =============================================================
# TAB 1: GLOBAL MAP & OVERVIEW
# =============================================================
with tab1:
    st.subheader("Global Epidemiological Spread (Interactive Choropleth)")
    
    col_map_metric, col_map_scope = st.columns([2, 1])
    with col_map_metric:
        map_metric = st.selectbox(
            "Select Map Metric",
            [
                "cumulative_cases", "cumulative_deaths", "cumulative_recovered",
                "cases_per_million", "deaths_per_million",
                "fully_vaccinated_pct", "case_fatality_rate_pct"
            ],
            format_func=lambda x: {
                "cumulative_cases": "Total Confirmed Cases",
                "cumulative_deaths": "Total Fatalities",
                "cumulative_recovered": "Estimated Recoveries",
                "cases_per_million": "Cases per Million People",
                "deaths_per_million": "Deaths per Million People",
                "fully_vaccinated_pct": "Fully Vaccinated Population (%)",
                "case_fatality_rate_pct": "Case Fatality Rate (CFR %)"
            }[x]
        )

    # Choropleth Map using Plotly
    color_scales = {
        "cumulative_cases": "Blues",
        "cumulative_deaths": "Reds",
        "cumulative_recovered": "Greens",
        "cases_per_million": "Oranges",
        "deaths_per_million": "Purples",
        "fully_vaccinated_pct": "Tealgrn",
        "case_fatality_rate_pct": "YlOrRd"
    }

    fig_map = px.choropleth(
        filtered_country,
        locations="iso_code",
        color=map_metric,
        hover_name="country",
        hover_data={
            "iso_code": False,
            "cumulative_cases": ":,",
            "cumulative_deaths": ":,",
            "cumulative_recovered": ":,",
            "fully_vaccinated_pct": ":.1f%",
            "case_fatality_rate_pct": ":.2f%"
        },
        color_continuous_scale=color_scales.get(map_metric, "Viridis"),
        projection="natural earth"
    )
    fig_map.update_layout(
        margin={"r": 0, "t": 20, "l": 0, "b": 0},
        height=520,
        geo=dict(showcoastlines=True, coastlinecolor="LightGray", showland=True, landcolor="#f8f9fa")
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Continental Breakdown Section
    c_col1, c_col2 = st.columns([1, 1])
    with c_col1:
        st.subheader("Distribution by Continent")
        cont_cases = filtered_country.groupby('continent')['cumulative_cases'].sum().reset_index()
        fig_pie = px.pie(
            cont_cases,
            values='cumulative_cases',
            names='continent',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c_col2:
        st.subheader("Continental CFR & Recovery Rate")
        cont_rates = filtered_country.groupby('continent').agg({
            'cumulative_cases': 'sum',
            'cumulative_deaths': 'sum',
            'cumulative_recovered': 'sum'
        }).reset_index()
        cont_rates['CFR (%)'] = (cont_rates['cumulative_deaths'] / cont_rates['cumulative_cases'] * 100).round(2)
        cont_rates['Recovery Rate (%)'] = (cont_rates['cumulative_recovered'] / cont_rates['cumulative_cases'] * 100).round(2)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='Recovery Rate (%)',
            x=cont_rates['continent'],
            y=cont_rates['Recovery Rate (%)'],
            marker_color='#27ae60'
        ))
        fig_bar.add_trace(go.Bar(
            name='Case Fatality Rate (%)',
            x=cont_rates['continent'],
            y=cont_rates['CFR (%)'],
            marker_color='#e74c3c'
        ))
        fig_bar.update_layout(
            barmode='group',
            height=350,
            margin=dict(t=20, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# =============================================================
# TAB 2: COUNTRY-WISE COMPARATIVE ANALYSIS
# =============================================================
with tab2:
    st.subheader("Country-Wise Comparative Analytics")

    if not selected_countries:
        st.warning("Please select at least one country from the sidebar filter.")
    else:
        comp_df = filtered_ts[filtered_ts['country'].isin(selected_countries)]
        
        col_scale1, col_scale2 = st.columns([3, 1])
        with col_scale2:
            log_scale = st.checkbox("Logarithmic Y-Axis", value=False)

        case_col = 'daily_cases_7d_avg' if smoothing_opt == "7-Day Moving Average" else 'daily_cases'
        death_col = 'daily_deaths_7d_avg' if smoothing_opt == "7-Day Moving Average" else 'daily_deaths'

        # Comparative Epidemic Curves
        fig_comp = px.line(
            comp_df,
            x='date',
            y=case_col,
            color='country',
            title=f"Comparative Daily Infection Trends ({smoothing_opt})",
            labels={case_col: "Daily Cases", "date": "Date"},
            log_y=log_scale
        )
        fig_comp.update_layout(height=450, hovermode="x unified", legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_comp, use_container_width=True)

        # Comparative Trajectory Chart (Log New Cases vs Log Cumulative Cases)
        st.subheader("Epidemic Trajectory Curve (Log-Log Scale)")
        st.caption("Visualizes whether countries are actively 'bending the curve' (falling off the straight trajectory line).")

        fig_traj = go.Figure()
        for country in selected_countries:
            c_data = comp_df[comp_df['country'] == country].sort_values('date')
            fig_traj.add_trace(go.Scatter(
                x=c_data['cumulative_cases'],
                y=c_data['daily_cases_7d_avg'],
                mode='lines',
                name=country
            ))
        fig_traj.update_xaxes(type="log", title="Total Cumulative Cases (Log Scale)")
        fig_traj.update_yaxes(type="log", title="New Confirmed Cases 7-Day Avg (Log Scale)")
        fig_traj.update_layout(height=450, legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_traj, use_container_width=True)

        # Top Rankings Bar Comparison
        st.subheader("Key Metric Benchmarks (Selected Nations)")
        c_summary = filtered_country[filtered_country['country'].isin(selected_countries)].sort_values('cumulative_cases', ascending=False)
        
        b1, b2 = st.columns(2)
        with b1:
            fig_cases_bar = px.bar(
                c_summary,
                x='cumulative_cases',
                y='country',
                orientation='h',
                title="Total Confirmed Cases",
                color='cumulative_cases',
                color_continuous_scale="Blues"
            )
            fig_cases_bar.update_layout(height=380, yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
            st.plotly_chart(fig_cases_bar, use_container_width=True)

        with b2:
            fig_per_mil = px.bar(
                c_summary,
                x='cases_per_million',
                y='country',
                orientation='h',
                title="Infection Rate (Cases per Million People)",
                color='cases_per_million',
                color_continuous_scale="Viridis"
            )
            fig_per_mil.update_layout(height=380, yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
            st.plotly_chart(fig_per_mil, use_container_width=True)

# =============================================================
# TAB 3: CASES, RECOVERIES & DEATH TRENDS
# =============================================================
with tab3:
    st.subheader("Global Dynamics: Cases, Active Infections, Recoveries & Deaths")

    # Stacked Area Dynamic Breakdown
    fig_stacked = go.Figure()
    fig_stacked.add_trace(go.Scatter(
        x=df_global['date'],
        y=df_global['cumulative_recovered'],
        mode='lines',
        name='Total Recoveries',
        stackgroup='one',
        fillcolor='rgba(39, 174, 96, 0.7)',
        line=dict(color='#27ae60', width=0.5)
    ))
    fig_stacked.add_trace(go.Scatter(
        x=df_global['date'],
        y=df_global['active_cases'],
        mode='lines',
        name='Active Infectious Cases',
        stackgroup='one',
        fillcolor='rgba(243, 156, 18, 0.7)',
        line=dict(color='#f39c12', width=0.5)
    ))
    fig_stacked.add_trace(go.Scatter(
        x=df_global['date'],
        y=df_global['cumulative_deaths'],
        mode='lines',
        name='Total Fatalities',
        stackgroup='one',
        fillcolor='rgba(231, 76, 60, 0.8)',
        line=dict(color='#e74c3c', width=0.5)
    ))

    fig_stacked.update_layout(
        title="Global Cumulative Distribution: Recovered vs Active vs Fatalities",
        height=450,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_stacked, use_container_width=True)

    # Dual Axis: Daily Recoveries vs Daily Cases
    st.subheader("Daily Incident Cases vs Daily Recoveries")
    fig_dual = go.Figure()
    fig_dual.add_trace(go.Scatter(
        x=df_global['date'],
        y=df_global['daily_cases_7d_avg'],
        name='Daily Cases (7D Avg)',
        line=dict(color='#2980b9', width=2)
    ))
    fig_dual.add_trace(go.Scatter(
        x=df_global['date'],
        y=df_global['daily_recovered_7d_avg'],
        name='Daily Recoveries (7D Avg)',
        line=dict(color='#27ae60', width=2, dash='dot')
    ))
    fig_dual.update_layout(height=420, hovermode="x unified", legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_dual, use_container_width=True)

# =============================================================
# TAB 4: VACCINE DECOUPLING IMPACT
# =============================================================
with tab4:
    st.subheader("The Vaccine Impact: Clinical Decoupling of Cases and Deaths")
    st.markdown("""
    > **Epidemiological Insight:** When mass vaccination rollouts reached critical thresholds in mid-2021, 
    > the historic correlation between surging infection counts and fatalities broke down dramatically. 
    > The Omicron wave produced record daily cases, yet mortality stayed vastly lower compared to earlier waves.
    """)

    # Scatter plot: Fully Vaccinated % vs Case Fatality Rate (CFR %)
    fig_scatter = px.scatter(
        filtered_country,
        x='fully_vaccinated_pct',
        y='case_fatality_rate_pct',
        size='population',
        color='continent',
        hover_name='country',
        text='country',
        trendline='ols',
        title="Correlation: Vaccination Coverage vs Case Fatality Rate (CFR %)",
        labels={
            'fully_vaccinated_pct': "Population Fully Vaccinated (%)",
            'case_fatality_rate_pct': "Case Fatality Rate (%)"
        }
    )
    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(height=520)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Global Vaccine Rollout Timeline
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.subheader("Global Vaccination Progress")
        fig_vax_ts = px.line(
            df_global,
            x='date',
            y=['people_vaccinated', 'people_fully_vaccinated', 'total_boosters'],
            title="Cumulative Vaccination Doses Administered",
            labels={'value': 'Total People', 'date': 'Date', 'variable': 'Milestone'}
        )
        fig_vax_ts.update_layout(height=400, legend=dict(orientation="h", y=-0.25))
        st.plotly_chart(fig_vax_ts, use_container_width=True)

    with v_col2:
        st.subheader("Top Vaccinated Countries")
        top_vax = filtered_country.sort_values('fully_vaccinated_pct', ascending=False).head(10)
        fig_vax_bar = px.bar(
            top_vax,
            x='fully_vaccinated_pct',
            y='country',
            orientation='h',
            title="Highest Fully Vaccinated Populations (%)",
            color='fully_vaccinated_pct',
            color_continuous_scale="Tealgrn"
        )
        fig_vax_bar.update_layout(height=400, yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
        st.plotly_chart(fig_vax_bar, use_container_width=True)

# =============================================================
# TAB 5: DATA EXPLORER & REPORTS
# =============================================================
with tab5:
    st.subheader("Interactive Dataset Explorer")
    
    # Filterable Dataframe
    display_cols = [
        'country', 'continent', 'population', 'cumulative_cases',
        'cumulative_deaths', 'cumulative_recovered', 'active_cases',
        'cases_per_million', 'deaths_per_million', 'case_fatality_rate_pct',
        'recovery_rate_pct', 'fully_vaccinated_pct'
    ]
    st.dataframe(filtered_country[display_cols].sort_values('cumulative_cases', ascending=False), use_container_width=True)

    # Export Buttons
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        csv_data = filtered_country[display_cols].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Country Summary as CSV",
            data=csv_data,
            file_name="covid19_country_summary_filtered.csv",
            mime="text/csv"
        )

    with col_exp2:
        excel_path = os.path.join(REPORTS_DIR, "COVID19_Global_Executive_Report.xlsx")
        if os.path.exists(excel_path):
            with open(excel_path, "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="📊 Download Multi-Sheet Executive Excel Report (.xlsx)",
                data=excel_bytes,
                file_name="COVID19_Global_Executive_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Executive Excel report will be available after running the export pipeline.")
