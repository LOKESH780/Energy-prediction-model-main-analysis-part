import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Energy Data Analysis", layout="wide")
st.title("📊 Global Energy Analysis Dashboard")

# Upload dataset
uploaded_file = st.file_uploader("Upload CSV file for analysis", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data loaded successfully!")
    
    st.write("### Raw Data Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # KPIs Section
    st.header("🌟 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        avg_access = df["Access_to_electricity_of_population"].mean()
        st.metric("Average Access to Electricity", f"{avg_access:.2f}")

    with col2:
        avg_renewable = df["Renewable_share_energy_consumption"].mean()
        st.metric("Average Renewable Share", f"{avg_renewable:.2f}")

    with col3:
        total_co2 = df["Co2_emissions_Mt"].sum()
        st.metric("Total CO₂ Emissions", f"{total_co2/1e6:.2f}M")  # Dividing by 1 million for 'M'

    with col4:
        avg_gdp = df["gdp_per_capita"].mean()
        st.metric("Average GDP per Capita", f"{avg_gdp/1000:.2f}K")  # Showing in 'K'

    with col5:
        avg_energy_intensity = df["Energy_intensity_level_primary_energy_MJ_per_2017PPP_GDP"].mean()
        st.metric("Average Energy Intensity", f"{avg_energy_intensity:.2f}")

    with col6:
        total_countries = df["Country"].nunique()
        st.metric("Total Countries", total_countries)

    st.markdown("---")

    # Bar chart: gdp growth vs gdp per capita
    st.header("📈 GDP Growth vs GDP per Capita (Top 5 Countries)")
    
    # Group and calculate sum
    gdp_df = df.groupby("Country")[["gdp_growth", "gdp_per_capita"]].sum().reset_index()
    top5_countries = gdp_df.sort_values(by="gdp_per_capita", ascending=False).head(5)

    fig, ax = plt.subplots(figsize=(10,6))
    bar_width = 0.35
    x = range(len(top5_countries))

    ax.bar(x, top5_countries["gdp_growth"], width=bar_width, label="GDP Growth", color="lightblue")
    ax.bar([i + bar_width for i in x], top5_countries["gdp_per_capita"], width=bar_width, label="GDP per Capita", color="black")

    ax.set_xlabel("Country")
    ax.set_ylabel("Value")
    ax.set_title("GDP Growth vs GDP per Capita (Top 5 countries)")
    ax.set_xticks([i + bar_width / 2 for i in x])
    ax.set_xticklabels(top5_countries["Country"])
    ax.legend()

    st.pyplot(fig)

else:
    st.info("📂 Please upload a CSV file to start the analysis.")
