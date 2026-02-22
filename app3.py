# app.py
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Two dataframe", layout="wide")

st.title("Modification History")

# -----------------------------
# 1) Data generation
# -----------------------------
@st.cache_data
def make_data(seed: int = 42) -> pd.DataFrame:
    n_cols = np.random.randint(4,6)
    n_rows = np.random.randint(20,50)
    np.random.random((n_rows, n_cols))
    return pd.DataFrame(data = np.random.random((n_rows, n_cols)),
                        columns = [f"column_{i}" for i in range(n_cols)])

df = make_data()

# -----------------------------
# 2) Layout (4 columns)
# -----------------------------
# Column width control: col1/col3 narrow, col2/col4 wide
# relative widths: [0.6, 1.4, 0.6, 1.4]
col1, col2 = st.columns([1, 1], gap="large")

# Column 1
with col1:
    st.subheader("Fab 1")
    st.caption(f"update time: {datetime.now()}")
    st.dataframe(make_data())

# Column 2
with col2:
    st.subheader("Fab 2")
    st.caption(f"update time: {datetime.now()}")
    st.dataframe(make_data())