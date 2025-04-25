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
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.markdown("---")

    # Line chart for energy trend
    st.subheader("📈 Energy Consumption Over Years")
    if 'Year' in df.columns:
        energy_trend = df.groupby('Year')["Primary_energy_consumption_per_capita_kWh_person"].mean().reset_index()
        st.line_chart(energy_trend.rename(columns={"Primary_energy_consumption_per_capita_kWh_person": "Avg. Energy"}))
    else:
        st.warning("⚠️ 'Year' column not found in dataset.")

    # GDP vs Energy Scatter Plot
    st.subheader("💡 GDP vs Energy Consumption")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(
        data=df,
        x="gdp_per_capita",
        y="Primary_energy_consumption_per_capita_kWh_person",
        hue="Access_to_electricity_of_population",
        palette="viridis",
        ax=ax2
    )
    ax2.set_xlabel("GDP per Capita")
    ax2.set_ylabel("Energy Consumption per Capita")
    st.pyplot(fig2)

else:
    st.info("📂 Please upload a CSV file to start the analysis.")
