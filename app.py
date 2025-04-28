import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Energy Data Deep Dive", layout="wide")
st.title("⚡ Global Energy Analytics Dashboard")

# Load the CSV
df = pd.read_csv("global-data-on-sustainable-energy.csv")

# Rename columns
rename_dict = {
    'Access to electricity (% of population)': 'Access_to_electricity_of_population',
    'Access to clean fuels for cooking': 'Access_to_clean_fuels_for_cooking',
    'Renewable-electricity-generating-capacity-per-capita': 'Renewable_electricity_generating_capacity_per_capita',
    'Financial flows to developing countries (US$)': 'Financial_flows_to_developing_countries_US',
    'Renewable energy share in the total final energy consumption (%)': 'Renewable_energy_share_in_the_total_final_energy_consumption',
    'Electricity from fossil fuels (TWh)': 'Electricity_from_fossil_fuels_TWh',
    'Electricity from nuclear (TWh)': 'Electricity_from_nuclear_TWh',
    'Electricity from renewables (TWh)': 'Electricity_from_renewables_TWh',
    'Low-carbon electricity (% electricity)': 'Low_carbon_electricity_electricity',
    'Primary energy consumption per capita (kWh/person)': 'Primary_energy_consumption_per_capita_kWh_person',
    'Energy intensity level of primary energy (MJ/$2017 PPP GDP)': 'Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP',
    'Value_co2_emissions_kt_by_country': 'Value_co2_emissions_kt_by_country',
    'Renewables (% equivalent primary energy)': 'Renewables_equivalent_primary_energy',
    'gdp_growth': 'gdp_growth',
    'gdp_per_capita': 'gdp_per_capita',
    'Density\n(P/Km2)': 'Density_n_P_Km2',
    'Land Area(Km2)': 'Land_Area_Km2'
}
df.rename(columns=rename_dict, inplace=True)

# Sidebar filters
st.sidebar.header("🔽 Filters")
years = sorted(df['Year'].dropna().unique())
entities = sorted(df['Entity'].dropna().unique())

selected_year = st.sidebar.selectbox("Select Year", ['All'] + years)
selected_entity = st.sidebar.selectbox("Select Entity", ['All'] + entities)

# Filtered Data
df_year = df.copy()
if selected_year != 'All':
    df_year = df_year[df_year['Year'] == selected_year]
if selected_entity != 'All':
    df_year = df_year[df_year['Entity'] == selected_entity]

# Tabs
tabs = st.tabs(["Overview KPIs", "Renewable Energy Insights", "Electricity Access Insights", "CO2 Emissions Map", "Correlation Heatmap"])

# --- Tab 1: Overview KPIs ---
with tabs[0]:
    st.header("📌 Business KPIs Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Access to Electricity", f"{df_year['Access_to_electricity_of_population'].mean():.2f}%")
    with col2:
        st.metric("Average Renewable Share", f"{df_year['Renewable_energy_share_in_the_total_final_energy_consumption'].mean():.2f}%")
    with col3:
        st.metric("Total CO₂ Emissions", f"{df_year['Value_co2_emissions_kt_by_country'].sum() / 1e3:.2f}M kt")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Average GDP per Capita", f"${df_year['gdp_per_capita'].mean():,.0f}")
    with col5:
        st.metric("Average Energy Intensity", f"{df_year['Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP'].mean():.2f} MJ/$")
    with col6:
        total_countries = df_year['Entity'].nunique()
        st.metric("Total Countries", f"{total_countries}")
    col7, col8, col9 = st.columns(3)
    with col7:
        st.metric("Average Renewable Capacity Per Capita", f"{df_year['Renewable_electricity_generating_capacity_per_capita'].mean():.2f}")
    with col8:
        st.metric("Average GDP Growth", f"{df_year['gdp_growth'].mean():.2f}%")
    with col9:
        st.metric("Average Land Area", f"{df_year['Land_Area_Km2'].mean():,.0f} Km²")

