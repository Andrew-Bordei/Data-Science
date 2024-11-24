import streamlit as st
import numpy as np
import polars as pl
import plotly.express as px 
import os 
import sys

# Manually add path to read from another folder 
path2add = os.path.normpath(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir, "utils"))
)
if not (path2add in sys.path):
    sys.path.append(path2add)

import preprocessing
models = {"Cosine Similarity", "Neural Net"}

model_accuracy = pl.read_csv("../data/model_accuracy.csv",ignore_errors=True)
df = pl.read_csv("../data/google_analytics_data.csv",ignore_errors=True)
encoded_df = pl.read_csv("../data/encoded_df.csv",ignore_errors=True)

names = ["Average Accuracy","Selected User Accuracy"]
names = pl.DataFrame({"Data":names})

model_accuracy=model_accuracy.mean()

df = df.with_columns(pl.col("fullVisitorId").cast(str))
purchasing_users=df.filter(pl.col('transactionId') != "null").select(pl.col('fullVisitorId')).unique()
purchasing_users=purchasing_users.filter(pl.col('fullVisitorId') != "None")
user_profiles = preprocessing.user_profiles(encoded_df)

st.title("Ecommerce Recommender")
st.subheader("An App by Andrew Bordei")
st.write("This app provides purchase recommendations to users. The data is real traffic from the "
         "Google merchandise store website. An SQL query was used to acquire the dataset.")

left_column, right_column = st.columns(2)
with left_column:
    "Select a user to recommend products to:"
    user_selected = st.selectbox(options=purchasing_users, label="User ID's")
    
with right_column:
    "Recommendations!"
    recommendations = preprocessing.recommendation_pipeline(user_selected, user_profiles,
                                                            encoded_df,df)
    st.dataframe(recommendations,width=200,column_config={"value":"Recommendations"})

model_eval = preprocessing.recommendation_eval_pipeline(user_selected, user_profiles,
                                                        encoded_df,df)

model_accuracy=model_accuracy.with_columns(model_eval)
model_accuracy=model_accuracy.transpose()
names = names.with_columns(model_accuracy)
names = names.rename({"column_0":"Accuracy"})
visitors_px = px.bar(names, x='Data',y='Accuracy', title="Recommendation Accuracy")
st.plotly_chart(visitors_px)
    