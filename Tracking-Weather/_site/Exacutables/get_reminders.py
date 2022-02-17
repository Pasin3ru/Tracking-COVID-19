#!/usr/local/bin/python

import datetime
import icalendar
from icons import *

# So my thoughts are I will pass the function the name of the file
# I want to use.
def get_reminders(file):
    icalfile = open(file, 'rb')
    gcal = icalendar.Calendar.from_ical(icalfile.read())                                                   

    output = [] 

    for component in gcal.walk():                                                                          
        if component.name == "VEVENT":                                                                     
            summary = component.get('summary')                                                             
            startdt = component.get('dtstart').dt                                                          
            output.append([startdt, str(summary)])   
        
    sorted_output = sorted(output, key=lambda x: x[0])

    tday = datetime.datetime.now()
    # print(tday.month)
    
    # Create a time delta 
    tdelta = datetime.timedelta(days=0)# Pass in a duration
    
    # print(tday + tdelta)
    tday = tday + tdelta

    # Print a list of events
    # for i in sorted_output:
    #     print(i[1])
    # print('My Reminders:\n')

    for startdt, summary in sorted(sorted_output):
        if startdt.date() >= tday.date():
            till_event = startdt - tday

            # Add emojis here

            if 'St. Patrick\'s' in summary:
                icon = shamrock
            if 'Daylight Savings' in summary:
                icon = clock
            if 'Birthday' in summary:
                icon = birthday
            if 'Easter' in summary:
                icon = easter
            if 'Spring' in summary:
                icon = spring
            if 'Flag' in summary:
                icon = us_flag
            if 'Memorial' in summary:
                icon = us_flag
            if 'Earth' in summary:
                icon = earth_day
            if 'Mother\'s' in summary:
                icon = blossom
            if 'Independence' in summary:
                summary = f'{summary} {us_flag}'
                icon = us_flag
            if 'April Fools' in summary:
                icon = april_fools
            if 'Palm' in summary:
                icon = party_popper
            if 'Good' in summary:
                icon = smile
            if 'Passover' in summary:
                icon = cross

            # Display Today's
            if  startdt.date() == tday.date():
                if summary == 'Daylight Savings Time Begins':
                    summary = f'{summary[0:28]} Today {clock}'
                    print(f'{summary}')
                else:
                    print(f'Today is {summary} {icon}')

            # Display Tommorow   
            if till_event.days == 0:
                if 'Daylight Savings Time Begins' in summary:
                    summary = f'{summary[0:28]} Tomorrow {clock}'
                    print(f'{summary}')
                else:
                    print(f'Tomorrow is {summary} {icon}')

            # Display Untill   
            if till_event.days < 7 and till_event.days >= 1:
                print(f'There are {str(till_event.days + 1)} more days untill {summary} {icon}')
            
           
           
         
get_reminders('my_holidays.ics')

  