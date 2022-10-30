#import libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

#Connect to Cloud SQL using the Cloud SQL Python connector

#define your app object
app = Dash(__name__)

#--Import and clean data(importing csv into pandas)
#df = pd.read_csv('bees_data.csv') ?
#To get data from Cloud Sql use this file 
df = pd.read_csv('~/development/gcp/dashboards/bees/bees_data.csv')

#group data by pctOfColonies
df = df.groupby(['state', 'ansi', 'affectedBy', 'year', 'stateCode'])[['pctOfColonies']].mean()
df.reset_index(inplace=True)
print(df[:5])

#App layout
app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                 ],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

     dcc.Graph(id='my_bee_map', figure={})
    
])

#Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
     [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
  print(option_slctd)
  print(type(option_slctd))

  container = "The year chose by user was: {}".format(option_slctd)

  dff = df.copy()
  dff = dff[dff["year"] == option_slctd]
  dff = dff[dff["affectedBy"] == "Varroa_mites"]

    #Plotly Express
  fig = px.choropleth(
    data_frame = dff,
    locationmode='USA-states',
    locations='stateCode',
    scope="usa",
    color='pctOfColonies',
    hover_data=['state', 'pctOfColonies'],
    color_continuous_scale=px.colors.sequential.YlOrRd,
    labels={'pctOfColonies': '% of Bee Colonies'},
    template='plotly_dark'
)
  
  return container, fig

if __name__ == '__main__':
    app.run_server(debug=False)

