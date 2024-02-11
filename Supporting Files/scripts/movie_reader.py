import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import corrcoef

#Now we're using self-gathered data
#data types: title:str, release_date:datetime, opening_box_office: int, domestic_box_office: int, franchise: category
movies = pd.read_csv('../csvs/movies.csv', parse_dates=['release_date'], dtype={'franchise':'category'})
#print(movies.dtypes)
#data types: Year:int, Tickets Sold: int, Total Inflation Adjusted Box Office: int, Average Ticket Price: Float
tickets = pd.read_csv('../csvs/tickets_1.csv', parse_dates = ['Year'])
tickets['Year'] = tickets['Year'].dt.year
#print(tickets.dtypes)
movies = movies.sort_values(by='release_date')
#create franchise category type, order so our graphs are always in the same order
franchise_type = pd.CategoricalDtype(['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars'], ordered = True)
movies['franchise'] = movies['franchise'].astype(franchise_type)

#print category counts
print(movies['franchise'].value_counts())
#FIXME: need to add 1970-1976 total box office + tickets sold data (tickets sold can be found by total box office

#merge movies and tickets so we have all dates in one dataframe
movies['Year'] = movies['release_date'].dt.year
#one-to-many merge. Should end up with same number of rows as movies database
moviesntics = movies.merge(tickets, on='Year')
#Now we need to find tickets sold per movie
moviesntics['Tickets Sold by Movie_opening'] = (moviesntics['opening_box_office']/moviesntics['Average Ticket Price']).astype('int')
moviesntics['Tickets Sold by Movie_domestic'] = (moviesntics['domestic_box_office']/moviesntics['Average Ticket Price']).astype('int')

#Now, the dataset for the observations
observations = pd.read_csv('../csvs/RenFaireObservations.csv')
#print(observations.dtypes)
observations_filtered = observations[observations['Media Source'].isin(['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars'])]
#set Media Source col to franchise_type so all graphs have the same order
observations_filtered.loc[:,'Media Source'] = observations_filtered['Media Source'].astype(franchise_type)#FIXME: This line is throwing a warning


#Compare on a few different angles:
#Box office data
#compare from movies around summer 2022 to summer 2023
#compare with 10 + 20 year data trends?


#now get normalization data
#FIXME: delete this next line when we've figured out how to fill missing data in tickets
moviesntics.query('Year > 1976', inplace=True)
moviesntics['normal_tics_domestic'] = moviesntics['Tickets Sold by Movie_domestic']/moviesntics['Tickets Sold']

#set graph customizations
sns.set( rc = {'figure.figsize' : (15, 15)})
sns.set_style('white')
sns.set_palette(sns.color_palette('husl',5))
#Plot normalized data and sum of tickets sold, visual comparison against counts at renaissance faire
g = sns.catplot(data=moviesntics, x='franchise', y='Tickets Sold by Movie_domestic', kind='bar', estimator='sum', errorbar=None, hue = 'franchise')
g.fig.suptitle('Tickets Sold Domestically')
g.fig.subplots_adjust(top = 0.9)
g.set_axis_labels('Franchise','Tickets Sold')
plt.savefig('../graphs/Tickets_Sold_Bar.svg')
plt.clf()
g = sns.catplot(data=moviesntics, x='franchise', y='normal_tics_domestic', kind='bar', estimator='sum', errorbar=None, hue = 'franchise')
g.fig.suptitle('Tickets Sold Domesticly, Normalized')
g.fig.subplots_adjust(top = 0.9) 
g.set_axis_labels('Franchise','Tickets Sold')
plt.savefig('../graphs/Tickets_Sold_Bar_Normal.svg')
plt.clf()
g = sns.catplot(data=observations_filtered, x='Media Source', kind='count', hue = 'Media Source')
g.fig.suptitle('Character Observations')
g.fig.subplots_adjust(top = 0.9) 
g.set_axis_labels('Franchise','Observation Count')
plt.savefig('../graphs/Ren_Faire_Observations_Bar.svg')
plt.clf()

#Then, get 2022-2023 data

#Now I want to compare franchise counts in scatterplots
franchise_counts = pd.DataFrame()
franchise_counts['franchise'] = ['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars']
franchise_counts['Tickets Sold Domestically'] = moviesntics.groupby('franchise', observed=True)['Tickets Sold by Movie_domestic'].sum().values
franchise_counts['Tickets Sold Domestically Normalized'] = moviesntics.groupby('franchise', observed=True)['normal_tics_domestic'].sum().values
franchise_counts['Ren Faire Observations'] = observations_filtered['Media Source'].value_counts(sort=False).values
print(franchise_counts)

#Now do scatterplots
#instances in last year vs instances at ren faire
#tickets sold last year vs instances at ren faire
#tickets sold all time vs instances at ren faire
plt.clf()
g = sns.relplot(data = franchise_counts, x='Ren Faire Observations', y='Tickets Sold Domestically', kind='scatter', hue = 'franchise')
g.fig.suptitle('Tickets Sold Domestically vs\n Ren Faire Observations (2023)')
g.fig.subplots_adjust(top = 0.9) 
g.set_axis_labels('','Tickets Sold total')
plt.savefig('../graphs/Tickets_Sold_vs_RFObs.svg')
print(corrcoef(franchise_counts['Ren Faire Observations'], franchise_counts['Tickets Sold Domestically']))
g = sns.relplot(data = franchise_counts, x='Ren Faire Observations', y='Tickets Sold Domestically Normalized', kind='scatter', hue = 'franchise')
g.fig.suptitle('Tickets Sold Domestically (Normalized) vs\n Ren Faire Observations (2023)')
g.fig.subplots_adjust(top = 0.9) 
g.set_axis_labels('','Tickets Sold (normalized per year)')
plt.savefig('../graphs/Tickets_Sold_Norm_vs_RFObs.svg')
print(corrcoef(franchise_counts['Ren Faire Observations'], franchise_counts['Tickets Sold Domestically Normalized']))
#plt.show()
