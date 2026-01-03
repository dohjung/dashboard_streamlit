import streamlit as st

st.title("My First Streamlit App")

x = st.slider("Select a number", 0, 100, 50)

st.write("You selected:", x)