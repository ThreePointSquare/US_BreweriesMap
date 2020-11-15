#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:19:31 2020

@author: eshna
"""
# plotly-4.12.0 
# plotly-express-0.4.1

from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import plotly.graph_objects as go 
import pandas as pd

beers_df = pd.read_csv('data/brewery_beer_by_state.csv')
beers_df.fillna('N/A', inplace = True)
init_notebook_mode()

for col in beers_df.columns:
    beers_df[col] = beers_df[col].astype(str)

beers_df['text'] = beers_df['state_name'] + '<br>' + \
    '1. ' + beers_df['rank1'] + '<br>' + \
    '2. ' + beers_df['rank2'] + '<br>' + \
    '3. ' + beers_df['rank3']

fig = go.Figure(data = go.Choropleth(
    locations = beers_df['state'], # spatial coordinates
    z = beers_df['brewery_count'].astype(int), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    #colorscale = [[0, 'rgb(255,204,153)'],[1, 'rgb(255, 153, 51)'],[2, 'rgb(102,51,0)'] ],
    colorscale = 'hot_r',
    showscale = True,
    zmid = 500,
    zmax = 1500,
    zmin = 10,
    colorbar_title = 'Number Of Breweries',
    text=beers_df['text'], # hover text
    ))
fig.update_layout(
        title_text = 'US Breweries & Top-Rated Brews By State', 
        geo_scope='usa', #limit map scope to USA
        )
plot(fig, filename = "brewery_map.html")