# --- Tab 2: Renewable Energy Insights ---
with tabs[1]:
    st.header("♻️ Renewable Energy Insights")

    renewable_sum = df.groupby('Entity')['Renewable_energy_share_in_the_total_final_energy_consumption'].sum().reset_index()
    renewable_sum = renewable_sum.dropna(subset=['Renewable_energy_share_in_the_total_final_energy_consumption'])
    top_5 = renewable_sum.sort_values(by='Renewable_energy_share_in_the_total_final_energy_consumption', ascending=False).head(5)
    bottom_5 = renewable_sum.sort_values(by='Renewable_energy_share_in_the_total_final_energy_consumption', ascending=True).head(5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Countries by Renewable Energy Share (Total Sum)")
        fig_top = px.bar(top_5, x='Entity', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity',
                         labels={"Entity": "Country", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"},
                         text_auto='.2s')
        fig_top.update_layout(xaxis_title="Country", yaxis_title="Renewable Share (%)")
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        st.subheader("Bottom 5 Countries by Renewable Energy Share (Total Sum)")
        fig_bottom = px.bar(bottom_5, x='Entity', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity',
                            labels={"Entity": "Country", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"},
                            text_auto='.2s')
        fig_bottom.update_layout(xaxis_title="Country", yaxis_title="Renewable Share (%)")
        st.plotly_chart(fig_bottom, use_container_width=True)

    st.subheader("📈 Renewable Energy Share Trend (Bottom 5 Countries)")
    bottom_entities = bottom_5['Entity'].tolist()
    trend_data = df[df['Entity'].isin(bottom_entities)]
    fig_area = px.area(trend_data, x='Year', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity',
                       labels={"Entity": "Country", "Year": "Year", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"})
    fig_area.update_layout(xaxis_title="Year", yaxis_title="Renewable Share (%)")
    st.plotly_chart(fig_area, use_container_width=True)

    st.subheader("Renewable Energy Share Trend (Top 5 Countries)")
    top_entities = top_5['Entity'].tolist()
    trend_data_top = df[df['Entity'].isin(top_entities)]
    fig_area_top = px.area(trend_data_top, x='Year', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity',
                           labels={"Entity": "Country", "Year": "Year", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"})
    fig_area_top.update_layout(xaxis_title="Year", yaxis_title="Renewable Share (%)")
    st.plotly_chart(fig_area_top, use_container_width=True)

# --- Tab 3: Electricity Access Insights ---
with tabs[2]:
    st.header("🔌 Electricity Access Insights")

    st.subheader("Global Access to Electricity Over Years")
    if 'Year' in df.columns:
        access_trend = df.groupby('Year')['Access_to_electricity_of_population'].mean().reset_index()
        fig_line = px.line(access_trend, x='Year', y='Access_to_electricity_of_population',
                           labels={"Access_to_electricity_of_population": "Access to Electricity (%)"})
        fig_line.update_traces(mode='lines+markers+text', text=access_trend['Access_to_electricity_of_population'].round(1), textposition='top center')
        fig_line.update_layout(xaxis_title="Year", yaxis_title="Access to Electricity (%)")
        st.plotly_chart(fig_line, use_container_width=True)

    access_avg = df.groupby('Entity')['Access_to_electricity_of_population'].mean().reset_index()
    access_avg = access_avg.dropna(subset=['Access_to_electricity_of_population'])
    top_5_access = access_avg.sort_values(by='Access_to_electricity_of_population', ascending=False).head(5)
    bottom_5_access = access_avg.sort_values(by='Access_to_electricity_of_population', ascending=True).head(5)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Top 5 Countries by Average Electricity Access")
        fig_top_access = px.bar(top_5_access, x='Entity', y='Access_to_electricity_of_population', color='Entity',
                                labels={"Entity": "Country", "Access_to_electricity_of_population": "Electricity Access (%)"},
                                text_auto='.2s')
        fig_top_access.update_layout(xaxis_title="Country", yaxis_title="Electricity Access (%)")
        st.plotly_chart(fig_top_access, use_container_width=True)

    with col4:
        st.subheader("Bottom 5 Countries by Average Electricity Access")
        fig_bottom_access = px.bar(bottom_5_access, x='Entity', y='Access_to_electricity_of_population', color='Entity',
                                   labels={"Entity": "Country", "Access_to_electricity_of_population": "Electricity Access (%)"},
                                   text_auto='.2s')
        fig_bottom_access.update_layout(xaxis_title="Country", yaxis_title="Electricity Access (%)")
        st.plotly_chart(fig_bottom_access, use_container_width=True)

# --- Tab 4: CO2 Emissions Map ---
with tabs[3]:
    st.header("🌎 CO₂ Emissions by Country")
    df_year['Value_co2_emissions_kt_by_country'] = df_year['Value_co2_emissions_kt_by_country'].fillna(0)
    fig_map = px.scatter_geo(
        df_year,
        locations="Entity",
        locationmode="country names",
        size="Value_co2_emissions_kt_by_country",
        projection="natural earth",
        title="CO₂ Emissions (kt) by Country",
        size_max=50,
        color="Value_co2_emissions_kt_by_country",
        color_continuous_scale="Reds",
        labels={"Entity": "Country", "Value_co2_emissions_kt_by_country": "CO₂ Emissions (kt)"}
    )
    fig_map.update_layout(title_x=0.5)
    st.plotly_chart(fig_map, use_container_width=True)

# --- Tab 5: Correlation Heatmap ---
with tabs[4]:
    st.header("🧠 Correlation Heatmap")
    numeric_cols = df_year.select_dtypes(include=['float64', 'int64']).columns
    corr = df_year[numeric_cols].corr()
    fig_corr, ax_corr = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, cmap='coolwarm', annot=True, fmt=".2f", ax=ax_corr)
    ax_corr.set_title("Correlation between Energy & Economic Indicators", fontsize=16)
    st.pyplot(fig_corr)
