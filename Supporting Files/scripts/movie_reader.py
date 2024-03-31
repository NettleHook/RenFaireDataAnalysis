import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import corrcoef

#plotting functions, so I don't have to re-type the code so many times
def plot_bar(data_frame, x_val, y_val, labels, name):
    """
    Plots a bar graph of the x and y columns of the dataframe and saves it to a file

    Parameters:
        data_frame (pandas DataFrame): data we'll be plotting
        x_val (string): name of x column for our graph
        y_val (string): name of y column for our graph
        labels (list): list of labels in the form [x-axis label, y-axis label, title]
        name (string): filename we're saving the file under

    """
    g = sns.catplot(data=data_frame, x=x_val, y=y_val, kind='bar', estimator='sum', errorbar=None, hue = 'franchise')
    g.fig.suptitle(labels[2])
    g.fig.subplots_adjust(top = 0.9)
    g.set_axis_labels(labels[0],labels[1])
    plt.savefig('../graphs/' + name + '.svg')
    plt.clf()
    
def plot_scatter(data_frame, x_val, y_val, labels, name):
    """
    Plots a scatter graph of the x and y columns of the dataframe and saves it to a file

    Parameters:
        data_frame (pandas DataFrame): data we'll be plotting
        x_val (string): name of x column for our graph
        y_val (string): name of y column for our graph
        labels (list): list of labels in the form [x-axis label, y-axis label, title]
        name (string): filename we're saving the file under

    """
    g = sns.relplot(data = data_frame, x=x_val, y=y_val, kind='scatter', hue = 'franchise')
    g.fig.suptitle(labels[2])
    g.fig.subplots_adjust(top = 0.9) 
    g.set_axis_labels(labels[0],labels[1])
    plt.savefig('../graphs/'+name+'.svg')
    print(corrcoef(data_frame[x_val], data_frame[y_val]))

def moviesandticks(movies, tickets):
    """
    Merges a movies dataset with a tickets dataset, and adds columns for the tickets sold per movie data

    Parameters:
        movies (pandas DataFrame): dataframe with the movie data
        tickets (pandas DataFrame): dataframe with the tickets data
    
    """
    #merge movies and tickets
    movies['Year'] = movies['release_date'].dt.year
    #one-to-many merge. Should end up with same number of rows as movies database
    moviesntics = movies.merge(tickets, on='Year')
    assert moviesntics.shape[0] == movies.shape[0]
    #Now we need to find tickets sold per movie
    moviesntics['Tickets Sold by Movie_opening'] = (moviesntics['opening_box_office']/moviesntics['Average Ticket Price']).astype('int')
    moviesntics['Tickets Sold by Movie_domestic'] = (moviesntics['domestic_box_office']/moviesntics['Average Ticket Price']).astype('int')
    #now get normalization data
    moviesntics['normal_tics_domestic'] = moviesntics['Tickets Sold by Movie_domestic']/moviesntics['Tickets Sold']
    return moviesntics

def franchisecounts(movies, observations):
    """
    Merges a movies dataset with our Renaissance Faire Observations, grouping by franchise

    Parameters:
        movies (pandas DataFrame): dataframe with the movie data
        observations (pandas DataFrame): dataframe with the renaissance faire observation data
    
    """
    #Now I want to compare franchise counts in scatterplots
    franchise_counts = pd.DataFrame()
    franchise_counts['franchise'] = ['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars']
    franchise_counts['Tickets Sold Domestically'] = movies.groupby('franchise', observed=True)['Tickets Sold by Movie_domestic'].sum().values
    franchise_counts['Tickets Sold Domestically Normalized'] = movies.groupby('franchise', observed=True)['normal_tics_domestic'].sum().values
    franchise_counts['Ren Faire Observations'] = observations['Media Source'].value_counts(sort=False).values
    return franchise_counts

