# app.py
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Streamlit Dashboard Demo", layout="wide")

st.title("Streamlit Dashboard (Slider + Dropdown)")

# -----------------------------
# 1) Data generation
# -----------------------------
@st.cache_data
def make_data(seed: int = 42, n_days: int = 180, groups=("A", "B", "C", "D")) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=n_days, freq="D")

    rows = []
    for g in groups:
        base = {"A": 100, "B": 120, "C": 90, "D": 110}[g]
        trend = {"A": 0.05, "B": -0.02, "C": 0.03, "D": 0.00}[g]
        season = 5 * np.sin(np.linspace(0, 4 * np.pi, n_days) + rng.uniform(0, 2*np.pi))
        noise = rng.normal(0, 1.0, size=n_days)  # base noise (will be scaled by slider)

        value = base + trend * np.arange(n_days) + season + noise
        rows.append(pd.DataFrame({"date": dates, "group": g, "value": value}))

    df = pd.concat(rows, ignore_index=True)
    return df

df = make_data()

# -----------------------------
# 2) Layout with containers
# -----------------------------

# Top row: two logical panels (Left: col1+col2, Right: col3+col4)
left_panel, right_panel = st.columns([2.0, 2.0], gap="large")

with left_panel:
    with st.container(border=True):
        st.subheader("Panel A: Slider + Plot")

        # Column width control inside left panel
        col1, col2 = st.columns([0.6, 1.4], gap="large")

        # Column 1: Slider
        with col1:
            st.subheader("Slider 1")
            noise_scale = st.slider(
                "Noise scale (plot variability)",
                min_value=0.0,
                max_value=5.0,
                value=1.0,
                step=0.1,
            )
            ma_window = st.slider(
                "Moving average window",
                min_value=3,
                max_value=30,
                value=7,
                step=1,
            )
            st.caption("Slider 1이 Column 2의 plot 변동성을 바꿉니다.")

        # Column 2: Plot controlled by slider
        with col2:
            st.subheader("Plot controlled by Slider 1")

            # aggregate across groups to show a single time series
            daily = df.groupby("date", as_index=False)["value"].mean()

            # add adjustable noise to visualize slider effect (not changing underlying cached df)
            rng = np.random.default_rng(123)
            adj = daily.copy()
            adj["value_adj"] = adj["value"] + rng.normal(0, noise_scale, size=len(adj))

            adj["ma"] = adj["value_adj"].rolling(ma_window, min_periods=1).mean()

            fig, ax = plt.subplots()
            ax.plot(adj["date"], adj["value_adj"], label="Daily mean (adjusted)")
            ax.plot(adj["date"], adj["ma"], label=f"MA({ma_window})")
            ax.set_xlabel("Date")
            ax.set_ylabel("Value")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig, clear_figure=True)

with right_panel:
    with st.container(border=True):
        st.subheader("Panel B: Dropdown + Plot")

        # Column width control inside right panel
        col3, col4 = st.columns([0.6, 1.4], gap="large")

        # Column 3: Dropdown
        with col3:
            st.subheader("Dropdown 1")
            group = st.selectbox("Select group", sorted(df["group"].unique()))
            st.caption("Dropdown 1이 Column 4의 plot(분포)을 바꿉니다.")

        # Column 4: Plot controlled by dropdown
        with col4:
            st.subheader("Plot controlled by Dropdown 1")

            sub = df[df["group"] == group].copy()

            fig2, ax2 = plt.subplots()
            ax2.hist(sub["value"], bins=20)
            ax2.set_xlabel("Value")
            ax2.set_ylabel("Count")
            ax2.set_title(f"Distribution for Group {group}")
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2, clear_figure=True)

st.divider()
st.write("Sample data preview")
st.dataframe(df.head(20), use_container_width=True)
