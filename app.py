import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)

def identity(x): return x

func_list = {'identity': identity, 'mean': np.mean, 'median': np.median, 'sum': np.sum, 'max': np.max, 'min': np.min}

app.layout = html.Div([
    html.H2(children="Element Periodic Table", className="header-title"),
    html.Div(
        [
            html.Div([
                html.Div(children="index", className="menu-title"),
                dcc.Dropdown(
                    id = "index",
                    options = [{
                        'label': i,
                        'value': i
                    } for i in df.columns],
                    value = "all columns",
                    multi = True,
                    ),
            ]),
            html.Div([
                html.Div(children="columns", className="menu-title"),
                dcc.Dropdown(
                    id = "columns",
                    options = [{
                        'label': i,
                        'value': i
                    } for i in df.columns],
                    value = "all columns",
                    multi = True,
                    ),
            ]),
            html.Div([
                html.Div(children="values", className="menu-title"),
                dcc.Dropdown(
                    id = "values",
                    options = [{
                        'label': i,
                        'value': i
                    } for i in df.columns],
                    value = "all columns",
                    ),
            ]),
            html.Div([
                html.Div(children="aggfunc", className="menu-title"),
                dcc.Dropdown(
                    id = "aggfunc",
                    options = [{
                        'label': i,
                        'value': i
                    } for i in func_list.keys()],
                    value = "none",
                    ),
            ]),
        ],
    ),

    dash_table.DataTable(
        id='pivot-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    ),
])

@app.callback(
    [
        Output('pivot-table', 'data'),
        Output('pivot-table', 'columns')
    ],
    [
        Input("index", "value"),
        Input("columns", "value"),
        Input("values", "value"),
        Input("aggfunc", "value"),
    ],
)

def update_table(input_index, input_column, input_value, input_aggfunc):
    if input_index == "all columns" or input_column == "all columns" or input_value == "all columns" or input_aggfunc == "none":
        df_table = df.copy()
    else:
        df_table = pd.pivot_table(df,index=input_index,columns=input_column,values=input_value,aggfunc=func_list[input_aggfunc],fill_value='NaN')
    
    columns=[{"name": str(i), "id": str(i)} for i in df_table.columns]
    data=df_table.to_dict('records')

    return [data, columns]

app.run_server(debug=True, host="0.0.0.0")