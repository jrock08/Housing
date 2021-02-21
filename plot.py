import pandas
import seaborn
import pdb
import matplotlib.pyplot as plt

births = pandas.read_excel('births.xls')
housing_starts = pandas.read_excel('housing_starts.xls')

housing_starts['smoothed'] = housing_starts['smoothed']*1000
housing_starts['Total'] = housing_starts['Total']*1000

#fig,ax = plt.subplots()
#ax.plot(births['Year'], births['Births'], color='blue', marker='o')
#ax.set_xlabel("year",fontsize=14)
#ax.set_ylabel("Births",color="blue",fontsize=14)
#
#ax2=ax.twinx()
#ax2.plot(housing_starts['Year'] - 18, housing_starts['smoothed'], '-r')
#ax2.set_ylabel("Housing Starts (year + 18)", color="red", fontsize=14)
#ax2.plot(housing_starts['Year'] - 18, housing_starts['Total'], 'xr')
#
#plt.show()

year_range = [1959, 2020]
offset = 18

births_1990 = births[(births['Year'] > year_range[0]-offset) & (births['Year'] < year_range[1]-offset)]
births_1990['Births_csum'] = births_1990['Births'].cumsum()
housing_1990 = housing_starts[(housing_starts['Year'] > year_range[0]) & (housing_starts['Year'] < year_range[1])]
housing_1990['Starts_csum'] = housing_1990['Total'].cumsum()

fig,ax = plt.subplots()
ax.plot(births_1990['Year'] + offset, births_1990['Births_csum']/2, color='blue', marker='o', label='People/2 reaching maturity')
ax.set_xlabel("year",fontsize=14)

ax.plot(housing_1990['Year'], housing_1990['Starts_csum'], '-xr', label='housing starts')


births_1990['Year'] += offset
combined = pandas.concat([housing_1990.set_index('Year'), births_1990.set_index('Year')], axis=1).reset_index()
combined['debt'] = combined['Total'] - combined['Births']/2
combined['debt_csum'] = combined['debt'].cumsum()

ax.plot(combined['Year'], -combined['debt_csum'], '-k', label='cumulative missing housing')

plt.legend()

plt.show()

