import pandas as pd

pd.set_option('display.max_colwidth', 1000) # <---- This sets the max number characters in a column .
pd.set_option('display.max_columns', 50) # <---- This sets the max number of columns.
pd.set_option('display.max_rows', None)  # <---- Enable to view all rows.

df = pd.read_csv('/Volumes/Weather-Data/Weather-Data-2022.csv')
df.reset_index(drop=True, inplace=True)

df.drop(columns=[

    'DATE',
    'TIME',
    'STATION_ID',
    'CITY',
    'STATE',
    'LATITUDE',
    'LONGITUDE',
    'SNOW',

], axis=0, inplace=True)



temp = str(df['TEMP'].tail(1).values[0]) + '\u00B0F'
baro = dew_point = feels_like = df['BAROMETER'].tail(1).values[0].astype(str) + 'iHg'
dew_point = feels_like = df['DEW_POINT'].tail(1).values[0].astype(str) + '\u00B0F'
feels_like = df['FEELS_LIKE'].tail(1).values[0].astype(str) + '\u00B0F'
humidity = df['HUMIDITY'].tail(1).values[0].astype(str)
sun_rise = df['SUNRISE'].tail(1).values[0]
sun_set = df['SUNSET'].tail(1).values[0]
print(temp)

data = (temp, baro, dew_point, feels_like, humidity, sun_rise, sun_set)
columns = ['temp', 'baro', 'dew_point', 'feels_like', 'humidity', 'sun_rise',  'sun_set']


df2 = pd.DataFrame(zip(columns, data))

df2.T.to_json('/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-Weather/_data/weather1.json')

print(df2.T)
