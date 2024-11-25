import streamlit as st

# Page directory
recommender_page = st.Page(
    page="views/recommender.py",
    title="Recommendation System",
    icon=":material/home:",
    default=True,
)

eda_page = st.Page(
    page="views/eda.py",
    title="Exploratory Data Analysis",
    icon=":material/data_thresholding:",
)

about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
)

# Navigation Menu
page = st.navigation(pages=[recommender_page, eda_page, about_page])

# Run nav
page.run()
