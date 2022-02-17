#!/usr/local/bin/python
# RKP
# 2/13/2022

import pandas as pd
from datetime import datetime
from icons import *
from phases_of_moon import lunar_phase
import get_suntime

pd.set_option('display.max_colwidth', 1000) # <---- This sets the max number characters in a column .
pd.set_option('display.max_columns', 50) # <---- This sets the max number of columns.
pd.set_option('display.max_rows', None)  # <---- Enable to view all rows.

# These are Time Stamps I used for Pandas Data Frame
tday = datetime.now()
current_date = datetime.now()
formatted_date = current_date.strftime("%A, %B %-d, %Y")

today_2019 = f'{tday.month}/{tday.day}/2019'
today_2020 = f'{tday.month}/{tday.day}/2020'
today_2021 = f'{tday.month}/{tday.day}/2021'
today_2022 = f'{tday.month}/{tday.day}/2022'

print('\nCreating DataFrame....\n')
# Sheet Names
a = 'Weather-Data-2019'
b = 'Weather-Data-2020'
c = 'Weather-Data-2021'
d = 'Weather-Data-2022'

# Work Book Path
# data_file = '/Volumes/PiShare/WeatherStation.xlsx'
data_file = '/Volumes/Weather-Data/WeatherStation.xlsx'


# Assign Sheet to DataFrame
# df2019 = pd.read_excel(data_file, sheet_name= a , na_values=[' '])
# df2020 = pd.read_excel(data_file, sheet_name= b , na_values=[' '])
# df2021 = pd.read_excel(data_file, sheet_name= c , na_values=[' '])
# df2022 = pd.read_excel(data_file, sheet_name= d , na_values=[' '])

df2019 = pd.read_csv('/Volumes/Weather-Data/Weather-Data-2019.csv')
df2020 = pd.read_csv('/Volumes/Weather-Data/Weather-Data-2020.csv')
df2021 = pd.read_csv('/Volumes/Weather-Data/Weather-Data-2021.csv')
df2022 = pd.read_csv('/Volumes/Weather-Data/Weather-Data-2022.csv')

blankIndex=[''] * len(df2019) # <---- Hide row number
df2019.index=blankIndex # <---- Hide row number
df2019['DATE'] = pd.to_datetime(df2019.DATE)

blankIndex=[''] * len(df2020) # <---- Hide row number
df2020.index=blankIndex # <---- Hide row number
df2020['DATE'] = pd.to_datetime(df2020.DATE)

blankIndex=[''] * len(df2021) # <---- Hide row number
df2021.index=blankIndex # <---- Hide row number
df2021['DATE'] = pd.to_datetime(df2021.DATE)

blankIndex=[''] * len(df2022) # <---- Hide row number
df2022.index=blankIndex # <---- Hide row number
df2022['DATE'] = pd.to_datetime(df2022.DATE)

pd.Series.__unicode__ = pd.Series.to_string

# Here I set the search for each year  = today's month and day and store the results
daily_high_low_2019 = df2019.loc[(df2019['DATE'] == pd.to_datetime(today_2019))][['DATE', 'STATION_ID', 'CITY', 'STATE', 'CONDITIONS', 'FORECAST', 'TEMP']].agg(['max','min','mean'])
daily_high_low_2020 = df2020.loc[(df2020['DATE'] == pd.to_datetime(today_2020))][['DATE', 'STATION_ID', 'CITY', 'STATE', 'CONDITIONS', 'FORECAST', 'TEMP']].agg(['max','min','mean'])
daily_high_low_2021 = df2021.loc[(df2021['DATE'] == pd.to_datetime(today_2021))][['DATE', 'STATION_ID', 'CITY', 'STATE', 'UV_INDEX','CONDITIONS', 'FORECAST', 'TEMP']].agg(['max','min','mean'])
daily_high_low_2022 = df2022.loc[(df2022['DATE'] == pd.to_datetime(today_2022))][['DATE', 'STATION_ID', 'CITY', 'STATE', 'UV_INDEX', 'CONDITIONS', 'FORECAST', 'TEMP']].agg(['max','min','mean'])


# Here I create a data frame to display the results 
columns = ['2019', '2020', '2021', '2022']
index=['High:', 'Low:', 'Average:', 'Conditions:']

df = pd.DataFrame(columns=columns, index=index)

