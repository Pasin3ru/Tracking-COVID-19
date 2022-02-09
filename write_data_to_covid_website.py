#!/usr/local/bin/python
# Author: RKP
# 2//7/2022


'''
    This writes Global, US, New York State and New York State County
    data in both HTML and JSON format for use in my website to
    JSON writes to /Users/robertpriddle/Tracking-COVID-19/_data/
    HTML writes to /Users/robertpriddle/Tracking-COVID-19/_includes/hospital-tables/

'''

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta

# Display option changes for DataFrame
pd.set_option('display.max_colwidth', 1000) # <---- This sets the max number characters in a column .
pd.set_option('display.max_columns', 50) # <---- This sets the max number of columns.
pd.set_option('display.max_rows', None)  # <---- Enable to view all rows.
pd.set_option('display.precision', 1)
pd.set_option('colheader_justify', 'center')

now = datetime.datetime.now().strftime("%A %B %-d, %Y at %-I:%M %p")
tday = datetime.date.today()

# Website for Dataset
url = 'https://www.worldometers.info/coronavirus/'
project_runtime = tday - datetime.date(2020,3,15)

# Making a request to the worldometer website
r = requests.get(url)

# Parsing html file to beautifulsoup
html = r.text
soup = BeautifulSoup(html, 'html.parser')

# Main Title
data_source = soup.title.text.split()
live_data = soup.find_all('div', id='maincounter-wrap')

# Extracting table data from html file
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

countries = []
cases = []
new_cases = []
deaths = []
new_deaths = []
total_recovered = []
active_cases = []
critical_cases = []
total_tested = []
population = []

for tr in table_rows:
    td = tr.find_all('td')
    countries.append(td[1].text)
    cases.append(td[2].text)
    new_cases.append(td[3].text)
    deaths.append(td[4].text)
    new_deaths.append(td[5].text)
    total_recovered.append(td[6].text)
    active_cases.append(td[7].text)
    critical_cases.append(td[8].text)
    total_tested.append(td[12].text)
    population.append(td[14].text)
        
headers = ['Country', 'Total Cases', 'New Cases', 'Total Deaths',
           'New Deaths', 'Total Recovered', 'Active Cases', 'Serious Critical', 'Total Tested', 'Population']

df = pd.DataFrame(list(zip(countries, cases, new_cases, deaths, new_deaths,
                           total_recovered, active_cases, critical_cases, total_tested, population)), columns=headers)

# Work around for unwanted rows. The first 7 rows show the globe broken into areas.
df = df[7:]
df.reset_index(inplace=True)
df.drop(['index', 'Total Recovered', 'Active Cases', 'Serious Critical', 'Total Tested'], axis=1, inplace=True)
df['Date'] = pd.to_datetime(tday).strftime('%-m/%-d/%Y')
cols = list(df.columns)
cols = [cols[-1]] + cols[:-1]
df = df[cols]

''' DO NOT MOVE THESE 5 LINES '''
columns=['Date']
date_data = pd.to_datetime(df['Date'].tail(1).values).strftime('%-b %-d, %Y')
last_update = pd.DataFrame(zip(date_data, columns))
print(f'\nLast Updated: {last_update.values[0][0]}')
last_update.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/last_update.json")

world_cases = int(df['Total Cases'][0].replace(',', ''))
usa_cases = int(str(df.loc[df['Country'] == 'USA']['Total Cases'][1]).replace(',', ''))
percent_cases = round(usa_cases / world_cases * 100,1)

# This adds the world total population to DataFrame
country_population = list(df['Population'].str.strip()) 
total_population = []
for i in country_population:
    i = i.replace(',','')
    if len(i) > 0:
        total_population.append(int(i))
global_population = sum(map(int, total_population))
df['Population'][0] = (f'{global_population:,}')

# This figures out the fatality rate for each country and adds column to DataFrame
cases = list(df['Total Cases'].str.strip()) 
total_cases = []
for i in cases:
    i = i.replace(',','')
    if len(i) > 0:
        total_cases.append(int(i))
        
deaths = list(df['Total Deaths'].str.strip())         
total_deaths = []
for i in deaths:
    i = i.replace(',','')
    if len(i) > 0:
        total_deaths.append(int(i))
        
df2 = pd.DataFrame(zip(total_cases, total_deaths), columns=['Cases', 'Deaths'])
df['Fatality Rate'] = round(df2['Deaths'] / df2['Cases'] * 100,1).astype(str) + '%'

# This adds the percentage of the population infected for each country
total_population.insert(0, global_population)
df3 = pd.DataFrame(zip(total_cases, total_population), columns=['Cases', 'Population'])
df['% Infected'] = round(df3['Cases'] / df3['Population'] * 100,1).astype(str) + '%'

wc = int(df['Total Cases'][0].replace(',',''))
w_pop = int(df['Population'].values[0].replace(',',''))
t_cases = df['Total Cases'].str.replace(',','')
p_cases = []
for i in t_cases:
    i = int(i)
    p_cases.append(i)
