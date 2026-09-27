from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go


DF = pd.read_csv(r"C:\Users\pdawg\OneDrive\CDC 2026 DATA\doi-10.7281-t170wn53\index_scores_v3_2026.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Political candidate voting pool analysis'),
    html.P("Select a candidate:"),
    dcc.RadioItems(
        id='candidate',
        options=["Economic", "Education","Health", "Housing", "Crime"],
        value="Education",
        inline=True
    ),
    dcc.Graph(id="graph"),
])





DF_CA = DF[DF["State"] == "CA"].copy()

DF_CA["FIPS County Code"] = DF_CA["FIPS County Code"].astype(int).astype(str).str.zfill(5)

DF_CA_agg = DF_CA.groupby("FIPS County Code").mean(numeric_only=True)

DF_CA_agg["County"] = DF_CA.groupby("FIPS County Code")["County"].first()

@app.callback(
    Output("graph", "figure"),
    Input("candidate", "value"))
def display_choropleth(candidate):
    fig = go.Figure(go.Choroplethmap(geojson=counties, 
                                 locations=DF_CA_agg.index,
                                 z=DF_CA_agg[candidate],
                                 colorscale="Viridis", zmin=10, zmax=80,
                                 text=DF_CA_agg["County"],
                                marker_opacity=0.5, marker_line_width=0))
    fig.update_layout(map_style="carto-positron",
                  map_zoom=4, map_center = {"lat": 36.778, "lon": -119.417})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


app.run(debug=True)