import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

app = dash.Dash(__name__)

year_list = [i for i in range(1980, 2024, 1)]

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", 
            style={"text-align": "center", "color": "#503D36", "font-size": "24px"}),

    dcc.Dropdown(
        id="dropdown-statistics",
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value='Yearly Statistics',
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
    ),

    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select a year',
        style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
    ),

    html.Div(id='output-container', style={'display': 'flex', 'flex-wrap': 'wrap'})
])

@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(statistics_value):
    return statistics_value != 'Yearly Statistics'


@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(statistics_value, selected_year):
    if statistics_value == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Automobile Sales During Recessions")
        )

        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Sales by Vehicle Type")
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', 
                          title="Advertising Expenditure Share by Vehicle Type")
        )

        unemp_data = recession_data.groupby(['Unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='Unemployment_Rate', y='Automobile_Sales', color='Vehicle_Type',
                          title="Effect of Unemployment Rate on Vehicle Type and Sales")
        )

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex', 'width': '100%'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex', 'width': '100%'})
        ]

    elif selected_year and statistics_value == 'Yearly Statistics':
        yearly_data = data[data['Year'] == selected_year]


        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales")
        )

        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title="Total Monthly Automobile Sales")
        )

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f"Average Vehicles Sold by Vehicle Type in {selected_year}")
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Total Advertisement Expenditure by Vehicle Type")
        )

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex', 'width': '100%'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex', 'width': '100%'})
        ]

    return [html.Div("Select a valid report type and year.", style={'text-align': 'center'})]

if __name__ == '__main__':
    app.run_server()
