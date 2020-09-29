# -------------------------------------------------------------------------------------
# # import everything

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

ext_url = 'https://github.com/plotly/dash-app-stylesheets/blob/master/dash-docs-tutorial-stylesheet1.css'
app.css.append_css({'external_url': ext_url})

df = pd.read_excel('cleaned_data.xlsx')
df2 = pd.read_excel('cleaned_data.xlsx')
df2 = df2.sort_values(by='Item Sort Order',ascending=True)
df2 = df2.drop('Item Type',axis=1)
# -------------------------------------------------------------------------------------
# Start Dash Coding

app.layout = html.Div([
    html.Div([
        html.H1('Fruits and Vegetables'),
        html.H3('Select filter type : ')
    ], style={'textAlign': 'center'}),

    html.Br(),
    html.Div([
        dbc.RadioItems(
            options=[
                {'label': 'Select All', 'value': 'ALL'},
                {'label': 'Fruits', 'value': 'FRT'},
                {'label': 'Vegetables', 'value': 'VEG'}
            ],
            value='ALL', 
            id="check-list",
            inline=True,
        ),
    ],style={'textAlign': 'center'}),

    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
                id = 'main-table',
                data = df2.to_dict('records'),
                columns = [{'id':c,'name':c} for c in df2.columns],
                style_as_list_view=True,  
                style_header={
                    'backgroundColor':'white',
                    'fontWeight':'bold',
                    'color': 'black'             
                },
                style_cell_conditional=[],
                virtualization=True,   
            ) ,width={'size':6,'offset':3}     # end of datatable

        ) # end of dbc col
    ), # end of dbc row

# button to save
    html.Br(),   
    dbc.Row([
        dbc.Col(
            dbc.Button("Save", color="success",size='lg', className="mr-1", id='save-button'),
            width = {'size':3,'offset':5}
            )
        ]),
    html.Hr(),
    dbc.Alert([
        html.H4("Success! ", className="alert-heading"),
        "Your data saved in your local drive. It should be saved as 'BQ-Custom-by--Kanishk_sharma.xlsx'.",
        ],
        id="alert-fade",
        dismissable=True,
        duration=4000,
        is_open=True,
    ),


dbc.Row([
    dbc.Col(
        dcc.Markdown('''
        > ###### ** The Project is created by : [Kanishk Sharma](https://linkedin.com/in/kanishksh4rma) **
        ''') , width={'size':5,'offset':0},
        ),
    ]),


])  # end of whole div

# -------------------------------------------------------------------------------------
# call backs

@app.callback(
    dash.dependencies.Output('main-table',component_property='data'),
    [dash.dependencies.Input('check-list','value'),
    dash.dependencies.Input('save-button', 'n_clicks')])

def update_main_table(value,n_clicks):  
    
    if 'ALL' in value:
        dff = df2

    if 'FRT' in value:
        dff = df[df['Item Type'] == 'uFruit']
        dff = dff.drop('Item Type',axis=1)
        dff = dff.sort_values(by='Item Sort Order',ascending=True)
    elif 'VEG' in value:
        dff = df[df['Item Type'] == 'uVegetable']
        dff = dff.drop('Item Type',axis=1)
        dff = dff.sort_values(by='Item Sort Order',ascending=True)
    
    if n_clicks > 0:
        dff.to_excel('BQ-Custom-by--Kanishk_Sharma.xlsx', index=False)
    return dff.to_dict('recordes')

@app.callback(
    dash.dependencies.Output("alert-fade", "is_open"),
    [dash.dependencies.Input("save-button", "n_clicks")],
    [dash.dependencies.State("alert-fade", "is_open")],
)
def toggle_alert(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# -------------------------------------------------------------------------------------
# driver's code

if __name__ == '__main__':
    app.run_server(debug=False)
