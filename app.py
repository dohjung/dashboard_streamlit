import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data, create our data frame for Country, year (sorted), Ladder score
url = 'https://raw.githubusercontent.com/loewenj700/global_happiness/main/WHR2024.csv'
df = pd.read_csv(url)
df = df[["Country name", "Year", "Ladder score"]].dropna()
df["Year"] = df["Year"].astype(int)
df = df.sort_values("Year")

# Sidebar: Country dropdown menu sorted alphabetically
country_list = sorted(df["Country name"].unique())
selected_country = st.sidebar.selectbox("Select a Country (A–Z):", country_list)
country_df = df[df["Country name"] == selected_country]

# Line chart of Ladder Score over time
st.subheader(f"Happiness Score Over Time: {selected_country}")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(country_df["Year"], country_df["Ladder score"], marker='o', linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Ladder Score")
ax.set_title(f"{selected_country}: Happiness Score by Year")
st.pyplot(fig)