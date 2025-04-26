import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Energy Data Analysis", layout="wide")
st.title("📊 Global Energy Analysis Dashboard")

# Load the CSV directly from file
file_path = "global-data-on-sustainable-energy.csv"
df = pd.read_csv(file_path)

# Rename columns for easier access in code
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
with st.sidebar:
    st.markdown("### 🔽 Filter Data")
    if 'Year' in df.columns:
        selected_year = st.selectbox("Select Year", sorted(df['Year'].dropna().unique()))
        df = df[df['Year'] == selected_year]
    if 'Entity' in df.columns:
        selected_entity = st.selectbox("Select Country/Entity", sorted(df['Entity'].dropna().unique()))
        df = df[df['Entity'] == selected_entity]

# KPIs Section
st.header("📌 Business KPIs")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Access to Electricity", f"{df['Access_to_electricity_of_population'].mean():.2f}")
with col2:
    st.metric("Average Renewable Share", f"{df['Renewable_energy_share_in_the_total_final_energy_consumption'].mean():.2f}")
with col3:
    st.metric("Total CO₂ Emissions", f"{df['Value_co2_emissions_kt_by_country'].sum() / 1e3:.2f}M")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Average GDP per Capita", f"{df['gdp_per_capita'].mean()/1000:.2f}K")
with col5:
    st.metric("Average Energy Intensity", f"{df['Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP'].mean():.2f}")
with col6:
    total_countries = df['Entity'].nunique()
    st.metric("Total Countries", f"{total_countries}")

st.markdown("---")

# Correlation Heatmap
st.subheader("🔍 Correlation Heatmap")
numeric_df = df.select_dtypes(include=['float64', 'int64'])
corr = numeric_df.corr()
fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(corr, annot=False, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("---")

# Energy Consumption Trend
st.subheader("📈 Energy Consumption Over Years")
if 'Year' in df.columns:
    energy_trend = df.groupby('Year')["Primary_energy_consumption_per_capita_kWh_person"].mean().reset_index()
    st.line_chart(energy_trend.rename(columns={"Primary_energy_consumption_per_capita_kWh_person": "Avg. Energy"}))
else:
    st.warning("⚠️ 'Year' column not found in dataset.")

st.markdown("---")

# Scatter Plot (Fixed X and Y)
st.subheader("📊 GDP vs Energy Consumption (Fixed Axes)")
fig2, ax2 = plt.subplots()
sns.scatterplot(
    data=df,
    x="gdp_per_capita",
    y="Primary_energy_consumption_per_capita_kWh_person",
    hue="Access_to_electricity_of_population" if "Access_to_electricity_of_population" in df.columns else None,
    palette="viridis",
    ax=ax2
)
ax2.set_xlabel("GDP per Capita")
ax2.set_ylabel("Primary Energy Consumption per Capita (kWh/person)")
st.pyplot(fig2)
