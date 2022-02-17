#!/usr/local/bin/python
# Author: RKP

import datetime
from dateutil.relativedelta import relativedelta

now = datetime.datetime.now().strftime("%A, %B %-d, %Y | %-I:%M %p")
tday = datetime.date.today()
start_date = datetime.date(2019,5,7)
rdelta = relativedelta(tday, start_date)
years = rdelta.years
months = rdelta.months
weeks = rdelta.weeks
days = rdelta.days
day = ((weeks % 7) + 1) 

def project_runtime():

    if years > 1 and months > 1 and days > 1:
        print(f'Project Runetime: {years} years, {months} months and {days} days')

    if years > 1 and months == 1 and days == 1:
        print(f'Project Runetime: {years} years, {months} month and {days} day')

    if years > 1 and months == 1 and days > 1:
        print(f'Project Runetime: {years} years, {months} month and {days} days')

    if years > 1 and months > 1 and days == 1:
        print(f'Project Runetime: {years} years, {months} months and {days} day')

    if years > 1 and months == 0 and days == 1:
        print(f'Project Runtime: {years} years and {day} day')

    if years > 1 and months == 0 and days > 1:
        print(f'Project Runetime: {years} years and {days} days')

    # if years > 1 and months == 0 and weeks == 1 and day > 1:
    #     print(f'Project Runetime: {years} years, {weeks} week and {day} days')

    # if years > 1 and months == 0 and weeks > 1 and day > 1:
    #     print(f'Project Runetime: {years} years, {weeks} weeks and {day} days')

    if years >= 1 and months == 1 and days == 0:
        print(f'Project Runtime: {years} years and {months} month')

    if years > 1 and months > 1 and days == 0:
        print(f'Project Runtime: {years} years and {months} months')
    
    if years > 1 and months == 0 and days == 0:
        print(f'Project Runetime: {years} years')

    print(f'Last Update: {now}')
    # print(years)
    # print(months)
    # print(days)
    

# project_runtime()
