#!/usr/local/bin/python
# Author: RKP
# 12/12/2020

import math
import datetime 
from text_colors import *
from IPython.display import Image

tday = datetime.date.today()

def lunar_phase(tday):
    month = tday.month
    day = tday.day
    year = tday.year

    ages = [18, 0, 11, 22, 3, 14, 25, 7, 18, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7] 
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]

    description = ['new (totally dark)',
      'waxing crescent (increasing to full)',
      'in it\'s first quarter (increasing to full)',
      'waxing gibbous (increasing to full)',
      'full (full light)',
      'waning gibbous (decreasing from full)',
      'in it\'s last quarter (decreasing from full)',
      'waning crescent (decreasing from full)']

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    if day == 31:
        day = 1

    days_into_phase = ((ages[(year + 1) % 19] +
                        ((day + offsets[month-1]) % 30) +
                        (year < 1900)) % 30)

    # print(days_into_phase)

    # print(day)
    # print((year + 1) % 19)
    # print(ages[(year + 1) % 19])
    # print((day + offsets[month-1]) % 30)
    # print((year < 1900) % 30)

    if days_into_phase == 2:
        days_into_phase += 1

    if days_into_phase == 6:
        days_into_phase += 2

    if days_into_phase == 7:
        days_into_phase += 1

    if days_into_phase == 10:
        days_into_phase += 1

    if days_into_phase == 14:
        days_into_phase += 1

    if days_into_phase == 17:
        days_into_phase += 1

    if days_into_phase == 21:
        days_into_phase += 1

    if days_into_phase == 25:
        days_into_phase += 1

    if days_into_phase == 26:
        days_into_phase += 1

    if days_into_phase == 29:
        days_into_phase = 1

    index = int((days_into_phase + 1) * 16/59) #59.0

    # print(math.ceil(index))  # test
    if index > 7:
        index = 7 # was set to 7
    status = description[index]

    # print(status)
    # light should be 100% 15 days into phase

    # print(days_into_phase)

    light = int(2 * days_into_phase * 100/29)
    if light > 100:
        light = abs(light - 200)
    # print('Light:',light)    
    
    date = '%s %d %d' % (months[month-1],day, year)

    if status == 'new (totally dark)':
        message = 'new'
    if status == 'waxing crescent (increasing to full)':
        message = 'waxing_crescent'
    if status == 'in it\'s first quarter (increasing to full)':
        message = 'first_quarter'
    if status ==  'waxing gibbous (increasing to full)':
        message = 'waxing_gibbous'
    if status == 'full (full light)':
        message = 'full'
    if status == 'waning gibbous (decreasing from full)':
        message = 'waning_gibbous'
    if status == 'in it\'s last quarter (decreasing from full)':
        message = 'last_quarter'
    if status == 'waning crescent (decreasing from full)':
        message = 'waning_crescent'


    # print('Index:',index)
    # print('Light:',light)

    words = message.split(' ')

    emojis = {

        'new':'🌑',
        'waxing_crescent':'🌒',
        'first_quarter':'🌓',
        'waxing_gibbous':'🌔',
        'full':'🌕',
        'waning_gibbous':'🌖',
        'last_quarter':'🌗',
        'waning_crescent':'🌘'
    }

    output = ''
    for word in words:
        output += emojis.get(word, word) + ''
        # return output

    fullmoon_name = {
        'January': 'Wolf Moon',       # 1/28/2021
        'February': 'Snow Moon',      # 2/27/2021
        'March': 'Worm Moon',         # 3/28/2021
        'April': 'Pink Moon',         # 4/26/2021
        'May': 'Flower Moon',         # 5/26/2021
        'June': 'Strawberry Moon',    # 6/24/2021
        'July': 'Buck Moon',          # 7/23/2021
        'August': 'Sturgeon Moon',    # 8/22/2021
        'September': 'Harvest Moon',  # 9/20/2021
        'October': 'Hunters Moon',    # 10/20/2021
        'November': 'Beaver Moon',    # 11/19/2021
        'December': 'Cold Moon'       # 12/18/2021
    }

    moon_discription = {
        
        'Wolf Moon': "The first Full Moon of the year is named after howling wolves. \nIn some cultures, it was known as Old Moon, Ice Moon, Snow Moon, and the Moon after Yule.",

        'Snow Moon': "The February Full Moon is named after the snow on the ground. \nSome Native American tribes named this the Hunger Moon; others called it the Storm Moon.",

        'Worm Moon': "The Full Moon in March is the Worm Moon, and it is usually considered the last Full Moon of winter. \nIt is also called Lenten Moon, Crow Moon, Crust Moon, Chaste Moon, Sugar Moon, and Sap Moon.",

        'Pink Moon': "April 2021's Pink Moon, named after phlox, the pink flowers that bloom in spring, is also a Super Moon. \nOther names for this Full Moon are Sprouting Grass Moon, Fish Moon, Hare Moon, Egg Moon, and Paschal Moon.",

        'Flower Moon': 'The Full Moon in May is known as the Flower Moon. \nOther names include the Corn Planting Moon, and the Milk Moon, while some named it the Hare Moon.',

        'Strawberry Moon': 'The Full Moon in June is called the Strawberry Moon. The wild strawberries that start to ripen during early summer give it it\'s name. Other names of this Full Moon are Rose Moon, Hot Moon, and Mead Moon.',

        'Buck Moon': 'The Full Moon in July is the Buck Moon, named after the new antlers that emerge from a buck\'s forehead around this time of the year. It is also called Thunder Moon, Hay Moon, and Wort Moon.',

        'Sturgeon Moon': 'The Full Moon in August is named after North America\'s largest fish, the lake sturgeon. \nOther names for this Full Moon include Grain Moon, Green Corn Moon, Fruit Moon, and Barley Moon.',

        'Harvest Moon': 'The Full Moon closest to the September equinox is called the Harvest Moon, \nand it is either in September or October.',

        'Hunters Moon': 'October’s Full Moon is the Hunter’s Moon. It is also called Travel Moon, Dying Grass Moon, \nand sometimes Blood Moon or Sanguine Moon.',

        'Beaver Moon': 'The Full Moon in November is named after beavers who build their winter dams at this time of year. \nIt is also called Frost Moon and Mourning Moon, depending on the winter solstice.',

        'Cold Moon': 'In December, winter sets in and the Full Moon is called the Cold Moon. \nIt is also called Long Nights Moon, and the Moon before Yule.'
    }

    moon_month = tday.strftime('%B')
    moon_name = fullmoon_name[moon_month]
    moon_details = moon_discription[moon_name]

    if message == 'full':
        return color.BOLD + '| Moon Phase:' + color.END + f' The Moon is Full {output}'#\n\n{moon_details}' 

        # print(f'\nThe Moon is Full. {moon_details}\n')
    else:    
        word = word.replace('_', ' ')
    
        # print(f'The Moon is {status} {output} Luminosity = {light} % ')

        return color.BOLD + '| Moon Phase:' + color.END + f' {word.title()} {output}'



# lunar_phase(tday)    
   