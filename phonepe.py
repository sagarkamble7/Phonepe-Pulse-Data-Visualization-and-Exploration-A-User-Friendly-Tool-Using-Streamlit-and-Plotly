import streamlit as st
from streamlit_option_menu import option_menu

# # st.set_page_config(page_title= 'phonepe', layout= 'wide', page_icon= "P")
st.title("PHONEPE PULSE")

with st.sidebar:
    option = st.selectbox("SELECT",("Aggregate", "map", "top"))
    st.write("You Selected", option)

    year = st.selectbox("select the year",(2018, 2019, 2020, 2021, 2022, 2023))
    quarter = st.selectbox("select the quarter",("Q1", "Q2", "Q3", "Q4"))


