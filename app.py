import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from login import login

st.set_page_config(page_title="Energy Data Deep Dive", layout="wide")

# === Login Logic ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# === Logout Button on Top-Right ===
col1, col2, col3 = st.columns([6, 1, 1])
with col3:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

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
tabs = st.tabs(["Overview KPIs", "Renewable Energy Insights", "Electricity Access Insights", "CO2 Emissions Map", "Correlation Heatmap","Energy Mix & Comparisons"])

# --- Tab 1: Overview KPIs ---
with tabs[0]:
    st.header("📌 Business KPIs Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Access to Electricity", f"{df_year['Access_to_electricity_of_population'].mean():.2f}%")
    with col2:
        st.metric("Total Renewable Share", f"{df_year['Renewable_energy_share_in_the_total_final_energy_consumption'].sum():.2f}%")
    with col3:
        st.metric("Total CO₂ Emissions", f"{df_year['Value_co2_emissions_kt_by_country'].sum() / 1e3:.2f}M kt")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Total GDP per Capita", f"${df_year['gdp_per_capita'].sum():,.0f}")
    with col5:
        st.metric("Total Energy Intensity", f"{df_year['Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP'].sum():.2f} MJ/$")
    with col6:
        total_countries = df_year['Entity'].nunique()
        st.metric("Total Countries", f"{total_countries}")
    col7, col8, col9 = st.columns(3)
    with col7:
        st.metric("Total Renewable Capacity Per Capita", f"{df_year['Renewable_electricity_generating_capacity_per_capita'].sum():.2f}")
    with col8:
        st.metric("Average GDP Growth", f"{df_year['gdp_growth'].mean():.2f}%")
    with col9:
        st.metric("Average Land Area", f"{df_year['Land_Area_Km2'].mean():,.0f} Km²")

