# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min and max payload values
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[

    html.H1("SpaceX Launch Dashboard",
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))

])

# TASK 2: Pie chart callback
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):

    if selected_site == 'ALL':
        # Show total success launches by site
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        # Filter data for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f"Success vs Failure for {selected_site}"
        )
        return fig


# TASK 4: Scatter plot callback
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):

    low, high = payload_range

    # Filter by payload
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Outcome (All Sites)'
        )
        return fig
    else:
        site_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Outcome for {selected_site}'
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)