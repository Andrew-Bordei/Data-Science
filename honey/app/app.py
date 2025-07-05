from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import sys

sys.path.append('./')

from eda.eda_pipeline import eda_pipeline 

# run the eda pipeline
eda_pipeline(5.17)

df = pd.read_csv('honey_grouped_data.csv')

ranking = ['Top 5', 'Top 15', 'Top 25', 'Top 50', 'Top 100', 'Others']
dates = df['date_acquired'].unique()

app = Dash()

app.layout = [
    html.H1(children='Honey Market Analytics', style={'textAlign':'center'}),
    dcc.Dropdown(
        ranking, 
        id='dropdown-selection', 
        value='Top 5',
        ),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = df

    fig = make_subplots(
        rows=2, cols=2, 
        subplot_titles=[
            "Price Per Ounce", "Monthly Sales", 
            "Product Rating", "Estimated Monthly Profit"
        ]
    )

    fig.add_trace(row=1, col=1,
        trace=go.Scatter(
            x=dates, 
            y=dff[dff['rank'] == f'{value}']['price_per_ounce'],
            mode="lines+markers",
            name='Price Per Ounce',
            hovertemplate="%{y}%{_xother}",
        )
    )
    
    fig.add_trace(
        row=1, col=2,
        trace=go.Scatter(
            x=dates, 
            y=dff[dff['rank'] == f'{value}']['bought_last_month'],
            mode="lines+markers",
            name='Monthly Sales',
            hovertemplate="%{y}%{_xother}",
        )
    )
    
    fig.add_trace(
        row=2, col=1,
        trace=go.Scatter(
            x=dates, 
            y=dff[dff['rank'] == f'{value}']['product_rating'],
            mode="lines+markers",
            name='Product Rating',
            hovertemplate="%{y}%{_xother}",
        )
    )
    
    fig.add_trace(
        row=2, col=2,
        trace=go.Scatter(
            x=dates, 
            y=dff[dff['rank'] == f'{value}']['estimated_monthly_profit'],
            mode="lines+markers",
            name='Estimated Monthly Profit',
            hovertemplate="%{y}%{_xother}",
        )
    )

    axis_labels = [
        {"row": 1, "col": 1, "x": "Date", "y": "Price (USD)"},
        {"row": 1, "col": 2, "x": "Date", "y": "Units"},
        {"row": 2, "col": 1, "x": "Date", "y": "Rating"},
        {"row": 2, "col": 2, "x": "Date", "y": "Profit (USD)"},
    ]

    for label in axis_labels:
        fig.update_xaxes(title_text=label["x"], row=label["row"], col=label["col"])
        fig.update_yaxes(title_text=label["y"], row=label["row"], col=label["col"])

        fig.update_layout(height=825)

    return fig

if __name__ == '__main__':
    # app.run(debug=True)
    # Make the app accessible to people on same wifi network if they have the url 
    app.run(host="0.0.0.0", port="8050")
