import pandas as pd
from datetime import datetime

def parseMovies(yr):
    movies = pd.read_csv(f'../csvs/{yr}_movies.csv', usecols=['Release', 'Gross', 'Opening', 'Open'])
    movies.columns=['title', 'domestic_box_office', 'opening_box_office', 'release_date']

    #reformat columns
    movies['domestic_box_office'] = movies['domestic_box_office'].str.strip('$').astype(int)
    movies['opening_box_office'] = movies['opening_box_office'].str.strip('$').astype(int)
    movies['release_date'] = movies['release_date'].str.rstrip()
    movies['release_date'] = pd.to_datetime(movies['release_date'], format="%b %d")
    movies['release_date'] = movies['release_date'].apply(lambda x: x.replace(year=yr))
    movies.to_csv(f'../csvs/{yr}_movies_formatted.csv', index=False)
    return movies


#keeping columns: Release, Gross, Opening, Open, add Franchise Col in both
movies2022 = parseMovies(2022)
print(movies2022.shape)
movies2023 = parseMovies(2023)
print(movies2023.shape)
#concat into one matrix
movies = pd.concat([movies2022, movies2023])
#movies.reset_index(inplace=True)
print(movies.shape)
#Reduce to September -2022 - September 2023 movies
movies = movies[movies['release_date'] >= '2022-09-01']
movies = movies[movies['release_date'] <= '2023-09-30']
print(movies.head(10))
print(movies.info())
print(movies.shape)

#Then cross-reference titles with movies.csv to get the movies we're looking at and their franchises
movies_all_time = pd.read_csv('../csvs/movies.csv', usecols=['title', 'franchise'])
disney_movies = pd.read_csv('../csvs/disney2022-2023.csv', usecols=['title'])
disney_movies['franchise'] = ['Disney']*len(disney_movies['title'])
movies_to_select = pd.concat([movies_all_time, disney_movies])
#we don't actually have duplicates in this combined dataset, so we can proceed to do an inner merge
moviesSep22_23 = movies.merge(right=movies_to_select, how='inner', on='title')
print(moviesSep22_23.head(12))
print(moviesSep22_23.shape)

moviesSep22_23.to_csv('../csvs/2022-2023movies.csv', index=False)
