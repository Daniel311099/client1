import dash
from dash import dcc, html
import plotly.express as px

# Create a Dash app
dash_app = dash.Dash(__name__)

# Generate a sample plot
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')

dash_app.layout = html.Div([
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# Expose the server property
app = dash_app.server
