import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Global Energy Insights", layout="wide")
st.title("🌍 Global Energy Data Visualization")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.write("### Data Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # Top 10 Countries by Access to Electricity
    st.subheader("🔌 Top 10 Countries by Access to Electricity")
    top_electricity = df.groupby("Entity")["Access_to_electricity_of_population"].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots()
    top_electricity.plot(kind="bar", color="skyblue", ax=ax1)
    ax1.set_ylabel("% Population with Access")
    ax1.set_title("Top 10 Countries by Access to Electricity")
    st.pyplot(fig1)

    st.markdown("---")

    # Top 5 Countries by GDP Growth vs GDP per Capita (Side-by-Side Bars)
    st.subheader("📊 Top 5 Countries: GDP Growth vs GDP per Capita")

    top5 = df.groupby('Entity').agg({
        'gdp_growth': 'mean',
        'gdp_per_capita': 'mean'
    }).sort_values('gdp_per_capita', ascending=False).head(5).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.35
    x = range(len(top5))

    ax.bar([i - bar_width/2 for i in x], top5['gdp_growth'], width=bar_width, label='GDP Growth', color='#00bfc4')
    ax.bar([i + bar_width/2 for i in x], top5['gdp_per_capita'], width=bar_width, label='GDP per Capita', color='#f8766d')

    ax.set_xlabel('Country')
    ax.set_ylabel('Value')
    ax.set_title('Top 5 Countries: GDP Growth vs GDP per Capita')
    ax.set_xticks(x)
    ax.set_xticklabels(top5['Entity'])
    ax.legend()
    st.pyplot(fig)

else:
    st.info("📂 Please upload a CSV file to start analysis.")
