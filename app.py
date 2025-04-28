import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_csv('global-data-on-sustainable-energy.csv')

# Set up Streamlit page
st.set_page_config(page_title="Global Energy Insights", layout="wide")
st.title("🌍 Predicting Global Energy Consumption Insights")

# Sidebar for year selection
year = st.sidebar.selectbox('Select Year', sorted(df['Year'].unique()))
df_year = df[df['Year'] == year]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Global Overview", "Renewable Energy Insights", "Electricity Access Insights", "CO₂ Emissions & Energy Intensity"])

# ---------------- Tab 1: Global Overview ----------------
with tab1:
    st.header("🌎 Global Overview")
    
    st.subheader("Total Primary Energy Consumption per Capita (Top 10 Countries)")
    energy_top10 = df_year[['Entity', 'Primary_energy_consumption_per_capita']].dropna()
    energy_top10 = energy_top10.sort_values(by='Primary_energy_consumption_per_capita', ascending=False).head(10)
    
    fig1 = px.bar(energy_top10, x='Entity', y='Primary_energy_consumption_per_capita', color='Entity',
                  labels={'Primary_energy_consumption_per_capita': 'Energy Consumption per Capita (kWh/person)'},
                  title="Top 10 Countries by Primary Energy Consumption per Capita")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Average Energy Intensity by Region")
    intensity = df_year[['Entity', 'Energy_intensity_level_of_primary_energy']].dropna()
    intensity = intensity.groupby('Entity').mean().reset_index()
    fig2 = px.bar(intensity.sort_values(by='Energy_intensity_level_of_primary_energy').head(10),
                  x='Entity', y='Energy_intensity_level_of_primary_energy',
                  labels={'Energy_intensity_level_of_primary_energy': 'Energy Intensity (MJ/$2017 PPP GDP)'},
                  title="Regions with Lowest Energy Intensity")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- Tab 2: Renewable Energy Insights ----------------
