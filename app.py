import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Global Energy Dashboard", layout="wide")
st.title("🌍 Global Energy Consumption Analysis Dashboard")

# Load data
file_path = "global-data-on-sustainable-energy.csv"
df = pd.read_csv(file_path)

# Rename columns
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

# Sidebar filters
st.sidebar.header("🔎 Filter the Data")
year_options = df['Year'].dropna().unique()
entity_options = df['Entity'].dropna().unique()

selected_year = st.sidebar.selectbox("Select Year", sorted(year_options), index=0)
selected_entity = st.sidebar.selectbox("Select Country/Entity", sorted(entity_options), index=0)

# Apply filters
filtered_df = df[(df['Year'] == selected_year) & (df['Entity'] == selected_entity)]

# KPIs
st.header("📌 Key Business Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Access to Electricity (%)", f"{filtered_df['Access_to_electricity_of_population'].mean():.2f}")
with col2:
    st.metric("GDP per Capita ($)", f"{filtered_df['gdp_per_capita'].mean():,.2f}")
with col3:
    st.metric("CO₂ Emissions (kT)", f"{filtered_df['Value_co2_emissions_kt_by_country'].sum():,.0f}")
with col4:
    st.metric("Renewable Energy Share (%)", f"{filtered_df['Renewable_energy_share_in_the_total_final_energy_consumption'].mean():.2f}")

st.markdown("---")

# Line Chart - Energy Consumption Over Years
st.subheader("📈 Primary Energy Consumption Over the Years")
energy_trend = df.groupby('Year')["Primary_energy_consumption_per_capita_kWh_person"].mean().reset_index()
fig_line = px.line(energy_trend, x="Year", y="Primary_energy_consumption_per_capita_kWh_person",
                   labels={"Primary_energy_consumption_per_capita_kWh_person": "Avg Energy Consumption (kWh/person)"})
st.plotly_chart(fig_line, use_container_width=True)

# Choropleth Map - Access to Electricity
st.subheader("🗺️ Access to Electricity Across Countries")
map_df = df[df['Year'] == selected_year]
fig_map = px.choropleth(
    map_df,
    locations="Entity",
    locationmode="country names",
    color="Access_to_electricity_of_population",
    color_continuous_scale="YlGnBu",
    title=f"Access to Electricity in {selected_year}",
    labels={'Access_to_electricity_of_population':'Access to Electricity (%)'}
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# Bar Chart - Top 10 Renewable Share
st.subheader("🌿 Top 10 Countries by Renewable Energy Share")
top10 = df[df['Year'] == selected_year].nlargest(10, 'Renewable_energy_share_in_the_total_final_energy_consumption')
fig_bar = px.bar(
    top10,
    x="Entity",
    y="Renewable_energy_share_in_the_total_final_energy_consumption",
    color="Renewable_energy_share_in_the_total_final_energy_consumption",
    color_continuous_scale="viridis",
    labels={"Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Energy Share (%)"},
)
st.plotly_chart(fig_bar, use_container_width=True)

# Scatter Plot - GDP vs Energy
st.subheader("💡 GDP vs Energy Consumption")
fig_scatter = px.scatter(
    df,
    x="gdp_per_capita",
    y="Primary_energy_consumption_per_capita_kWh_person",
    size="Access_to_electricity_of_population",
    color="Renewable_energy_share_in_the_total_final_energy_consumption",
    hover_name="Entity",
    title="GDP vs Energy Consumption",
    color_continuous_scale="viridis",
    size_max=50
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Correlation Heatmap
st.subheader("📊 Correlation Heatmap of Features")
numeric_features = df.select_dtypes(include=['float64', 'int64'])
corr = numeric_features.corr()
fig_corr, ax_corr = plt.subplots(figsize=(12,8))
sns.heatmap(corr, cmap="coolwarm", ax=ax_corr)
st.pyplot(fig_corr)