#Import data
#data types: title:str, release_date:datetime, opening_box_office: int, domestic_box_office: int, franchise: category
movies = pd.read_csv('../csvs/movies.csv', parse_dates=['release_date'], dtype={'franchise':'category'})
movies = movies.sort_values(by='release_date')

#dxata types: Year:int, Tickets Sold: int, Total Inflation Adjusted Box Office: int, Average Ticket Price: Float
tickets = pd.read_csv('../csvs/tickets_final.csv', parse_dates = ['Year'])
tickets['Year'] = tickets['Year'].dt.year

#get last year data
ly_movies = pd.read_csv('../csvs/2022-2023movies.csv', parse_dates=['release_date'])
ly_movies = ly_movies.sort_values(by='release_date')

#create franchise category type, order so our graphs are always in the same order
franchise_type = pd.CategoricalDtype(['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars'], ordered = True)
movies['franchise'] = movies['franchise'].astype(franchise_type)
print(movies['franchise'].value_counts())
ly_movies['franchise'] = ly_movies['franchise'].astype(franchise_type)
print(ly_movies['franchise'].value_counts())

all_movies_tics = moviesandticks(movies, tickets)
ly_movies_tics = moviesandticks(ly_movies, tickets)

#Now, the dataset for the observations
observations = pd.read_csv('../csvs/RenFaireObservations.csv')
observations_filtered = observations[observations['Media Source'].isin(['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars'])]
#set Media Source col to franchise_type so all graphs have the same order
observations_filtered['Media Source'] = observations_filtered['Media Source'].astype(franchise_type)
print(observations_filtered['Media Source'].value_counts(sort = False))

#set graph customizations
sns.set( rc = {'figure.figsize' : (15, 15)})
sns.set_style('white')
sns.set_palette(sns.color_palette('husl',5))

#Plot normalized data and sum of tickets sold, visual comparison against counts at renaissance fair
plot_bar(all_movies_tics, 'franchise', 'Tickets Sold by Movie_domestic', ['Franchise', 'Tickets Sold', 'Tickets Sold Domesticly'], 'Tickets_Sold_Bar')
plot_bar(all_movies_tics, 'franchise', 'normal_tics_domestic', ['Franchise', 'Tickets Sold', 'Tickets Sold Domesticly, Normalized'], 'Tickets_Sold_Bar_Normal')
plot_bar(ly_movies_tics, 'franchise', 'Tickets Sold by Movie_domestic', ['Franchise', 'Tickets Sold', 'Tickets Sold Domesticly, 2022-2023'], 'Tickets_Sold_Bar_2022-2023')
plot_bar(ly_movies_tics, 'franchise', 'normal_tics_domestic', ['Franchise', 'Tickets Sold', 'Tickets Sold Domesticly, Normalized, 2022-2023'], 'Tickets_Sold_Bar_Normal_2022-2023')

g = sns.catplot(data=observations_filtered, x='Media Source', kind='count', hue = 'Media Source')
g.fig.suptitle('Character Observations')
g.fig.subplots_adjust(top = 0.9)
g.set_axis_labels('Franchise','Observation Count')
plt.savefig('../graphs/Ren_Faire_Observations_Bar.svg')
plt.clf()

franchise_counts_all = pd.DataFrame()
franchise_counts_all['franchise'] = ['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars']
franchise_counts_all['Tickets Sold Domestically'] = all_movies_tics.groupby('franchise', observed=True)['Tickets Sold by Movie_domestic'].sum().values
franchise_counts_all['Tickets Sold Domestically Normalized'] = all_movies_tics.groupby('franchise', observed=True)['normal_tics_domestic'].sum().values
franchise_counts_all['Ren Faire Observations'] = observations_filtered['Media Source'].value_counts(sort=False).values
#print(franchise_counts_all)

