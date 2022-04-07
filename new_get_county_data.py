import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from datetime import timedelta

pd.options.mode.chained_assignment = None

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
    county_df = ny_df.loc[['Warren ', 'Saratoga ', 'Franklin '],:]
    
county_df.reset_index(inplace=True)
# blankIndex=[''] * len(county_df) # <---- Hide row number
# county_df.index=blankIndex # <---- Hide row number

first_column = county_df.pop('Date')
county_df.insert(0, 'Date', first_column)
county_df.sort_values('County', ascending=True, inplace=True)



wc = county_df.loc[county_df['County'] == 'Warren ']
blankIndex=[''] * len(wc) # <---- Hide row number
wc.index=blankIndex # <---- Hide row number
wc.drop(columns=['Date', 'County', 'Active Cases'], axis=1, inplace=True)
if wc['New Cases'].tail(1).values[0] == '':
    wc['New Cases'].tail(1).values[0] = 0
if wc['New Deaths'].values[0] == ' ':
    wc['New Deaths'].values[0] = 0
wc.T.to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/warren_county_data.json') 

sc = county_df.loc[county_df['County'] == 'Saratoga ']
blankIndex=[''] * len(sc) # <---- Hide row number
sc.index=blankIndex # <---- Hide row number
sc.drop(columns=['Date', 'County', 'Active Cases'], axis=1, inplace=True)
if sc['New Cases'].tail(1).values[0] == '':
    sc['New Cases'].tail(1).values[0] = 0
if sc['New Deaths'].values[0] == ' ':
    sc['New Deaths'].values[0] = 0
sc.T.to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/saratoga_county_data.json') 

fc = county_df.loc[county_df['County'] == 'Franklin ']
blankIndex=[''] * len(fc) # <---- Hide row number
fc.index=blankIndex # <---- Hide row number
fc.drop(columns=['Date', 'County', 'Active Cases'], axis=1, inplace=True)
if fc['New Cases'].tail(1).values[0] == '':
    fc['New Cases'].tail(1).values[0] = 0
if fc['New Deaths'].values[0] == ' ':
    fc['New Deaths'].values[0] = 0
fc.T.to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_data/franklin_county_data.json') 

print('Complete')