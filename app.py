import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Energy Data Analysis", layout="wide")
st.title("📊 Global Energy Analysis Dashboard")

# Load the CSV directly from file
file_path = "global-data-on-sustainable-energy.csv"
df = pd.read_csv(file_path)

st.success("✅ Data loaded successfully!")
st.write("### Raw Data Preview")
st.dataframe(df.head())

st.markdown("---")

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
    'Energy intensity level of primary energy (MJ per $2017 PPP GDP)': 'Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP',
    'CO2 emissions (kT) (by country)': 'Value_co2_emissions_kt_by_country',
    'Renewables (equivalent primary energy)': 'Renewables_equivalent_primary_energy',
    'GDP growth (annual %)': 'gdp_growth',
    'GDP per capita (current US$)': 'gdp_per_capita',
    'Population density (people per sq. km of land area)': 'Density_n_P_Km2',
    'Land area (sq. km)': 'Land_Area_Km2'
}, inplace=True)

# KPIs Section
st.header("🌟 Key Performance Indicators")
col1, col2, col3 = st.columns(3)

with col1:
    avg_energy = df["Primary_energy_consumption_per_capita_kWh_person"].mean()
    st.metric("Avg. Energy Consumption (kWh/person)", f"{avg_energy:.2f}")

with col2:
    avg_gdp = df["gdp_per_capita"].mean()
    st.metric("Avg. GDP per Capita", f"${avg_gdp:,.2f}")

with col3:
    avg_access = df["Access_to_electricity_of_population"].mean()
    st.metric("Avg. Electricity Access (%)", f"{avg_access:.2f}%")

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

# Dynamic scatter plot: Select any 2 features
st.subheader("💡 Explore Relationships Between Features")
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
x_col = st.selectbox("Select X-axis", numeric_cols, index=numeric_cols.index("gdp_per_capita") if "gdp_per_capita" in numeric_cols else 0)
y_col = st.selectbox("Select Y-axis", numeric_cols, index=numeric_cols.index("Primary_energy_consumption_per_capita_kWh_person") if "Primary_energy_consumption_per_capita_kWh_person" in numeric_cols else 1)

fig2, ax2 = plt.subplots()
sns.scatterplot(
    data=df,
    x=x_col,
    y=y_col,
    hue="Access_to_electricity_of_population" if "Access_to_electricity_of_population" in df.columns else None,
    palette="viridis",
    ax=ax2
)
ax2.set_xlabel(x_col)
ax2.set_ylabel(y_col)
st.pyplot(fig2)
