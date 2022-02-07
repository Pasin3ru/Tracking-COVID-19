import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates


fig = plt.figure(figsize=(20,10), dpi=25)

ax_1 = fig.add_subplot(2,1,1)

label_size = 12
font_size = 12
title_font_size = 14

hos = pd.read_csv('https://health.data.ny.gov/resource/jw46-jpb7.csv')
hos['as_of_date'] = pd.to_datetime(hos['as_of_date'])
blankIndex=[''] * len(hos) # <---- Hide row number
hos.index=blankIndex
hos = hos.loc[hos['facility_county'] == 'WARREN']
hos['patients_newly_admitted'] = hos['patients_newly_admitted'].astype(int)
hos_name = str(hos['facility_name'].tail(1).values[0]).title()

x = hos['as_of_date'].values
y = hos['patients_newly_admitted'].values

ax_1.set_ylabel('Patients Admitted', fontsize=font_size, color='black', labelpad=10)
ax_1.set_xlabel('', fontsize=font_size, color='black', labelpad=14)
ax_1.tick_params(axis='x', which='major', labelsize=label_size, length=10, colors='black')
ax_1.tick_params(axis='y', which='major', labelsize=label_size, colors='black', length=10)
ax_1.tick_params(axis='y', which='minor', labelsize=label_size, colors='black', length=8)
ax_1.xaxis.set_major_formatter(mpl_dates.DateFormatter('%A\n%b %-d'))
ax_1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: '{:,}'.format(int(x))))
# ax_1.margins(x=0.002)

ax_3 = ax_1.twinx()
ax_3.set_ylabel('Patients Admitted', fontsize=font_size, color='black', labelpad=10)
ax_3.set_xlabel('', fontsize=font_size, color='black', labelpad=14)
ax_3.tick_params(axis='x', which='major', labelsize=label_size, length=10, colors='black')
ax_3.tick_params(axis='y', which='major', labelsize=label_size, length=10, colors='black')
ax_3.tick_params(axis='y', which='minor', labelsize=label_size, length=8, colors='black')
ax_3.xaxis.set_major_formatter(mpl_dates.DateFormatter('%A\n%b %-d'))
ax_3.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: '{:,}'.format(int(x))))
# ax_3.margins(x=0.002)

ax_1.bar(x, y, color='blue', alpha=1, linewidth=1, width= -0.8, align='center')
ax_3.bar(x, y, color='blue', alpha=1, linewidth=1, width= -0.8, align='center')

plt.grid(which='both', color='gray', alpha=0.1)

plt.title(f'Patients Admitted to {hos_name} with COVID-19', fontweight='bold', fontsize=title_font_size, pad=20, color='black')

for i, v in enumerate(y):
    plt.text(x[i] - 0, v - 1.2, '+' + str(v), color='white', fontsize=16, fontweight='bold', ha='center')

if __name__ == '__main__':
    plt.show()