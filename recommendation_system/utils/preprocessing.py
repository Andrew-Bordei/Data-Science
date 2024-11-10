def encoding(df:pl.DataFrame) -> pl.DataFrame: 
    encoding = df_cleaned.filter(pl.col('country') == "United States").select(
    pl.col('fullVisitorId'),pl.col('country'), pl.col('browser'),
    pl.col('transactionId'),pl.col('v2ProductName')
    )
    
    canada = df_cleaned.filter(pl.col('country') == "Canada").select(
    pl.col('fullVisitorId'),pl.col('country'), pl.col('browser'),
    pl.col('transactionId'),pl.col('v2ProductName')
    )