percent_total_cases = [] 
for i in p_cases:
    percent_total_cases.append(str(round(i / wc *100,1)) + '%')
df['% Total Cases'] = percent_total_cases
df['% Total Cases'][0] = ''

# This makes the population column the last column
population_column = df.pop('Population')
df.insert(9, 'Population', population_column)

global_df = df

global_df.drop(columns=['Date'], axis=1, inplace=True)
df.to_html("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_includes/hospital-tables/global_data.html", \
            col_space=115, justify="center", index=False)

print('Global HTML Data Written To Website')

nc = global_df['New Cases'][0]
nd = global_df['New Deaths'][0]
tc = global_df['Total Cases'][0]
td = global_df['Total Deaths'][0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
gldf = pd.DataFrame(data,columns)
gldf.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/world_total_data.json")

print('Global JSON Data Written To Website')

# Website for Dataset
url = 'https://www.worldometers.info/coronavirus/country/us/'

# Making a request to the worldometer website
r = requests.get(url)

# Parsing html file to beautifulsoup
html = r.text
soup = BeautifulSoup(html, 'html.parser')

live_data = soup.find_all('div', id="usa_table_countries_div")

# Extracting table data from html file
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

state = []
cases = []
new_cases = []
deaths = []
new_deaths = []
total_recovered = []
active_cases = []
critical_cases = []
total_tested = []
population = []

for tr in table_rows:
    td = tr.find_all('td')
    state.append(td[1].text)
    cases.append(td[2].text)
    new_cases.append(td[3].text)
    deaths.append(td[4].text)
    new_deaths.append(td[5].text)
    active_cases.append(td[6].text)
    total_tested.append(td[10].text)
    population.append(td[12].text)
        
headers = ['State', 'Total Cases', 'New Cases',
           'Total Deaths', 'New Deaths', 'Active Cases', 'Total Tested', 'Population']

df6 = pd.DataFrame(list(zip(state, cases, new_cases, deaths,
                            new_deaths, active_cases, total_tested, population)), columns=headers)

df6['Date'] = pd.to_datetime(tday).strftime('%-m/%-d/%Y')
cols = list(df6.columns)
cols = [cols[-1]] + cols[:-1]
df6 = df6[cols]
df6.replace(regex=True, inplace=True, to_replace=r'\n', value=r'')

us_total_population = df['Population'][1]
df6['Population'][0] = us_total_population # <---- Adds thousands seperator

blankIndex=[''] * len(df6) # <---- Hide row number
df6.index=blankIndex

us_df = df6
add_zero = us_df['New Cases'].head(1)[0]
if len(add_zero) == 0:
    add_zero = '0'
    us_df['New Cases'].head(1)[0] = add_zero
else:
    add_zero = add_zero
    
add_zero = us_df['New Deaths'][0]
if len(add_zero) == 0:
    add_zero = '0'
    us_df['New Deaths'][0] = add_zero
else:
    add_zero = add_zero

us_df.drop(columns=['Date'], axis=1, inplace=True)
us_df.to_html("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_includes/hospital-tables/us_data.html", \
            col_space=115, justify="center", index=False)

print('US HTML Data Written To Website')

nc = us_df['New Cases'][0]
nd = us_df['New Deaths'][0]
tc = us_df['Total Cases'][0]
td = us_df['Total Deaths'][0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
usdf = pd.DataFrame(data,columns)
usdf.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/us_total_data.json")

print('US JSON Data Written To Website')

# Website for Dataset
url = 'https://www.worldometers.info/coronavirus/usa/new-york/'
tday = datetime.date.today()

# Making a request to the worldometer website
r = requests.get(url)

# Parsing html file to beautifulsoup
html = r.text
soup = BeautifulSoup(html, 'html.parser')

live_data = soup.find_all('div', id='usa_table_countries_today')

# Extracting table data from html file
table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')

county = []
total_cases = []
new_cases = []
total_deaths = []
new_deaths = []
active_cases = []
total_tests = []

for tr in table_rows:
    td = tr.find_all('td')
    county.append(td[0].text)
    total_cases.append(td[1].text)
    new_cases.append(td[2].text)
    total_deaths.append(td[3].text)
    new_deaths.append(td[4].text)
    active_cases.append(td[5].text)
    total_tests.append(td[6].text)

headers = ['County', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Active Cases']
ny_df = pd.DataFrame(list(zip(county, total_cases, new_cases, total_deaths, new_deaths, active_cases)), columns=headers)


ny_df['Date'] = pd.to_datetime(tday)
ny_df['Date'] =  pd.to_datetime(ny_df['Date']) - timedelta(days=1)
ny_df['Date'] = pd.to_datetime(ny_df['Date']).dt.strftime('%-m/%-d/%Y')

cols = list(ny_df.columns)
cols = [cols[-1]] + cols[:-1]
ny_df = ny_df[cols]
ny_df.replace(regex=True, inplace=True, to_replace=r'\n', value=r'')
blankIndex=[''] * len(ny_df) # <---- Hide row number
ny_df.index=blankIndex # <---- Hide row number

county_df = ny_df.set_index('County', inplace=True)
try:
    county_df = ny_df.loc[['Warren ', 'Franklin ', 'Saratoga ', 'Washington ', 'Albany ', 'Schenectady ', 'Rensselaer '],:]
except KeyError:
    county_df = ny_df.loc[['Warren ', 'Saratoga ', 'Washington '],:]
    
county_df.reset_index(inplace=True)
first_column = county_df.pop('Date')
county_df.insert(0, 'Date', first_column)
county_df.sort_values('County', ascending=True, inplace=True)

x = ny_df.loc[ny_df.index == 'Warren ']
nc = x['New Cases'].values[0]
nd = x['New Deaths'].values[0]
tc = x['Total Cases'].values[0]
td = x['Total Deaths'].values[0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
wcdf = pd.DataFrame(data,columns)
add_zero = wcdf[2:3].values[0][0]
if len(add_zero) == 0:
    add_zero = '0'
    wcdf[2:3].values[0][0] = add_zero
else:
    add_zero = add_zero 
   
add_zero = wcdf[3:4].values[0][0]
if add_zero == ' ':
    add_zero = '0'
    wcdf[3:4].values[0][0] = add_zero
else:
    add_zero = add_zero 
wcdf2  = wcdf.replace(np.nan, 0)
wcdf2.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/warren_county_data.json")

print('Warren County JSON Data Written To Website')

x = ny_df.loc[ny_df.index == 'Saratoga ']
nc = x['New Cases'].values[0]
nd = x['New Deaths'].values[0]
tc = x['Total Cases'].values[0]
td = x['Total Deaths'].values[0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
scdf = pd.DataFrame(data,columns)
add_zero = scdf[2:3].values[0][0]
if len(add_zero) == 0:
    add_zero = '0'
    scdf[2:3].values[0][0] = add_zero
else:
    add_zero = add_zero 
   
add_zero = scdf[3:4].values[0][0]
if add_zero == ' ':
    add_zero = '0'
    scdf[3:4].values[0][0] = add_zero
else:
    add_zero = add_zero 
scdf.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/saratoga_county_data.json")

print('Saratoga County JSON Data Written To Website')

x = ny_df.loc[ny_df.index == 'Franklin ']
nc = x['New Cases'].values[0]
nd = x['New Deaths'].values[0]
tc = x['Total Cases'].values[0]
td = x['Total Deaths'].values[0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
fcdf = pd.DataFrame(data,columns)
add_zero = fcdf[2:3].values[0][0]
if len(add_zero) == 0:
    add_zero = '0'
    fcdf[2:3].values[0][0] = add_zero
else:
    add_zero = add_zero
    
add_zero = fcdf[3:4].values[0][0]
if add_zero == ' ':
    add_zero = '0'
    fcdf[3:4].values[0][0] = add_zero
else:
    add_zero = add_zero 
fcdf.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/franklin_county_data.json")

print('Franklin County JSON Data Written To Website')

x = ny_df.loc[ny_df.index == 'Washington ']
nc = x['New Cases'].values[0]
nd = x['New Deaths'].values[0]
tc = x['Total Cases'].values[0]
td = x['Total Deaths'].values[0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
wgcdf = pd.DataFrame(data,columns)
add_zero = wgcdf[2:3].values[0][0]
if len(add_zero) == 0:
    add_zero = '0'
    wgcdf[2:3].values[0][0] = add_zero
else:
    add_zero = add_zero
    
add_zero = wgcdf[3:4].values[0][0]
if add_zero == ' ':
    add_zero = '0'
    wgcdf[3:4].values[0][0] = add_zero
else:
    add_zero = add_zero 
wgcdf.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/washington_county_data.json")

print('Washington County JSON Data Written To Website')

nys_df = ny_df
nys_df.drop(columns=['Date'], axis=1, inplace=True)
nys_df.reset_index(inplace=True)
nys_df.to_html("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_includes/hospital-tables/ny_state_data.html", \
            col_space=120, justify="center", index=False)

print('NY State HTML Data Written To Website')

nc = ny_df['New Cases'][0]
nd = ny_df['New Deaths'][0]
tc = ny_df['Total Cases'][0]
td = ny_df['Total Deaths'][0]
data = tc, td, nc, nd
columns = ['Total Cases: ', 'Total Deaths: ', 'New Cases: ', 'New Deaths: ' ]
nydf = pd.DataFrame(data,columns)
add_zero = nydf[2:3].values[0][0]
if len(add_zero) == 0:
    add_zero = '0'
    nydf[2:3].values[0][0] = add_zero
else:
    add_zero = add_zero
    
add_zero = nydf[3:4].values[0][0]
if len(add_zero) == 0:
    add_zero = '0'
    nydf[3:4].values[0][0] = add_zero
else:
    add_zero = add_zero 
nydf.to_json("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/ny_total_data.json")

print('NY State JSON Data Written To Website')