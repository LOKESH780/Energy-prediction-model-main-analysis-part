import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Config ---
st.set_page_config(page_title="Energy Data Deep Dive", layout="wide")
st.title("⚡ Global Energy Analytics Dashboard")

# --- Load and Prepare Data ---
df = pd.read_csv("global-data-on-sustainable-energy.csv")

rename_dict = {
    'Access to electricity (% of population)': 'Access_to_electricity_of_population',
    'Access to clean fuels for cooking (% of population)': 'Access_to_clean_fuels_for_cooking',
    'Renewable-electricity-generating-capacity-per-capita': 'Renewable_electricity_generating_capacity_per_capita',
    'Financial flows to developing countries (US$)': 'Financial_flows_to_developing_countries_US',
    'Renewable energy share in the total final energy consumption (%)': 'Renewable_energy_share_in_the_total_final_energy_consumption',
    'Electricity from fossil fuels (TWh)': 'Electricity_from_fossil_fuels_TWh',
    'Electricity from nuclear (TWh)': 'Electricity_from_nuclear_TWh',
    'Electricity from renewables (TWh)': 'Electricity_from_renewables_TWh',
    'Low-carbon electricity (% electricity)': 'Low_carbon_electricity_electricity',
    'Primary energy consumption per capita (kWh/person)': 'Primary_energy_consumption_per_capita_kWh_person',
    'Energy intensity level of primary energy (MJ/$2017 PPP GDP)': 'Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP',
    'CO2 emissions (kT) (by country)': 'Value_co2_emissions_kt_by_country',
    'Renewables (equivalent primary energy)': 'Renewables_equivalent_primary_energy',
    'GDP growth (annual %)': 'gdp_growth',
    'GDP per capita (current US$)': 'gdp_per_capita',
    'Population density (people per sq. km of land area)': 'Density_n_P_Km2',
    'Land Area(Km2)': 'Land_Area_Km2'
}
df.rename(columns=rename_dict, inplace=True)

# --- Sidebar Filters ---
st.sidebar.header("🔽 Filters")
years = sorted(df['Year'].dropna().unique())
entities = sorted(df['Entity'].dropna().unique())

selected_year = st.sidebar.selectbox("Select Year", ['All'] + years)
selected_entity = st.sidebar.selectbox("Select Entity", ['All'] + entities)

df_year = df.copy()
if selected_year != 'All':
    df_year = df_year[df_year['Year'] == selected_year]
if selected_entity != 'All':
    df_year = df_year[df_year['Entity'] == selected_entity]

# --- Tabs ---
tabs = st.tabs(["Overview KPIs", "Renewable + Electricity Insights"])

# --- Tab 1: Overview KPIs ---
with tabs[0]:
    st.header("📌 Business KPIs Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Access to Electricity (%)", f"{df_year['Access_to_electricity_of_population'].mean():.2f}")
    with col2:
        st.metric("Average Renewable Energy Share (%)", f"{df_year['Renewable_energy_share_in_the_total_final_energy_consumption'].mean():.2f}")
    with col3:
        st.metric("Average CO₂ Emissions (kt)", f"{df_year['Value_co2_emissions_kt_by_country'].mean():,.2f}")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Average Land Area (sq.km)", f"{df_year['Land_Area_Km2'].mean():,.0f}")
    with col5:
        st.metric("Average GDP Growth (%)", f"{df_year['gdp_growth'].mean():.2f}")
    with col6:
        total_countries = df_year['Entity'].nunique()
        st.metric("Total Countries", f"{total_countries}")

# --- Tab 2: Renewable + Electricity Insights ---
with tabs[1]:
    st.header("♻️ Renewable and Electricity Insights")

    # --- Renewable Capacity Trend (Area Chart) ---
    st.subheader("📈 Renewable Electricity Generating Capacity Trend")
    if 'Year' in df.columns:
        renewable_capacity_trend = df.groupby('Year')['Renewable_electricity_generating_capacity_per_capita'].mean().reset_index()
        fig_capacity = px.area(
            renewable_capacity_trend,
            x='Year',
            y='Renewable_electricity_generating_capacity_per_capita',
            labels={"Year": "Year", "Renewable_electricity_generating_capacity_per_capita": "Renewable Capacity per Capita"},
            color_discrete_sequence=["green"]
        )
        fig_capacity.update_traces(hovertemplate="Year: %{x}<br>Capacity: %{y:.2f}")
        st.plotly_chart(fig_capacity, use_container_width=True)

    # --- Top/Bottom 5 Clean Fuel Access (Bar Charts) ---
    st.subheader("🏆 Top and Bottom 5 Countries: Clean Fuel Access")

    clean_fuel_avg = df.groupby('Entity')['Access_to_clean_fuels_for_cooking'].mean().reset_index()
    clean_fuel_avg = clean_fuel_avg.dropna(subset=['Access_to_clean_fuels_for_cooking'])
    top_5_clean = clean_fuel_avg.sort_values(by='Access_to_clean_fuels_for_cooking', ascending=False).head(5)
    bottom_5_clean = clean_fuel_avg.sort_values(by='Access_to_clean_fuels_for_cooking', ascending=True).head(5)

    col7, col8 = st.columns(2)
    with col7:
        st.subheader("Top 5 Countries (Clean Fuel Access)")
        fig_top_clean = px.bar(
            top_5_clean,
            x='Entity',
            y='Access_to_clean_fuels_for_cooking',
            color='Entity',
            labels={"Entity": "Country", "Access_to_clean_fuels_for_cooking": "Access to Clean Fuel (%)"},
            color_discrete_sequence=px.colors.qualitative.G10
        )
        fig_top_clean.update_traces(hovertemplate="Country: %{x}<br>Access: %{y:.2f}%")
        st.plotly_chart(fig_top_clean, use_container_width=True)

    with col8:
        st.subheader("Bottom 5 Countries (Clean Fuel Access)")
        fig_bottom_clean = px.bar(
            bottom_5_clean,
            x='Entity',
            y='Access_to_clean_fuels_for_cooking',
            color='Entity',
            labels={"Entity": "Country", "Access_to_clean_fuels_for_cooking": "Access to Clean Fuel (%)"},
            color_discrete_sequence=px.colors.qualitative.G10
        )
        fig_bottom_clean.update_traces(hovertemplate="Country: %{x}<br>Access: %{y:.2f}%")
        st.plotly_chart(fig_bottom_clean, use_container_width=True)
