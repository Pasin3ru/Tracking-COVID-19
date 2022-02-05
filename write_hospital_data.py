#!/usr/local/bin/python
# Author: RKP
# 2/4/2022

'''
    This programs gets hospital data from ny state website and writes it to a
    html file 
'''

import pandas as pd

hosp = pd.read_csv('https://health.data.ny.gov/resource/jw46-jpb7.csv')
hosp['as_of_date'] = pd.to_datetime(hosp['as_of_date']).dt.strftime("%-b %-d")
hosp = hosp.loc[hosp['facility_county'] == 'WARREN']
print(hosp['facility_name'].values[0].title())
hosp = hosp[["as_of_date", "patients_currently", "patients_newly_admitted",\
            "patients_currently_in_icu", "patients_expired"]]
hosp['patients_newly_admitted'] = hosp['patients_newly_admitted'].astype(int)
hosp['patients_currently'] = hosp['patients_currently'].astype(int)
hosp['patients_currently_in_icu'] = hosp['patients_currently_in_icu'].astype(int)
hosp['patients_expired'] = hosp['patients_expired'].astype(int)
hosp['patients_currently_in_icu'] = hosp['patients_currently_in_icu'].astype(int)
hosp.rename(columns={'as_of_date': 'Date',
                    'patients_currently': 'Patients Currently',
                    'patients_newly_admitted': 'Patients Admitted',
                    'patients_currently_in_icu':'Patients In ICU',
                    'patients_expired':'Patients Expired'}, inplace=True)
hosp.to_html("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_includes/hospital\
-tables/gf_hospital.html", col_space=60, justify="center", index=False)

hosp2 = pd.read_csv('https://health.data.ny.gov/resource/jw46-jpb7.csv')
hosp2['as_of_date'] = pd.to_datetime(hosp2['as_of_date']).dt.strftime("%-b %-d")
hosp2 = hosp2.loc[hosp2['facility_county'] == 'SARATOGA']
print(hosp2['facility_name'].values[0].title())
hosp2 = hosp2[["as_of_date", "patients_currently", "patients_newly_admitted",\
            "patients_currently_in_icu", "patients_expired"]]
hosp2['patients_newly_admitted'] = hosp2['patients_newly_admitted'].astype(int)
hosp2['patients_currently'] = hosp2['patients_currently'].astype(int)
hosp2['patients_currently_in_icu'] = hosp2['patients_currently_in_icu'].astype(int)
hosp2['patients_expired'] = hosp2['patients_expired'].astype(int)
hosp2['patients_currently_in_icu'] = hosp2['patients_currently_in_icu'].astype(int)
hosp2.rename(columns={'as_of_date': 'Date',
                    'patients_currently': 'Patients Currently',
                    'patients_newly_admitted': 'Patients Admitted',
                    'patients_currently_in_icu':'Patients In ICU',
                    'patients_expired':'Patients Expired'}, inplace=True)
hosp2.to_html("/Users/rkp/Jupyter-Notebook/Web-Page/Tracking-COVID-19/_includes/hospital\
-tables/s_hospital.html", col_space=65, justify="center", index=False)
print('File Written Successfully')


