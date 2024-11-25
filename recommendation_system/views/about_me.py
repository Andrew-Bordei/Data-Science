import streamlit as st 

@st.dialog("Contact Me")
def contact_form():
    st.write("Email: andrewcbordei@yahoo.com")
    st.page_link("https://www.linkedin.com/in/andrew-bordei-80448813b/", label="LinkedIn")
    st.page_link("https://github.com/Andrew-Bordei", label="Github")
    st.page_link("https://www.kaggle.com/andrewbordei", label="Kaggle")
    st.page_link("https://medium.com/@andrewbordei07", label="Medium")

left_column, right_column = st.columns(2)
with left_column:
    st.image("./assets/LinkedIn_profile_pic_cropped.png",width=300)

with right_column:
    st.title("Andrew Bordei")
    st.write(
        """
        University of London computer science student, passionate about applying data science to provide business solutions.
        """
    )
    st.write("\n")
    if st.button("Contact Me"):
        contact_form()

st.write("\n")
st.subheader("Projects")
st.write(
    """
    ****WTI Crude Oil Price Forecast****
    -  Collected 14 datasets via the Federal Reserve's API corresponding to supply, demand, and economic categories to train
    machine learning models’ to forecast daily prices of crude oil.
    - Performed feature engineering by aggregating oil production data to increase model
    accuracy by 5%.
    - Discovered the US Dollar(56%) and world oil consumption(28%) were the most important
    features for the XGBRegressor model.

    ****Inflation Forecasting****
    - Collected 7 economic datasets via an API in monthly frequency from 1975-2024 to forecast inflation using machine learning.
    - Trained 3 different models (Decision Tree, Random Forest, SVR) and used RMSE to
    determine that the Support Vector Regression(SVR) model had the most accurate forecast.
    - Cleaned and analyzed the datasets which revealed all data was non-normally distributed
    with tail occurrences happening relatively frequently.
    - Discovered the model was more accurate when filling missing values in the dataset with
    their respective averages due to having more data for training.
    """
)

st.write("\n")
st.subheader("Skills")
st.write(
    """
    - Programming: Python, JavaScript, C++, HTML, CSS
    - Machine Learning: Linear & Logistic Regression, Decision Trees, Random Forest, Support Vector Machines
    - Databases: SQL, MySQL
    - Libraries: Scikit-learn, Pandas, Polars, NumPy, Plotly, Matplotlib 
    """
)

