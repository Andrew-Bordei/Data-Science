import streamlit as st
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
import preprocessing
# from main import recommendations, model_eval
models = {"Cosine Similarity", "Neural Net"}


# df = pl.read_csv("../data/purchasing_visitors.csv",ignore_errors=True)
# data_df = pl.read_csv("../data/cleaned_google_analytics.csv",ignore_errors=True)
# rec_df = pl.read_csv("../data/recommendations.csv",ignore_errors=True)
model_accuracy = pl.read_csv("../data/model_accuracy.csv",ignore_errors=True)

df = pl.read_csv("./raw_data.csv",ignore_errors=True)
df = df.with_columns(pl.col("fullVisitorId").cast(str))

df = df.filter(~pl.col('v2ProductCategory').str.contains('origCatName'))
encoded_df = preprocessing.target_encoding(df)

purchasing_users=encoded_df.filter(pl.col('transactionId') != 0).select(pl.col('fullVisitorId')).unique()

user_profiles = encoded_df.group_by(pl.col('fullVisitorId')).agg(
    pl.col('country'), pl.col('city'), 
    pl.col('browser'),pl.col('operatingSystem'),pl.col('deviceCategory'),
    pl.col('source'),pl.col('transactionId'),pl.col('v2ProductCategory')
)


st.title("Ecommerce Recommender")
st.subheader("An App by Andrew Bordei")
st.write("This app provides purchase recommendations to users. The data is real traffic from the "
         "Google merchandise store website. An SQL query was used to acquire the dataset.")

# left_column, middle_column, right_column = st.columns(3)
left_column, right_column = st.columns(2)
with left_column:
    "Select which model to use: "
    model_selected = st.selectbox(options=models, label="Model")
    
with right_column:
    "Select a user to recommend products to:"
    user_selected = st.selectbox(options=purchasing_users, label="User ID's")
    st.write(user_selected)
    recommendations = preprocessing.recommendation_pipeline(user_selected, user_profiles,
                                                            encoded_df,df)

    model_eval = preprocessing.recommendation_eval_pipeline(user_selected, user_profiles,
                                                            encoded_df,df)

st.write("Recommendations!")
st.dataframe(recommendations)

left_column, right_column = st.columns(2)
with left_column:
    st.write("Model accuracy for selected user: ",f"{np.round(model_eval,2)*100}%")

with right_column:
    st.write("Average model accuracy: ",f"{np.round(model_accuracy.mean().item(),2)*100}%")
    
st.sidebar.selectbox("Contact information??", 0.25)


# st.header("Top 10 Most Sold Categories")
# categories = data_df.filter(pl.col('transactionId') != 'null').select(pl.col('v2ProductCategory'))
# categories = categories.select(pl.col("v2ProductCategory").value_counts(sort=True)).unnest("v2ProductCategory")
# fig, ax = plt.subplots(figsize=(12,8))
# plt.pie(categories['count'][:10],labels=categories['v2ProductCategory'][:10],
#         autopct='%.1f%%',labeldistance=1.1,
#             shadow=True,startangle=60)
# st.pyplot(fig)

    