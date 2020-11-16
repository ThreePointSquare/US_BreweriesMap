#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 11:56:31 2020

@author: eshna
"""



import pandas as pd
from collections import Counter


# Reading CSV files. 
beer_df = pd.read_csv('data/8260_1.csv')
top_beers_df = pd.read_csv('data/popular_beer_by_state.csv')
zip_df = pd.read_csv('data/ZIP-COUNTY-FIPS_2017-06.csv')
zip2state = dict(zip(zip_df.ZIP,zip_df.STATE))
states = [] 

# Remove Breweries in Canada US. Virgin Islands & Brazil from our dataset
a = beer_df.index[(beer_df['province'] == 'NL') | (beer_df['province'] == 'ON')
                   | (beer_df['province'] == 'PR') | (beer_df['province'] == 'VI')
                   | (beer_df['province'] == 'AB')].tolist()
print("index", a)
beer_df = beer_df.drop(a).reset_index()


# Mapping zipcode to state

for i, zipcode in enumerate(beer_df['postalCode']): 
    try:
        if (pd.isnull(zipcode) != True):
            states.append(zip2state[int(zipcode)])
                
        else: 
            states.append(beer_df['province'][i])
    except:
        states.append(beer_df['province'][i])
        continue
        
            
# Assigning correct states to some entries that did not have 
# standard values for zipcodes/province   
STATE_ABBR = {'Arizona': 'AZ', 
              'California': 'CA', 
              'Chicago': 'IL',
              'Colorado': 'CO',  
              'District of Columbia': 'MD',
              'DC': 'MD', 
              'Hawaii': 'HI', 
              'Illinois': 'IL', 
              'Louisville': 'KY', 
              'Massachusetts': 'MA',  
              'Nevada': 'NV',
              'New York': 'NY',
              'Pennsylvania': 'PA', 
              'Tennessee': 'TN', 
              'Texas': 'TX', 
              'Washington': 'WA',
              }
            
for idx, st in enumerate(states):    
    if st in STATE_ABBR.keys():
        states[idx] = STATE_ABBR[st]
         

for idx, st in enumerate(states):
    if st == 'US':
        #print(beer_df['name'][idx])
        if(beer_df['name'][idx] == 'Speakeasy Ales & Lagers'):
            states[idx] = 'CA'
        else:
            states[idx] = 'NY'
            


print(len(set(states)))


print(len(beer_df['postalCode']))

# generating new dataset of no. of breweries & top ranked breweries by state

breweries_count_by_state = Counter(states)
brew_count_df = pd.DataFrame.from_dict(breweries_count_by_state, orient='index').reset_index()
brew_count_df = brew_count_df.rename(columns={'index':'state', 0:'brewery_count'})

final_brewery_df = pd.merge(top_beers_df, brew_count_df, on = 'state')
final_brewery_df.to_csv('data/brewery_beer_by_state.csv')





    