with tab2:
    st.header("♻️ Renewable Energy Insights")

    st.subheader("Renewable Energy Share Trend for Top 5 Countries")
    top5_renewables = df_year.sort_values(by='Renewable_energy_share_in_the_total_final_energy_consumption', ascending=False).head(5)['Entity'].tolist()
    df_top5 = df[df['Entity'].isin(top5_renewables)]

    fig3 = px.line(df_top5, x='Year', y='Renewable_energy_share_in_the_total_final_energy_consumption', color='Entity',
                   labels={'Renewable_energy_share_in_the_total_final_energy_consumption': 'Renewable Share (%)'},
                   title="Renewable Energy Share Over Time - Top 5 Countries")
    st.plotly_chart(fig3, use_container_width=True)

    # New - Renewable Capacity vs Renewable Share Scatterplot
    st.subheader("🔍 Renewable Capacity vs Renewable Share")
    scatter_data = df_year.dropna(subset=['Renewable_electricity_generating_capacity_per_capita', 'Renewable_energy_share_in_the_total_final_energy_consumption'])
    fig_scatter = px.scatter(
        scatter_data, 
        x='Renewable_electricity_generating_capacity_per_capita', 
        y='Renewable_energy_share_in_the_total_final_energy_consumption',
        color='Entity',
        size='Renewable_electricity_generating_capacity_per_capita',
        hover_name='Entity',
        labels={
            'Renewable_electricity_generating_capacity_per_capita': 'Renewable Capacity per Capita',
            'Renewable_energy_share_in_the_total_final_energy_consumption': 'Renewable Share (%)'
        },
        title="Renewable Capacity vs Renewable Share"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # New - Top 10 Countries by Renewable Capacity
    st.subheader("🏆 Top 10 Countries by Renewable Electricity Capacity Per Capita")
    top_capacity = df_year[['Entity', 'Renewable_electricity_generating_capacity_per_capita']].dropna()
    top_capacity = top_capacity.groupby('Entity').mean().sort_values(by='Renewable_electricity_generating_capacity_per_capita', ascending=False).head(10).reset_index()
    fig_top_capacity = px.bar(
        top_capacity, 
        x='Entity', 
        y='Renewable_electricity_generating_capacity_per_capita',
        color='Entity',
        labels={'Renewable_electricity_generating_capacity_per_capita': 'Renewable Capacity per Capita'},
        title="Top 10 Countries by Renewable Capacity Per Capita"
    )
    st.plotly_chart(fig_top_capacity, use_container_width=True)

# ---------------- Tab 3: Electricity Access Insights ----------------
with tab3:
    st.header("⚡ Electricity Access Insights")

    st.subheader("Top 10 Countries by Electricity Access (%)")
    top10_access = df_year[['Entity', 'Access_to_electricity_of_population']].dropna()
    top10_access = top10_access.sort_values(by='Access_to_electricity_of_population', ascending=False).head(10)
    fig4 = px.bar(top10_access, x='Entity', y='Access_to_electricity_of_population', color='Entity',
                  labels={'Access_to_electricity_of_population': 'Electricity Access (%)'},
                  title="Top 10 Countries with Highest Electricity Access")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Bottom 5 Countries by Electricity Access (%)")
    bottom5_access = df_year[['Entity', 'Access_to_electricity_of_population']].dropna()
    bottom5_access = bottom5_access.sort_values(by='Access_to_electricity_of_population', ascending=True).head(5)
    fig5 = px.bar(bottom5_access, x='Entity', y='Access_to_electricity_of_population', color='Entity',
                  labels={'Access_to_electricity_of_population': 'Electricity Access (%)'},
                  title="Bottom 5 Countries with Lowest Electricity Access")
    st.plotly_chart(fig5, use_container_width=True)

    # New - Electricity Access vs GDP per Capita
    st.subheader("💹 Electricity Access vs GDP per Capita")
    scatter_gdp = df_year.dropna(subset=['Access_to_electricity_of_population', 'gdp_per_capita'])
    fig_scatter_gdp = px.scatter(
        scatter_gdp, 
        x='gdp_per_capita', 
        y='Access_to_electricity_of_population',
        color='Entity',
        hover_name='Entity',
        size='gdp_per_capita',
        labels={
            'gdp_per_capita': 'GDP per Capita (US$)',
            'Access_to_electricity_of_population': 'Access to Electricity (%)'
        },
        title="Electricity Access vs GDP per Capita"
    )
    st.plotly_chart(fig_scatter_gdp, use_container_width=True)

    # New - Top 10 Countries with Lowest Electricity Access
    st.subheader("🚨 Top 10 Countries with Lowest Electricity Access")
    lowest_access = df_year[['Entity', 'Access_to_electricity_of_population']].dropna()
    lowest_access = lowest_access.groupby('Entity').mean().sort_values(by='Access_to_electricity_of_population', ascending=True).head(10).reset_index()
    fig_lowest_access = px.bar(
        lowest_access, 
        x='Entity', 
        y='Access_to_electricity_of_population',
        color='Entity',
        labels={'Access_to_electricity_of_population': 'Electricity Access (%)'},
        title="Bottom 10 Countries by Electricity Access"
    )
    st.plotly_chart(fig_lowest_access, use_container_width=True)

# ---------------- Tab 4: CO₂ Emissions & Energy Intensity ----------------
with tab4:
    st.header("🌿 CO₂ Emissions and Energy Intensity")

    st.subheader("Top 10 CO₂ Emitting Countries (kt)")
    top10_co2 = df_year[['Entity', 'Value_co2_emissions_kt_by_country']].dropna()
    top10_co2 = top10_co2.sort_values(by='Value_co2_emissions_kt_by_country', ascending=False).head(10)
    fig6 = px.bar(top10_co2, x='Entity', y='Value_co2_emissions_kt_by_country', color='Entity',
                  labels={'Value_co2_emissions_kt_by_country': 'CO₂ Emissions (kt)'},
                  title="Top 10 Countries by CO₂ Emissions")
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Countries with Highest Energy Intensity")
    high_intensity = df_year[['Entity', 'Energy_intensity_level_of_primary_energy']].dropna()
    high_intensity = high_intensity.sort_values(by='Energy_intensity_level_of_primary_energy', ascending=False).head(10)
    fig7 = px.bar(high_intensity, x='Entity', y='Energy_intensity_level_of_primary_energy', color='Entity',
                  labels={'Energy_intensity_level_of_primary_energy': 'Energy Intensity (MJ/$2017 PPP GDP)'},
                  title="Top 10 Countries by Energy Intensity")
    st.plotly_chart(fig7, use_container_width=True)

    # New - CO₂ Emissions vs Renewable Share
    st.subheader("🔍 CO₂ Emissions vs Renewable Share")
    scatter_co2 = df_year.dropna(subset=['Value_co2_emissions_kt_by_country', 'Renewable_energy_share_in_the_total_final_energy_consumption'])
    fig_scatter_co2 = px.scatter(
        scatter_co2, 
        x='Renewable_energy_share_in_the_total_final_energy_consumption', 
        y='Value_co2_emissions_kt_by_country',
        color='Entity',
        hover_name='Entity',
        size='Value_co2_emissions_kt_by_country',
        labels={
            'Renewable_energy_share_in_the_total_final_energy_consumption': 'Renewable Share (%)',
            'Value_co2_emissions_kt_by_country': 'CO₂ Emissions (kt)'
        },
        title="CO₂ Emissions vs Renewable Share"
    )
    st.plotly_chart(fig_scatter_co2, use_container_width=True)
