import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

#need to add ticket data
tickets = pd.read_csv('../csvs/tickets.csv')
tickets.drop(columns=['Total Inflation Adjusted Box Office'], inplace=True)
print(tickets.info())

missing_gross_1 = pd.read_csv('../csvs/Gross_Year_1977-1994.csv')
print(missing_gross_1.info())

tickets = tickets.set_index('Year')
missing_gross_1 = missing_gross_1.set_index('Year')
tickets.loc[1994:1977, 'Total Box Office'] = missing_gross_1.loc[1994:1977,'Total Gross']
tickets.loc[1994:1977, 'Tickets Sold'] = tickets.loc[1994:1977, 'Total Box Office']/tickets.loc[1994:1977, 'Average Ticket Price']
tickets.reset_index(inplace=True)
print(tickets.info())
#save as the intermediary file
tickets.to_csv('../csvs/tickets_1.csv', index=False)

#Now we want to plot to determine how best to fill missing data
filled = tickets.loc[tickets['Year']>1977]
sns.scatterplot(data = filled, x='Year', y='Tickets Sold')
plt.savefig('../graphs/tickets_tixSold_EDA.svg')
sns.scatterplot(data= filled, x='Year', y='Total Box Office')
plt.savefig('../graphs/tickets_boxOffice_EDA.svg')

#Conclusions: Total Box Office has a stronger linear relationship with Year, excluding 2020-2023, Tickets Sold looks like it has a logarithmic relationship with Year, again excluding 2020-2023:
pre_covid = filled.loc[filled['Year']<2020]
print(pre_covid.info())
print(np.corrcoef(pre_covid['Year'], pre_covid['Total Box Office']))

#Nice! correlation coefficient is 0.986, so we should be set for linear regression
slope, intercept, r, p, std_err = stats.linregress(pre_covid['Year'], pre_covid['Total Box Office'])

#write the function for the equation for y
def equationFunc(x):
    return slope*x + intercept
#Now we'll fill in the missing data from before 1977
tickets.loc[tickets['Year']<1977, 'Total Box Office'] = tickets.loc[tickets['Year']<1977, 'Year'].apply(equationFunc)
print(tickets)
plt.clf()
sns.scatterplot(data=tickets, x='Year', y='Total Box Office')


#This doesn't look right- and we're getting not insignificant negative values
predicted_total_box = list(map(equationFunc, pre_covid['Year']))
plt.plot(pre_covid['Year'], predicted_total_box)
plt.show()

#Looks like the data between 1977-1982 is skewing the rest by a bit
#There was a recession in the US which accounts for affect on diminished box office: https://en.wikipedia.org/wiki/Early_1980s_recession_in_the_United_States
#Do it again!
slope, intercept, r, p, std_err = stats.linregress(pre_covid.loc[pre_covid['Year']>=1982, 'Year'], pre_covid.loc[pre_covid['Year']>=1982, 'Total Box Office'])

#Now we'll fill in the missing data from before 1977
tickets.loc[tickets['Year']<1977, 'Total Box Office'] = tickets.loc[tickets['Year']<1977, 'Year'].apply(equationFunc)
print(tickets)
plt.clf()
sns.scatterplot(data=tickets, x='Year', y='Total Box Office')


#This doesn't look right- and we're getting not insignificant negative values
predicted_total_box = list(map(equationFunc, pre_covid['Year']))
plt.plot(pre_covid['Year'], predicted_total_box)
plt.show()

#last value is still negative. Considering the small change in ticket price, think we may be fine to say it's about the same as the year pror
tickets.loc[tickets['Year'] == 1973, 'Total Box Office'] = 161458981.9642334

#one last look
plt.clf()
sns.scatterplot(data=tickets, x='Year', y='Total Box Office')
plt.savefig('../graphs/Total_Box_office_Scatter_EDA.svg')

#fill tickets sold:
tickets.loc[tickets['Year']<1977, 'Tickets Sold'] = tickets.loc[tickets['Year']<1977, 'Total Box Office']/tickets.loc[tickets['Year']<1977, 'Average Ticket Price']
#convert box office and tickets sold to ints
tickets['Tickets Sold'] = round(tickets['Tickets Sold'], 0).astype(int)
tickets['Total Box Office'] = round(tickets['Total Box Office'], 0).astype(int)
print(tickets)

tickets.to_csv('../csvs/tickets_final.csv', index=False)
