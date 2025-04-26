import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Energy Deep Dive", layout="wide")
st.title("🔋 Global Energy Analytics Dashboard")

# Load data
file_path = "global-data-on-sustainable-energy.csv"
df = pd.read_csv(file_path)

# Rename columns for easier coding
df.rename(columns={
    'Access to electricity (% of population)': 'Access_to_electricity_of_population',
    'Access to clean fuels for cooking (% of population)': 'Access_to_clean_fuels_for_cooking',
    'Renewable electricity Generating Capacity per capita': 'Renewable_electricity_generating_capacity_per_capita',
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
    'Land area (sq. km)': 'Land_Area_Km2'
}, inplace=True)

# Sidebar Filters
st.sidebar.header("🔎 Filters")
if 'Year' in df.columns:
    year_selected = st.sidebar.selectbox("Select Year", sorted(df['Year'].dropna().unique()))
    df = df[df['Year'] == year_selected]
if 'Entity' in df.columns:
    entity_selected = st.sidebar.selectbox("Select Country", sorted(df['Entity'].dropna().unique()))
    df = df[df['Entity'] == entity_selected]

# Handling missing values
df.fillna(0, inplace=True)

# TABS Layout
tabs = st.tabs(["Overview", "Energy Trends", "CO₂ Emissions", "Renewable Energy", "GDP vs Energy", "Correlation Analysis"])

# --- Tab 1: Overview ---
with tabs[0]:
    st.header("📋 Overview KPIs")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Access to Electricity", f"{df['Access_to_electricity_of_population'].mean():.2f}%")
        st.metric("Avg GDP per Capita", f"${df['gdp_per_capita'].mean()/1000:.2f}K")
    with col2:
        st.metric("Avg Renewable Share", f"{df['Renewable_energy_share_in_the_total_final_energy_consumption'].mean():.2f}%")
        st.metric("Avg Energy Intensity", f"{df['Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP'].mean():.2f} MJ")
    with col3:
        st.metric("Total CO₂ Emissions", f"{df['Value_co2_emissions_kt_by_country'].sum()/1e3:.2f} M tonnes")
        st.metric("Total Countries", f"{df['Entity'].nunique()}")

# --- Tab 2: Energy Trends ---
with tabs[1]:
    st.header("📈 Primary Energy Consumption Over Years")
    if 'Year' in df.columns:
        energy_trend = df.groupby('Year')['Primary_energy_consumption_per_capita_kWh_person'].mean().reset_index()
        fig1 = px.line(energy_trend, x='Year', y='Primary_energy_consumption_per_capita_kWh_person', title="Avg Energy Consumption Per Capita")
        st.plotly_chart(fig1, use_container_width=True)

# --- Tab 3: CO₂ Emissions Map ---
with tabs[2]:
    st.header("🌎 CO₂ Emissions by Country")
    if 'Entity' in df.columns and 'Value_co2_emissions_kt_by_country' in df.columns:
        fig2 = px.choropleth(df, locations="Entity", locationmode="country names",
                             color="Value_co2_emissions_kt_by_country",
                             title="CO₂ Emissions by Country",
                             color_continuous_scale=px.colors.sequential.Plasma)
        st.plotly_chart(fig2, use_container_width=True)

# --- Tab 4: Renewable Energy ---
with tabs[3]:
    st.header("🌿 Top 10 Renewable Share Countries")
    top_renewables = df.sort_values(by='Renewable_energy_share_in_the_total_final_energy_consumption', ascending=False).head(10)
    fig3 = px.bar(top_renewables, x='Entity', y='Renewable_energy_share_in_the_total_final_energy_consumption',
                  title="Top 10 Countries by Renewable Energy Share", color='Renewable_energy_share_in_the_total_final_energy_consumption')
    st.plotly_chart(fig3, use_container_width=True)

# --- Tab 5: GDP vs Energy ---
with tabs[4]:
    st.header("💹 GDP vs Energy Consumption")
    fig4 = px.scatter(df, x='gdp_per_capita', y='Primary_energy_consumption_per_capita_kWh_person',
                      size='Population' if 'Population' in df.columns else None,
                      title="GDP per Capita vs Energy Consumption",
                      color='Access_to_electricity_of_population')
    st.plotly_chart(fig4, use_container_width=True)

# --- Tab 6: Correlation ---
with tabs[5]:
    st.header("🔗 Correlation Matrix")
    numeric_cols = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_cols.corr()
    fig5, ax5 = plt.subplots(figsize=(14,8))
    sns.heatmap(corr, cmap="YlGnBu", annot=False, ax=ax5)
    st.pyplot(fig5)