##########################################################################################
# Here I add the search results to the 2019 data frame
# Because I didn't start until 5/7/2019 there is no data from 1/1/2019 - 5/6/2019. 
# This line makes sure to only add the degree symbal to a cell with a number and not 'NaN'
# If data is available I get the high and low for each month and add the degree symbal 
if str(daily_high_low_2019['TEMP'].max()) != 'nan':
    df['2019'][0] = str(daily_high_low_2019['TEMP'].max()) + '\u00B0F'
    df['2019'][1] = str(daily_high_low_2019['TEMP'].min()) + '\u00B0F'
    df['2019'][2] = str(round(daily_high_low_2019['TEMP'].mean(),1)) + '\u00B0F'
    df['2019'][3] = df2019.loc[(df2019['DATE'] == pd.to_datetime(today_2019))]['FORECAST'].tail(1)[0]
    daily_rain = df2019.loc[(df2019['DATE'] == pd.to_datetime(today_2019))]['DAILY_RAIN'][0]
    daily_forecast = list(df2019.loc[(df2019['DATE'] == pd.to_datetime(today_2019))]['FORECAST'])
    if daily_rain >= .25:
        df['2019'][3] = 'Rain'
    else:
        def most_frequent(daily_forecast):
            df['2019'][3] = (max(set(daily_forecast), key = daily_forecast.count))
        most_frequent(daily_forecast) 
else:
    pass
current_forecast = df['2019'][3]
####################################################################
# Here I add the search results to the 2020 data frame
df['2020'][0] = str(daily_high_low_2020['TEMP'].max()) + '\u00B0F'
df['2020'][1] = str(daily_high_low_2020['TEMP'].min()) + '\u00B0F'
df['2020'][2] = str(round(daily_high_low_2020['TEMP'].mean(),1)) + '\u00B0F'
df['2020'][3] = df2020.loc[(df2020['DATE'] == pd.to_datetime(today_2020))]['FORECAST'].tail(1)[0]
daily_forecast = list(df2020.loc[(df2020['DATE'] == pd.to_datetime(today_2020))]['FORECAST'])
daily_rain = df2020.loc[(df2020['DATE'] == pd.to_datetime(today_2020))]['DAILY_RAIN'][0]
if daily_rain >= .25:
    df['2020'][3] = 'Rain'
else:
    def most_frequent(daily_forecast):
        df['2020'][3] = (max(set(daily_forecast), key = daily_forecast.count))
    most_frequent(daily_forecast) 

current_forecast = df['2020'][3]
#####################################################################
# Here I add the search results to the 2021 data frame
df['2021'][0] = str(round(daily_high_low_2021['TEMP'].max(),1)) + '\u00B0F'
df['2021'][1] = str(round(daily_high_low_2021['TEMP'].min(),1)) + '\u00B0F'
df['2021'][2] = str(round(daily_high_low_2021['TEMP'].mean(),1)) + '\u00B0F'
df['2021'][3] = df2021.loc[(df2021['DATE'] == pd.to_datetime(today_2021))]['FORECAST'].tail(1)[0]
daily_forecast = list(df2021.loc[(df2021['DATE'] == pd.to_datetime(today_2021))]['FORECAST']) 
daily_rain = df2021.loc[(df2021['DATE'] == pd.to_datetime(today_2021))]['DAILY_RAIN'][0]
if daily_rain >= .25:
    df['2021'][3] = 'Rain'
elif 'Snow' in daily_forecast and daily_forecast.count('Snow') > 6:
    df['2021'][3] = 'Snow'
else:    
    def most_frequent(daily_forecast):
        df['2021'][3] = (max(set(daily_forecast), key = daily_forecast.count))
    #     print(f'Items in List: {len(daily_forecast)} - ' + df['2021'][3] + ' has repeated ' + str(daily_forecast.count(df['2021'][3])) + ' times for today')
    most_frequent(daily_forecast)
        
current_forecast = df['2021'][3]
#########################################################################
# Here I add the search results to the 2022 data frame
df['2022'][0] = str(round(daily_high_low_2022['TEMP'].max(),1)) + '\u00B0F'
df['2022'][1] = str(round(daily_high_low_2022['TEMP'].min(),1)) + '\u00B0F'
df['2022'][2] = str(round(daily_high_low_2022['TEMP'].mean(),1)) + '\u00B0F'
df['2022'][3] = df2022.loc[(df2022['DATE'] == pd.to_datetime(today_2022))]['FORECAST'].tail(1)[0]

# My thoughts here are.. If I run this at 11:00 pm it will show me the over-all conditions for the day
# and not just the last condition in the list, but during the day it will show all the changes
if datetime.now().time().hour >= 23:
    daily_forecast = list(df2022.loc[(df2022['DATE'] == pd.to_datetime(today_2022))]['FORECAST']) 
    daily_rain = df2022.loc[(df2022['DATE'] == pd.to_datetime(today_2022))]['DAILY_RAIN'][0]
    if daily_rain >= .25:
        df['2022'][3] = 'Rain'
    else:    
        def most_frequent(daily_forecast):
            df['2022'][3] = (max(set(daily_forecast), key = daily_forecast.count))
        #     print(f'Items in List: {len(daily_forecast)} - ' + df['2021'][3] + ' has repeated ' + str(daily_forecast.count(df['2021'][3])) + ' times for today')
        most_frequent(daily_forecast)
