#!/usr/local/bin/python
# Author: RKP
# 3/17/2021

# Import Modules.
import os
import requests
from pprint import pprint
from datetime import datetime
from text_colors import *



#                                 DO NOT ALTER
# This file is needed for Jupyter Notebook: My_Weather_Year_by_Year.

# Here I am logging on to https://openweathermap.org/ to get current weather data.
city = 'Glens Falls'
weather_url = os.environ.get('WEATHER_URL')
url = weather_url.format(city)

# Process Weather Data.
res = requests.get(url)
data = res.json()
# pprint(data)

sunrise = data['sys']['sunrise']
sunset = data['sys']['sunset']

# I wanted to show a different emoji for day or night so I had to create these timestamps 
# to be able to compare times as an object instead of a string.

sunrise_ts = datetime.fromtimestamp(sunrise)
sunset_ts = datetime.fromtimestamp(sunset)
current_time_ts = datetime.now()

sun_rise = sunrise_ts.strftime('%-I:%M %p')
sun_set = sunset_ts.strftime('%-I:%M %p')
hrs_daylight = round((sunset - sunrise) / 3600,1)

sun_rise = color.BOLD + sun_rise + color.END 
sun_set = color.BOLD + sun_set + color.END 
hrs_daylight = color.BOLD + str(hrs_daylight) + color.END 


# print(sunshine)