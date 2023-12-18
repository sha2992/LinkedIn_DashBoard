import numpy as np
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

work_df = pd.read_excel('LinkedIn_Demo.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

months = work_df['Month Name'].unique()

# Layout of the dashboard
app.layout = html.Div([
    html.Title("LinkedIn DashBoard"),
    html.H1("Plotly Dashboard"),

    # Month range slider with an additional div for styling
    html.Div([
        dcc.RangeSlider(
            id='month-slider',
            marks={i: month for i, month in enumerate(months)},
            min=0,
            max=len(months) - 1,
            step=1,
            value=[0, len(months) - 1],  # Default to the entire range
        ),
    ], style={'width': '50%'}),  # Adjust the width as needed

    # Charts in the same div for side-by-side positioning
    html.Div([
        # Bar chart with preferred position
        dcc.Graph(
            id='bar-graph',
            figure=px.bar(work_df, x='Month Name', y='Total Applicant', title='Month wise Applicants'),
        ),
    ], style={'display': 'inline-block', 'width': '50%'}),

    html.Div([
        # Pie chart with preferred position
        dcc.Graph(
            id='pie-graph',
            figure=px.pie(work_df, 'Month Name', 'Total Applicant', title='Monthwise Total Applicant Percentage'),
        ),
    ], style={'display': 'inline-block', 'width': '50%'}),
])

# Define callback to update both charts based on month range selection
@app.callback(
    [Output('bar-graph', 'figure'),
     Output('pie-graph', 'figure')],
    [Input('month-slider', 'value')]
)
def update_charts(selected_months):
    start_index, end_index = selected_months

    # Filter data based on selected month range
    filtered_df = work_df.loc[start_index:end_index]

    # Update bar chart
    bar_fig = px.bar(filtered_df, x='Month Name', y='Total Applicant',
                     title=f'Month wise Applicants - {months[start_index]} to {months[end_index]}')

    # Update pie chart
    pie_fig = px.pie(filtered_df, 'Month Name', 'Total Applicant',
                     title=f'Monthwise Total Applicant Percentage - {months[start_index]} to {months[end_index]}')

    return bar_fig, pie_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)#, host='127.0.0.1', port=8000)
