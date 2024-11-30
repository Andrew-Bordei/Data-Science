import streamlit as st
import polars as pl
import plotly.express as px 
import plotly.graph_objects as go
from utils import preprocessing
import os 

import pandas as pd 

path = os.path.join(os.path.dirname(__file__), "..", "data",)
path2 = os.path.join(os.path.dirname(__file__), "..", "assets",)
model_accuracy = pl.read_csv(path+"/model_accuracy.csv",ignore_errors=True)
df = pl.read_csv(path+"/google_analytics_data.csv",ignore_errors=True)
encoded_df = pl.read_csv(path+"/encoded_df.csv",ignore_errors=True)

names = ["Average Accuracy","Selected User Accuracy"]
names = pl.DataFrame({"Data":names})

model_accuracy=model_accuracy.mean()

df = df.with_columns(pl.col("fullVisitorId").cast(str))
purchasing_users=df.filter(pl.col('transactionId') != "null").select(pl.col('fullVisitorId')).unique()
purchasing_users=purchasing_users.filter(pl.col('fullVisitorId') != "None")
user_profiles = preprocessing.user_profiles(encoded_df)

st.title("Ecommerce Recommender")
st.subheader("An App by Andrew Bordei")
st.write(
    """
    Select a visitor from the Google Merch website below to provide them with purchase recommendations! If you have any questions, 
    contact me on [LinkedIn](https://www.linkedin.com/in/andrew-bordei-80448813b/).
    """
)
st.write("\n")
left_column, right_column = st.columns(2)
with left_column:
    "Select a visitor to recommend products to:"
    st.write("\n")
    st.write("\n")
    user_selected = st.selectbox(options=purchasing_users, label="Visitor ID's")
    
with right_column:
    # "Recommendations!"
    recommendations = preprocessing.recommendation_pipeline(user_selected, user_profiles,encoded_df,df)
    fig = go.Figure(data=[go.Table(header=dict(values=["Recommendations"],line_color='black',fill_color='skyblue',
                                               align='center',
                                               font=dict(color='black', size=14),
                                               height=30),
                                   cells=dict(values=[recommendations],line_color='black',fill_color='lightblue',
                                              align='center',
                                              font=dict(color='black', size=14),
                                              height=30))])
    st.write(fig)
    # st.dataframe(recommendations,width=200,column_config={"value":"Recommendations"})

model_eval = preprocessing.recommendation_eval_pipeline(user_selected, user_profiles,encoded_df,df)

model_accuracy=model_accuracy.with_columns(model_eval)
model_accuracy=model_accuracy.transpose()
names = names.with_columns(model_accuracy)
names = names.rename({"column_0":"Accuracy"})
visitors_px = px.bar(names, x='Data',y='Accuracy', title="Recommendation Accuracy", color='Data')
st.plotly_chart(visitors_px) 
    