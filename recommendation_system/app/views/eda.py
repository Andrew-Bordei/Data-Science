import streamlit as st
import polars as pl
import plotly.express as px

encoded_df = pl.read_csv("../data/encoded_df.csv",ignore_errors=True)
daily_purchases = pl.read_csv("../data/daily_purchases.csv",ignore_errors=True)
daily_visitors= pl.read_csv("../data/daily_visitors.csv",ignore_errors=True)
pie_categories = pl.read_csv("../data/pie_categories.csv",ignore_errors=True)
pie_products = pl.read_csv("../data/pie_products.csv",ignore_errors=True)
viewed_categories = pl.read_csv("../data/viewed_categories.csv",ignore_errors=True)
viewed_products = pl.read_csv("../data/viewed_products.csv",ignore_errors=True)

pie_options = ["Most Sold Categories", "Most Sold Products", "Most Viewed Categories", "Most Viewed Products"]
daily_options = ["Daily Purchases", "Daily Users"]

st.title("Exploratory Data Analysis")

daily_selected = st.selectbox(options=daily_options, label="Data")
match daily_selected:
    case "Daily Purchases":
        visitors_px = px.bar(daily_purchases[-90:], x='date', y='len')
        st.plotly_chart(visitors_px)
    case "Daily Users":
        visitors_px = px.bar(daily_visitors[-90:], x='date', y='fullVisitorId')
        st.plotly_chart(visitors_px)

# Pie chart 
pie_selected = st.selectbox(options=pie_options, label="Data")
match pie_selected:
    case "Most Sold Categories":
        cat_px = px.pie(pie_categories[:10], values="count", names="v2ProductCategory", title=f"{pie_selected}")
        st.plotly_chart(cat_px)
    case "Most Sold Products":
        fig_px = px.pie(pie_products[:10], values="count", names="v2ProductName", title=f"{pie_selected}")
        st.plotly_chart(fig_px) 
    case "Most Viewed Categories":
        cat_px = px.pie(viewed_categories[:10], values="count", names="v2ProductCategory", title=f"{pie_selected}")
        st.plotly_chart(cat_px)
    case "Most Viewed Products":
        fig_px = px.pie(viewed_products[:10], values="count", names="v2ProductName", title=f"{pie_selected}")
        st.plotly_chart(fig_px) 

# Correlation matrix 
st.markdown("##### Feature Correlations")
corr_px = px.imshow(encoded_df['country':].corr(), x=encoded_df.columns[1:], y=encoded_df.columns[1:], 
                    text_auto='.2f')
st.plotly_chart(corr_px)