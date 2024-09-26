# Crude Oil Machine Learning Forecast Model
![network header](assets/header.png)
## Dataset
The model will be using 14 differenet features combined into a single dataset. All data is under a common use license and can be freely found online. 

## Objectives

The main objective of this project is:

> **To develop a machine learning model that will be able to accurately predict the price of crude oil**

To accomplish the objective it is necessary to complete 5 technical sub-objectives:

1. Clean and merge that different features into a single dataset 
2. Perform exploratory data analysis 
3. Engineer new predictive features using insights from exploratory data analysis 
4. Test and train ML models to determine which performs the best 
5. Iterate over the project to improve any and all areas 

## Main Insights
From the exploratory data analysis it was discovered that all features are non-normally distributed. There is significant volatility in oil production. American oil production has no statistical effect on the price of crude oil. 

The US dollar and world oil consumption data were the most important features the machine learning models utilized. 


## Engineered Features
Two new features were extracted during the project. 
- Feature 1 - Aggregating oil producing countries into one feature.
- Feature 2 - Converting the data to a 7 day rolling mean, to smooth volatility. 

However, the 7 day rolling mean feature engineering process had negavtive effects on the models' accuracy. The Random Forest RMSE saw a 13% reduction in accuracy, the Support Vector Regressor RMSE was reduced by 13.5%, with only the XGB Regressor having an improved model accuracy of 2.3% on the feature engineered dataset. This effect could likely be due to volatility being inherent in the oil market and such behavior is necessary for the models' to train on. 

## Model Selection
Four different machine learning models(Decision Tree, Random Forest, Support Vector Regressor, XGB Regressor) were tested during the project along with linear regression acting as a baseline model. The best performing model was the Decision Tree.  