print('Making franchise counts dataframe for last year\'s data')
franchise_counts_ly = pd.DataFrame()
franchise_counts_ly['franchise'] = ['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars']
print(ly_movies_tics.groupby('franchise', observed=False)['Tickets Sold by Movie_domestic'].sum())
franchise_counts_ly['Tickets Sold Domestically'] = ly_movies_tics.groupby('franchise', observed=False)['Tickets Sold by Movie_domestic'].sum().values
print(ly_movies_tics.groupby('franchise', observed=False)['normal_tics_domestic'].sum())
franchise_counts_ly['Tickets Sold Domestically Normalized'] = ly_movies_tics.groupby('franchise', observed=False)['normal_tics_domestic'].sum().values
#print(observations_filtered[observations_filtered['Media Source'].isin(['DC', 'Disney', 'Marvel'])]['Media Source'].value_counts(sort=False))
#franchise_counts_ly['Ren Faire Observations'] = observations_filtered[observations_filtered['Media Source'].isin(['DC', 'Disney', 'Marvel'])]['Media Source'].value_counts(sort=False).values
franchise_counts_ly['Ren Faire Observations'] = observations_filtered['Media Source'].value_counts(sort=False).values
franchise_counts_ly['Last Year Movie Release Counts'] = ly_movies_tics['franchise'].value_counts(sort=False).values
print(franchise_counts_ly)

#Now do final comparisons
#instances in last year vs instances at ren faire
plot_scatter(franchise_counts_ly, 'Ren Faire Observations', 'Last Year Movie Release Counts',\
             ['Renaissance Faire Observations', 'Movies Released per Franchise', 'Last Year Movie Release Counts vs Ren Faire Observations'], '22-23_Release_counts_vs_RFObs')
#[[ 1. 0.855955][0.855955  1.        ]]

#tickets sold last year vs instances at ren faire
plot_scatter(franchise_counts_ly, 'Ren Faire Observations', 'Tickets Sold Domestically',\
             ['Renaissance Faire Observations','Tickets Sold total', 'Tickets Sold Domestically(2022-2023) vs\n Ren Faire Observations (2023)'], 'Tickets_Sold_vs_RFObs(2022-2023)')
#[[ 1.         0.32403274][0.32403274  1.        ]]
plot_scatter(franchise_counts_ly, 'Ren Faire Observations', 'Tickets Sold Domestically Normalized',
             ['Renaissance Faire Observations', 'Tickets Sold (normalized per year)', 'Tickets Sold Domestically (Normalized, in 2022-2023) vs\n Ren Faire Observations (2023)'],\
             'Tickets_Sold_Norm_vs_RFObs(2022-2023)')
#[[ 1.         0.33429642][0.33429642  1.        ]]

#tickets sold all time vs instances at ren faire
plot_scatter(franchise_counts_all, 'Ren Faire Observations', 'Tickets Sold Domestically',\
             ['Renaissance Faire Observations','Tickets Sold total', 'Tickets Sold Domestically vs\n Ren Faire Observations (2023)'], 'Tickets_Sold_vs_RFObs')
#[[1.         -0.47053704][-0.47053704 1.        ]]

plot_scatter(franchise_counts_all, 'Ren Faire Observations', 'Tickets Sold Domestically Normalized',\
             ['Renaissance Faire Observations', 'Tickets Sold (normalized per year)', 'Tickets Sold Domestically (Normalized) vs\n Ren Faire Observations (2023)'],\
             'Tickets_Sold_Norm_vs_RFObs')
#[[1.         -0.4731117][-0.4731117 1.        ]]
#Curious about the previous graph, without the Lord of the Rings data:
plot_scatter(franchise_counts_all[franchise_counts_all['franchise'].isin(['DC','Disney', 'Marvel', 'Star Wars'])], 'Ren Faire Observations', 'Tickets Sold Domestically Normalized',\
             ['Renaissance Faire Observations (Modified)', 'Tickets Sold (normalized per year)', 'Tickets Sold Domestically (Normalized) vs\n Ren Faire Observations (2023, modified list)'],\
             'Tickets_Sold_Norm_Modified_vs_RFObs')
#[[ 1.         -0.96627727][-0.96627727  1.        ]]
