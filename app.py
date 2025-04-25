import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page settings
st.set_page_config(page_title="Global Energy Analysis", layout="wide")
st.title("🌍 Global Energy Dashboard")

# Upload dataset
uploaded_file = st.file_uploader("📂 Upload the CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data loaded successfully!")
    st.write("### 📋 Data Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # KPI Section
    st.header("📈 Key Metrics Overview")
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        avg_access = df["Access_to_electricity_of_population"].mean()
        st.metric("Average Access to Electricity (%)", f"{avg_access:.2f}")

    with col2:
        avg_renewable_share = df["Renewable_energy_share_in_the_total_final_energy_consumption"].mean()
        st.metric("Average Renewable Share (%)", f"{avg_renewable_share:.2f}")

    with col3:
        total_co2 = df["Value_co2_emissions_kt_by_country"].sum() / 1e6  # in millions
        st.metric("Total CO₂ Emissions", f"{total_co2:.2f}M")

    with col4:
        avg_gdp_capita = df["gdp_per_capita"].mean()
        st.metric("Average GDP per Capita ($)", f"{avg_gdp_capita:,.2f}")

    with col5:
        avg_energy_intensity = df["Energy_intensity_level_of_primary_energy_MJ_2017_PPP_GDP"].mean()
        st.metric("Average Energy Intensity", f"{avg_energy_intensity:.2f}")

    with col6:
        total_countries = df["Entity"].nunique()
        st.metric("Total Countries", total_countries)

    st.markdown("---")

    # Bar Chart: Top 5 Countries by GDP per Capita and GDP Growth
    st.subheader("📊 Top 5 Countries: GDP Growth vs GDP per Capita")

    top5 = df.groupby('Entity').agg({
        'gdp_growth': 'mean',
        'gdp_per_capita': 'mean'
    }).sort_values('gdp_per_capita', ascending=False).head(5).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(top5['Entity'], top5['gdp_per_capita'], label='GDP per Capita', color='#1f77b4')
    ax.bar(top5['Entity'], top5['gdp_growth'], label='GDP Growth', color='#ff7f0e', alpha=0.7)
    ax.set_ylabel("Value")
    ax.set_title("GDP per Capita and GDP Growth (Top 5 Countries)")
    ax.legend()
    st.pyplot(fig)

else:
    st.info("👆 Please upload a CSV file to start analysis.")