else:
    pass
current_forecast = df['2022'][3]
###########################################################################
# These are from imported get_suntime
sunrise_ts = datetime.fromtimestamp(get_suntime.sunrise)
sunset_ts = datetime.fromtimestamp(get_suntime.sunset)
current_time_ts = datetime.now()

# Add icons for specific monthly eventts
########################################
# St Patricks Day
if tday.month == 3 and tday.day == 17:
    monthly_icon = ' ' + shamrock
    
# April    
elif tday.month == 4: 
    if tday.day == 14:
        monthly_icon = ' ' + heart
    elif tday.day == 26:
        monthly_icon = ' ' + birthday 
    else:
        pass
    
# December    
elif tday.month == 12:
    if tday.day == 10:
        monthly_icon = ' ' + birthday
    elif tday.day == 24:
        monthly_icon = ' ' + santa
    elif tday.day == 25:
        monthly_icon = ' ' + christmas_tree
    else:
        monthly_icon = ' ' + snowman
else:
    monthly_icon = ''
    
################################################################################
# Add icons for specific weather events
if 'Clear' in current_forecast:
    if current_time_ts.day == tday.day and current_time_ts.hour >= sunrise_ts.hour\
    and current_time_ts <= sunset_ts:
        icon = sun_face
    else:
        icon = clear_night      
elif 'Clouds' in current_forecast: 
    icon = mostly_cloudy   
elif 'Cloudy' in current_forecast: 
    icon = mostly_cloudy
elif 'Rain' in current_forecast:
    icon = rainy
elif 'Thunderstorm' in current_forecast:
    icon = thunder_storm
elif 'Mist' in current_forecast:
    icon = rainy
elif 'Drizzle' in current_forecast:
    icon = rainy
elif 'Snow' in current_forecast:
    icon = snowy
elif 'Sleet' in current_forecast:
    icon = rainy
elif 'Fog' in current_forecast:
    icon = fog 
elif 'Wind' in current_forecast:
    icon = wind 
else:
    print(f'Error: {current_forecast} - has no icon to display')
    icon =  ''

# This will display the phase of the moon    
moon = lunar_phase(tday)

# This displays the Month and Day for each year in the DataFrame
todays_date = pd.to_datetime(tday).strftime('%B %-d')
todays_date = todays_date

# Here I print a title with an weather emoji corresponding to the forecast.
# I also add a moon emoji that corresponds to the moon phase.
high_low = 'High/Low Temps'
uv_index = daily_high_low_2022['UV_INDEX'][0]
current_temperatue = 'Current Temp: ' + str(df2022['TEMP'].tail(1)[0]) + '\u00B0F' 
temp_celsius = ' | ' + str(round((df2022['TEMP'].tail(1)[0] - 32) / 1.8,1)) + '\u00B0C'

# if current_forecast == 'Clear' and  current_time_ts >= sunrise_ts and current_time_ts <= sunset_ts:
#     print(f'{icon} Daily {high_low}' +  f' for {todays_date}{monthly_icon}| {thermometer} {current_temperatue}{temp_celsius} {moon}')

# else:
#     print(f'{icon} Daily {high_low}' +  f' for {todays_date} {monthly_icon}| {thermometer} {current_temperatue}{temp_celsius} {moon}\n')

# Here I chose to print the data frame instead of just displaying it, it's because the data frame 
# is just too small

print('Data Frame Created Successfully!\n') 
print('Convert Data to JSON\n') 
print('Convert Data to JSON Successful\n') 


pd.set_option('colheader_justify', 'center')
# print(df.info())
df.fillna('N/A').to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-Weather/_data/weather1.json')


print('Writing JSON File....\n') 

temperatue = str(df2022['TEMP'].tail(1)[0]) + '\u00B0F' 
temp_celsius = str(round((df2022['TEMP'].tail(1)[0] - 32) / 1.8,1)) + '\u00B0C'
import datetime
todays_date = datetime.date.today().strftime('%B %-d')
temperatue = str(df2022['TEMP'].tail(1)[0]) + '\u00B0F'
temp_celsius = str(round((df2022['TEMP'].tail(1)[0] - 32) / 1.8,1)) + '\u00B0C'
therm = "\U0001F321"

x = f'{icon}  Daily High/Low Temperature for {todays_date} | {thermometer} Current Temp: {str(temperatue)} | {str(temp_celsius)} {moon}'
df['Title'] = x
# print(x)
df.to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-Weather/_data/weather5.json')


df = pd.read_csv('/Volumes/Weather-Data/Weather-Data-2022.csv')
df = df[['SUNRISE','SUNSET','HRS_DAYLIGHT']].tail(1)
df.reset_index(inplace=True)
df.to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-Weather/_data/suntimes.json')

print('Finished!') 