# --- Tab 2: Renewable Energy Insights ---
with tabs[1]:
    st.header("♻️ Renewable Energy Insights")

    renewable_sum = df.groupby('Entity')['Renewable_energy_share_in_the_total_final_energy_consumption'].sum().reset_index()
    renewable_sum = renewable_sum.dropna()
    top_5 = renewable_sum.sort_values(by='Renewable_energy_share_in_the_total_final_energy_consumption', ascending=False).head(5)
    bottom_5 = renewable_sum.sort_values(by='Renewable_energy_share_in_the_total_final_energy_consumption', ascending=True).head(5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Countries by Renewable Energy Share")
        fig_top = px.bar(top_5, x='Entity', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity', text_auto='.2s',
                         labels={"Entity": "Country", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"})
        fig_top.update_traces(textposition='outside')
        st.plotly_chart(fig_top, use_container_width=True)
    with col2:
        st.subheader("Bottom 5 Countries by Renewable Energy Share")
        fig_bottom = px.bar(bottom_5, x='Entity', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity', text_auto='.2s',
                            labels={"Entity": "Country", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"})
        fig_bottom.update_traces(textposition='outside')
        st.plotly_chart(fig_bottom, use_container_width=True)

    st.subheader("Trend of Renewable Energy Share (Bottom 5)")
    fig_area = px.area(df[df['Entity'].isin(bottom_5['Entity'])], x='Year', y='Renewable_energy_share_in_the_total_final_energy_consumption',
                       color='Entity', labels={"Year": "Year", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"})
    st.plotly_chart(fig_area, use_container_width=True)

    st.subheader("Trend of Renewable Energy Share (Top 5)")
    fig_area_top = px.area(df[df['Entity'].isin(top_5['Entity'])], x='Year', y='Renewable_energy_share_in_the_total_final_energy_consumption',
                           color='Entity', labels={"Year": "Year", "Renewable_energy_share_in_the_total_final_energy_consumption": "Renewable Share (%)"})
    st.plotly_chart(fig_area_top, use_container_width=True)

    # Additional - Average Renewable Share by Region (if available)
    st.subheader("Overall Average Renewable Share Distribution")
    fig_hist = px.histogram(df, x='Renewable_energy_share_in_the_total_final_energy_consumption', nbins=50,
                            labels={'Renewable_energy_share_in_the_total_final_energy_consumption': 'Renewable Share (%)'})
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Tab 3: Electricity Access Insights ---
with tabs[2]:
    st.header("🔌 Electricity Access Insights")

    # Preparing data for Global Access Trend
    access_trend = df.groupby('Year')['Access_to_electricity_of_population'].sum().reset_index()
    
    st.subheader("Global Average Access to Electricity Over Time")
    fig_line = px.line(
        access_trend,
        x='Year',
        y='Access_to_electricity_of_population',
        text=access_trend['Access_to_electricity_of_population'].apply(lambda x: f"{x:.2f}"),  # <-- Adding data labels
        labels={
            "Year": "Year",
            "Access_to_electricity_of_population": "Access to Electricity (%)"
        }
    )
    fig_line.update_traces(textposition="top center")  # <-- Setting the position of the labels
    st.plotly_chart(fig_line, use_container_width=True)

    access_total = df.groupby('Entity')['Access_to_electricity_of_population'].sum().reset_index()
    top_5_access = access_avg.sort_values(by='Access_to_electricity_of_population', ascending=False).head(5)
    bottom_5_access = access_avg.sort_values(by='Access_to_electricity_of_population', ascending=True).head(5)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Top 5 Countries by Electricity Access")
        fig_top_access = px.bar(top_5_access, x='Entity', y='Access_to_electricity_of_population', color='Entity', text_auto='.2s',
                                labels={"Entity": "Country", "Access_to_electricity_of_population": "Electricity Access (%)"})
        fig_top_access.update_traces(textposition='outside')
        st.plotly_chart(fig_top_access, use_container_width=True)

    with col4:
        st.subheader("Bottom 5 Countries by Electricity Access")
        fig_bottom_access = px.bar(bottom_5_access, x='Entity', y='Access_to_electricity_of_population', color='Entity', text_auto='.2s',
                                   labels={"Entity": "Country", "Access_to_electricity_of_population": "Electricity Access (%)"})
        fig_bottom_access.update_traces(textposition='outside')
        st.plotly_chart(fig_bottom_access, use_container_width=True)

    # Additional - Electricity Access Distribution
    st.subheader("Electricity Access Distribution Across Countries")
    fig_dist = px.histogram(df, x='Access_to_electricity_of_population', nbins=50,
                            labels={"Access_to_electricity_of_population": "Access to Electricity (%)"})
    st.plotly_chart(fig_dist, use_container_width=True)

# --- Tab 4: CO2 Emissions Map ---
with tabs[3]:
    st.header("🌎 CO₂ Emissions by Country")

    df_year['Value_co2_emissions_kt_by_country'] = df_year['Value_co2_emissions_kt_by_country'].fillna(0)

    st.subheader("World Map - CO₂ Emissions Size and Color")
    fig_map = px.scatter_geo(df_year, locations="Entity", locationmode="country names", size="Value_co2_emissions_kt_by_country",
                             projection="natural earth", color="Value_co2_emissions_kt_by_country",
                             color_continuous_scale="Reds", size_max=50,
                             labels={"Entity": "Country", "Value_co2_emissions_kt_by_country": "CO₂ Emissions (kt)"})
    st.plotly_chart(fig_map, use_container_width=True)

    # Additional - Top CO2 Emitters
    st.subheader("Top 10 CO₂ Emitting Countries")
    top_emitters = df_year.groupby('Entity')['Value_co2_emissions_kt_by_country'].sum().reset_index()
    top_emitters = top_emitters.sort_values('Value_co2_emissions_kt_by_country', ascending=False).head(10)

    fig_top_emitters = px.bar(top_emitters, x='Entity', y='Value_co2_emissions_kt_by_country', color='Entity', text_auto='.2s',
                              labels={'Entity': 'Country', 'Value_co2_emissions_kt_by_country': 'CO₂ Emissions (kt)'})
    fig_top_emitters.update_traces(textposition='outside')
    st.plotly_chart(fig_top_emitters, use_container_width=True)

# --- Tab 5: Correlation Heatmap ---
with tabs[4]:
    st.header("🧠 Correlation Heatmap")
    numeric_cols = df_year.select_dtypes(include=['float64', 'int64']).columns
    corr = df_year[numeric_cols].corr()
    fig_corr, ax_corr = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, cmap='coolwarm', annot=True, fmt='.2f', ax=ax_corr)
    st.pyplot(fig_corr)

# === Tab 6: Energy Mix & Comparisons ===
# === Tab 6: Energy Mix & Comparisons ===
with tabs[5]:
    st.header("🔄 Energy Mix & Comparative Visualizations")

    # Pie Chart: Electricity Source Mix
    st.subheader("⚡ Electricity Source Mix")
    mix = df_year[['Electricity_from_fossil_fuels_TWh', 'Electricity_from_nuclear_TWh', 'Electricity_from_renewables_TWh']].sum()
    fig_pie = px.pie(
        names=mix.index,
        values=mix.values,
        hole=0.4,
        title="Total Electricity Production by Source",
    )
    fig_pie.update_traces(textinfo='label+percent', pull=[0.05, 0, 0], textfont_size=14)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Donut Chart: Fossil vs Low-Carbon
    st.subheader("🌀 Fossil vs Low-Carbon Electricity")
    low_carbon = df_year['Low_carbon_electricity_electricity'].mean()
    donut_df = pd.DataFrame({
        "Source": ["Fossil Fuels", "Low Carbon"],
        "Share": [100 - low_carbon, low_carbon]
    })
    fig_donut = px.pie(
        donut_df,
        names="Source",
        values="Share",
        hole=0.5,
        title="Average Electricity Type Share (%)"
    )
    fig_donut.update_traces(textinfo='label+percent', textfont_size=14)
    st.plotly_chart(fig_donut, use_container_width=True)

    # Line Chart: GDP vs Access to Electricity
    st.subheader("📈 GDP vs Electricity Access Over Time")
    gdp_trend = df.groupby("Year")[["gdp_per_capita", "Access_to_electricity_of_population"]].mean().reset_index()
    fig_line2 = px.line(
        gdp_trend,
        x="Year",
        y=["gdp_per_capita", "Access_to_electricity_of_population"],
        markers=True,
        labels={"value": "Metric Value", "variable": "Indicator"}
    )
    st.plotly_chart(fig_line2, use_container_width=True)

    # Treemap: CO2 Emissions
    st.subheader("🌍 CO₂ Emissions Treemap by Country")
    treemap = df_year.groupby("Entity")["Value_co2_emissions_kt_by_country"].sum().reset_index()
    treemap = treemap[treemap["Value_co2_emissions_kt_by_country"] > 0]
    fig_tree = px.treemap(
        treemap,
        path=["Entity"],
        values="Value_co2_emissions_kt_by_country",
        color="Value_co2_emissions_kt_by_country",
        color_continuous_scale="Reds",
        title="Total CO₂ Emissions by Country"
    )
    st.plotly_chart(fig_tree, use_container_width=True)
