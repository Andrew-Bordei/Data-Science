import streamlit as st
import polars as pl
import plotly.express as px 
from utils import preprocessing
import os 

path = os.path.join(os.path.dirname(__file__), "..", "data",)
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
    This app provides purchase recommendations to visitors of the Google Merch website. Recommendations are determined by finding
    the most similar previous purchasing users compared to the current user, then recommending past user purchases to the current user. 
    Similarity among users is determined by Cosine similarity. The data used is real traffic from the 
    Google store, which can be found [here](https://www.kaggle.com/datasets/bigquery/google-analytics-sample/data). 
    The entire code for the app is available on my [GitHub](https://github.com/Andrew-Bordei/Data-Science/tree/main/recommendation_system).
    If you have any questions, contact me on [LinkedIn](https://www.linkedin.com/in/andrew-bordei-80448813b/).
    """
)
st.write("\n")

left_column, right_column = st.columns(2)
with left_column:
    "Select a user to recommend products to:"
    user_selected = st.selectbox(options=purchasing_users, label="User ID's")
    
with right_column:
    "Recommendations!"
    recommendations = preprocessing.recommendation_pipeline(user_selected, user_profiles,encoded_df,df)
    st.dataframe(recommendations,width=200,column_config={"value":"Recommendations"})

model_eval = preprocessing.recommendation_eval_pipeline(user_selected, user_profiles,encoded_df,df)

model_accuracy=model_accuracy.with_columns(model_eval)
model_accuracy=model_accuracy.transpose()
names = names.with_columns(model_accuracy)
names = names.rename({"column_0":"Accuracy"})
visitors_px = px.bar(names, x='Data',y='Accuracy', title="Recommendation Accuracy")
st.plotly_chart(visitors_px)
    