# Can we Predict What People will Cosplay as at a Renaissance Faire Based on Domestic Box Office Data?

## Table of Contents

|Section|Subsections|
|---|---|
|[Quick Summary](#quick-summary)||
|[Goal](#goal)||
|[The Data](#the-data)|[Renaissance Faire Data](#renaissance-faire-data), [Movie Data](#movie-data), [Ticket Data](#ticket-data), [2022-2023 Data](#2022-2023-data)|
|[Analysis and Methods](#analysis-and-methods)|[Justification behind Limiting the Dataset by Franchise](#justification-behind-limiting-the-dataset-by-franchise), [Defining Popularity for Analysis](#defining-popularity-for-analysis), [Reasons for Time-Based analysis](#reasons-for-time-based-analysis), [General Analysis Approach](#general-analysis-approach)|
|[Results](#results)||
|[Conclusions](#conclusions)||

## Quick Summary

### Project 1

#### Hypothesis for Project 1

Popularity of a theater release, indicated as tickets sold, can be used to predict what people would cosplay as at the Renaissance Faire during a Superhero and Villains theme week.

#### Process for Project 1

Focusing on specific Disney movies, DC, Marvel, Star Wars, Lord of the Rings movies, we collect all the domestic box office revenue and the release dates. We use the release dates to find the average ticket price per year. Next, we divide revenue by average ticket price to get tickets sold for that movie. We also get normalization data by dividing the tickets sold for the movie by the tickets sold that year. This is to account for any economic limitations. Both are then compared to the observations of cosplay counts in 2023.

#### Results for Project 1

![Scatter plot comparing tickets sold domestically to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_vs_RFObs.svg)
The tickets sold were summed across franchises. The correlation coefficient between these is -0.47.  

![Scatter plot comparing tickets sold domestically, normalized by year, to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_Norm_vs_RFObs.svg)
The normalization values were summed across franchises. The correlation coefficient between these is -0.47.  

#### Conclusion for Project 1

We see that there really isn't a strong relationship between domestic box office success and people choosing to cosplay from that franchise at the Renaissance Faire, whether or not we normalize the ticket data. This implies that another factor would be a better determinant for how likely people are to cosplay from a specific franchise.

### Project 2

#### Hypothesis for Project 2

 We can predict from instances of a franchise and tickets sold in the year before the renaissance faire in question  what people would cosplay as at the Renaissance Faire during a Superhero and Villains theme week.

#### Process for Project 2

Collecting data from all movie releases in 2022 and 2023, we then cleaned and filtered to only include movies that were released in theaters between September 1, 2022 and September 30, 2023. Then we merge datasets to make sure we're only keeping movies from 2022 and 2023 that are in the franchises we are looking at (DC, Disney, Marvel, Star Wars, and Lord of the Rings). Now we do a similar analysis that we did in Project 1 with the all-time movie data, where we use the tickets dataset to get the tickets sold per movie and normalize it before comparing to the Renaissance Faire observations. We also compared the number of releases per franchise in this time frame to the Renaissance Faire observations, to see if a franchise having more releases meant it was likelier to have more people cosplaying from it.

#### Results for Project 2

![Scatter plot comparing number of releases per franchise in 2022-2023 to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/22-23_Release_counts_vs_RFObs.svg)
The correlation coefficient is 0.86.

![Scatter plot comparing tickets sold domestically in 2022-2023, normalized by year, to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_vs_RFObs(2022-2023).svg)
The correlation coefficient is 0.32.

![Scatter plot comparing tickets sold domestically in 2022-2023 to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_Norm_vs_RFObs(2022-2023).svg)
The correlation coefficient is 0.33.  

#### Conclusion for Project 2

Again the correlation coefficient is pretty low for tickets sold. It seems the past year's box office success also does not have a strong relationship with people choosing to cosplay from the franchise at the Renaissance Faire as well. Interestingly, releases from a franchise does appear to be strongly correlated with Renaissance Faire cosplays, implying that recent exposure may be a strong factor in what someone decides to cosplay as.

## Goal

The purpose of this analysis was to see if it might be possible to determine what people might cosplay at a Heroes and Villain themed week at my local Renaissance Faire.  
Since my friend and I have gotten full- time jobs, and after she's moved a bit further away, we've been trying to go to the Renaissance Faire every year. Our first trip together was in 2021, which also happened to coincide with their Heroes and Villain theme week. That year, the TV Show Loki had come out, and when we visited, I noticed that about half of all people who had dressed in theme were dressed as either Loki, or one of the multiverse variants introduced in that show.
This piqued my curiosity about whether it would be possible to predict what people would cosplay as based off of general popularity of franchises, but specifically recent releases prior to the Renaissance Faire. I didn't gather data that year, and in 2022 we didn't go during the Heroes and Villain theme week. We did return for that week in 2023, which is when the data I've used for this analysis is from.  
Ultimately, the questions we're hoping to answer are the following:

- Do movie releases in the year before this renaissance faire predict what costumes we see?

- Does the all-time popularity of these franchises predict what costumes we see?

## The Data

### Renaissance Faire Data

The Renaissance Faire data was gathered from a list of observations I made when I visited during 2023. There are some limitations with the accuracy of this data, which are as follows:

- My priority in visiting the Renaissance Faire was to have fun, rather than to observe total instances of costumes, so it's very likely I missed some cosplayers

- As a continuation of the previous point, I am of legal age and fond of cider, so I was tipsy for a not insignificant portion of the faire, which would have further inhibited my ability to notice cosplayers

- I am limited to only observing what I was able to recognize. There were some costumes that looked like they could be a specific character to me, but I wouldn't know who they were, so they weren't noted.

After the observations were gathered, I built a list from them, and used a switch statement to add various facts I thought may be useful to this analysis project and possible to some future projects. The final columns in the pandas dataframe were:
|Column Name| Description|
|---|---|
|Character| The name of the character|
|Media Source| The franchise from which the character came|
|Gender| Observed gender of the character|
|Year| For all this data, it's just 2023. I hoped in the future if I visit during this week, I might add more observations|

The script to form the csv from the observations is file `RenFaireSuperheroes.py`, which creates the csv `RenFaireObservations.csv`
The Observation data contains more data than what was ultimately used. I decided to only examine movie theater data, to ensure the scope of the project wouldn't be too big, and because expanding to video games, TV shows, and streaming would make it much harder to find a common metric to use as the definition of popularity.
The franchises I observed were Star Wars, Disney (Robin Hood, Shrek, Hercules), Marvel, DC, My Hero Academia, Legend of Zelda, Genshin Impact, Lord of the Rings, Princess Bride.
Due to the decision to focus on movie series, this list was reduced to Star Wars, Disney (Robin Hood, Shrek, Hercules), Marvel, DC, and Lord of the Rings (LOTR), for the purposes of the final data analysis. More details on this decision can be found [here](#justification-behind-limiting-the-dataset-by-franchise)

### Movie Data

For the next dataset, I searched for all the movies within a franchise, and copied their information into a csv. The exception to this was Disney movies, as including all of their movies would obscure all the other data, due to the sheer amount of them. For Disney movies, I only included those we observed people dressing as characters from -  Robin Hood, Hercules, and the Shrek series. Of course, this means introducing another dataset later, when I'm checking the preceding year's theatrical releases.
The data focuses on domestic releases in order to get as close to local data as is feasible. I also only noted data for the initial release, in the cases where movies were re- run a few years later. This seemed to be the easiest way to measure the success of a movie without accounting for any re- releases that may be done.
Failings of this approach include the inability to account for cult classics, doesn't account for the effects re- watchability has on popularity, and that movies people really liked are more likely to be rewatched many years after the fact.
Here is the column data for the `movies.csv` file, which contains the data gathered:
|Column Name| Description|
|---|---|
|name| title of the movie|
|release_date| Date of initial release. Due to lack of information, this isn't always the domestic release date|
| opening_box_office | opening weekend box office revenue. This information isn't necessarily domestic|
| domestic_box_office | box office revenue the film made during its initial run in theaters, domestically|
|franchise| the franchise it belongs too from the list: DC, Disney, Marvel, LOTR, Star Wars|

Data Source: <https://www.boxofficemojo.com/>

### Ticket Data

Because I chose to use tickets sold as the metric for [popularity](#defining-popularity-for-analysis), I also needed a dataset with ticket prices to help calculate the tickets sold per movie.
The dataset has the following columns;
|Column Name| Description|
|---|---|
|Year| year|
|Tickets Sold| total tickets sold that year|
|Total Box Office| Box Office revenue for that year|
|Avg. Ticket Price| Average price of tickets that year, not accounted for inflation|

Our first dataset only had information as early as 1995, but we needed information as early as 1970.
All data reflects domestic box office numbers.
Data Sources:

- <https://www.the-numbers.com/market/> (yielded the 1995- 2023 information)

- <https://finance.yahoo.com/news/cost-movie-ticket-were-born-155153039.html> (yielded the - 1994 average ticket prices)

- <https://www.boxofficemojo.com/year/?ref_=bo_nb_hm_secondarytab> (1977- 1994 Total Box Office revenue)

- A linear regression model was used to find the remaining missing Total Box Office Revenue.

- To fill in the missing Total Tickets Sold, I was able to calculate total tickets sold that year by dividing total box office revenue by average ticket price.
`tickets.py` is the file showing the steps taken to go from the initial dataset obtained from the Numbers.com to the dataset we ultimately used in our analysis. Additionally, `tickets.csv` is the original dataset, `tickets_1.csv` is the intermediary, before we did the linear regression, and `tickets_final.csv` is the final result that I used in my analysis.

### 2022-2023 Data

For the this dataset, I started with a complete dataset containing all movies released in 2022, and a complete dataset containing all movies in 2023. These were obtained from the boxofficemojo.com website. The `2022-2023_movies.py` file reformats the data in these datasets to data types we can work with, filters for movies released between September 1, 2022 and September 30, 2023, and finally uses an inner merge with our main movie dataset and a dataset containing disney animated movie titles released in 2022 and 2023 so we can filter for only the movies relevant to the franchises we're examining.
Here is the column data for the `2022-2023movies.csv` file, which contains the data gathered:
|Column Name| Description|
|---|---|
|name| title of the movie|
|release_date| Date of initial release. Due to lack of information, this isn't always the domestic release date|
| opening_box_office | opening weekend box office revenue. This information isn't necessarily domestic|
| domestic_box_office | box office revenue the film made during its initial run in theaters, domestically|
|franchise| the franchise it belongs too from the list: DC, Disney, Marvel, LOTR, Star Wars|

Data Sources:

- <https://www.boxofficemojo.com/> for the 2022 and 2023 data

- <https://en.wikipedia.org/wiki/List_of_Walt_Disney_Studios_films_(2020%E2%80%932029)> for the information about Disney animated films released in 2022 and 2023

## Analysis and Methods

### Justification behind Limiting the Dataset by Franchise

While at the Renaissance Faire, I noticed characters from movies, comics, video games, and TV Shows, I ultimately decided to only focus on movies released in theater. The primary reason for this was the availability of box office data and theater ticket pricing was far easier to find than data from streaming platforms such as Netflix and Disney+. It was also harder to find any download data about video games. The other main reason to focus only on box office data would be avoiding the difficulty introduced when quantifying popularity in a way that is comparable between different types of media.
If I wanted to compare video game download instances (assuming I could find it) to times a movie was seen in theaters, these wouldn't necessarily be comparable. Video Games are more expensive that theater tickets in many cases, and in some cases video games can be installed in multiple places at no additional cost. How would we compare these two metrics, and how would we relate these to popularity?
Furthermore, because of the way I am measuring popularity, it's not effective for works that aren't serialized. As a result, Princess Bride unfortunately had to be dropped from consideration.
To conclude, in order to  keep the scope of my project manageable, make sure my datasets were easier to find, and to ensure I could establish only one metric of 'popularity', I chose to focus my analysis on box office data for semi- serialized movies.

### Defining Popularity for Analysis

As we are using 'popularity' to see if we can predict cosplays at Heroes and Villains Week at my local Renaissance Faire, I needed to begin by defining what the popularity metric would be in this case. Ultimately, I decided tickets sold normalized per year would be the metric I used.
Reasons for this:

- In the context of initial theatrical release, box office revenue or tickets sold would be the best metrics of how well the movie performed among people

- Using tickets sold means I don't have to account too much for how inflation affected prices.

- Due to the effect of covid and post- covid on theater attendance, I wanted to use the normalized values, as that would more accurately demonstrate the movies relative success, and remove any penalty movies released in this theater would have in comparison to movies released pre- covid.

### Reasons for Time-Based analysis

There are two questions, split on the time axes. In one question, I hoped to determine if releases in the past year would predict cosplays seen. My idea behind this is that having recent exposure to an instance of a franchise will place both the notion of that franchise and the memory of loving previous iterations in your mind enough that when it comes time to planning your costume for the Renaissance Faire, you might decide to use that as inspiration.
To clarify, I mean that if Disney produced a new movie this year that you see, you might remember “Oh, I really loved Shrek!” and a few months down the line, when it comes time for you to start planning your costume, you'll remember thinking about Shrek, and might consider that as the inspiration for the costume.
As anecdotal evidence of this, I did watch Blue Beetle when it came out in the summer of 2023, and it did make me think about possibly doing a Batgirl- inspired Renaissance Faire costume. Ultimately, the decision not to was only due to an external influence (previous commitment to be a pirate with my friend), so I felt that there was sufficient evidence that nostalgia can fuel cosplay choices.
Of course, the nostalgia being fuel for the inspiration is dependent on you actually liking the franchise in the first place, which is why I think it's still important to examine all- time popularity of a franchise as a potential measure of the likelihood of people cosplaying from that franchise.
These are the justifications behind examining both all- time data, and the data from within the past year.

### General Analysis Approach

We begin by importing the movies data set from the `movies.csv` file, the last year movie data set from `2022-2023_movies.py`, and the tickets dataset from the `tickets_1.csv` file. The data in these three is explained in section the [Movie Data](#movie-data), [2022-2023 Data](#2022-2023-data), and [Ticket Data](#ticket-data) sections.
Next, we do a bit of dtype formatting. I need to get the year from the `release_date` column of the movies and 2022-2023 movies dataset, because I intend to merge these two datasets with the tickets dataset.
My code includes the `franchise` counts, because I wanted to see the general entry breakdown before we began.
From here, we do the same steps with the dataset that contains all movie data, and the dataset that contains 2022-2023's movie data. Both will be referred to as the 'movie' dataset.
Now, we merge the movie datasets and the ticket dataset on the `Year` column. We need to get the tickets sold per movie by dividing `Avg. Ticket Price` by `domestic_all`. This creates the column `Tickets Sold by Movie_domestic`. Next, we create a new column, called `normal_tics_Opening`, containing the normalized data, by dividing the tickets sold per movie by `Tickets Sold`. As a reminder, we want to compare using the normalized data to diminish any penalties caused by covid and post- covid (lack of) theater attendance.  

The next step is to import the observation data from `RenFaireObservations.csv`. I've already explained in [this section](#justification-behind-limiting-the-dataset-by-franchise) why I'm limiting the data to just DC, Disney, LOTR, Marvel, and Star Wars franchises, so we filter the dataset to only contain those franchises next.

Now that the datasets are ready, I can start doing the comparisons to see if the normalized ticket sales reflect cosplays seen at the Renaissance Faire.

## Results

I made bar graphs of the general data distributions, so we could examine visually if they seem to compare.
![Bar graph indicating tickets sold across franchises](/Supporting%20Files/graphs/Tickets_Sold_Bar.svg)  
![Bar graph indicating tickets sold across franchises, with tickets sold normalized by year](/Supporting%20Files/graphs/Tickets_Sold_Bar_Normal.svg)  
![Bar graph indicating tickets sold across franchises, for September 2022- September 2023](/Supporting%20Files/graphs/Tickets_Sold_Bar_2022-2023.svg)  
![Bar graph indicating tickets sold across franchises, with tickets sold normalized by year, for September 2022- September 2023](/Supporting%20Files/graphs/Tickets_Sold_Bar_Normal_2022-2023.svg)  
![Bar graph showing cosplay observations by franchise](/Supporting%20Files/graphs/Ren_Faire_Observations_Bar.svg)  

We can already see that these don't seem to match up, though interestingly Tickets Sold for all movies matches better than Tickets Sold Normalized for all movies to the Character Observations bar graph.

For the September 2022-2023 data, The two graphs look pretty similar. Neither appear to be similar to the Renaissance Faire Observations for this same year

That being said, this is just an initial look at the tickets sold data and how it compares to our observations at the 2023 faire.

We can better see if there's any relationship between these values using scatterplots.
Here are the scatterplots comparing 'all-time' tickets sold to Ren Faire observations:

![Scatter plot comparing tickets sold domestically, normalized by year, to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_vs_RFObs.svg).

The tickets sold were summed across franchises. The correlation coefficient between these is -0.47.  
And the same graph, where the tickets sold have been normalized based off all tickets sold that year:

![Scatter plot comparing tickets sold domestically to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_Norm_vs_RFObs.svg).
The normalization values were summed across franchises. The correlation coefficient between these is -0.47.

I also compared the Renaissance Faire Observations to just the last year's data.
First, I compared Renaissance Faire instances against the number of releases per franchise:  
![Scatter plot comparing number of releases per franchise in 2022-2023 to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/22-23_Release_counts_vs_RFObs.svg)  
Due to the uniform distribution of the observations, we could not calculate the correlation coefficient. In any case, the relationship between these is as good as random.  
Next I did the same comparisons as with the all-time movie data.  
Here is the 2022-2023 tickets sold by franchise compared to the Renaissance Faire Observations:
![Scatter plot comparing tickets sold domestically in 2022-2023, normalized by year, to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_vs_RFObs(2022-2023).svg)  
The correlation coefficient is 0.32.  
And the same graph with the tickets sold normalized by year:  
![Scatter plot comparing tickets sold domestically in 2022-2023 to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_Norm_vs_RFObs(2022-2023).svg)  
The correlation coefficient is 0.33.  

## Conclusions

From all-time data, we can't seem to predict the likelihood of cosplaying from a franchise from the tickets sold across all-time, whether we normalize or not. This is a bit of a surprise, as I expected the normalized data to have a noticeably stronger relationship due to the fact that it accounts for the effects of various phenomena such as Covid-19 and economic recessions on theater ticket sales.

Our ability to predict from last year's data isn't much better. The box office success of recent movie releases doesn't seem to have a strong relationship with instances of people cosplaying at the renaissance faire. Interestingly, whether or not there were movie releases does appear to have a much stronger relationship with the other factors considered, implying that recent exposure would be a better predictor for what people are likely to cosplay as at the Renaissance Faire

Ultimately, the ability to predict what people cosplay as is still limited by assumptions made when [choosing and collecting the data](#the-data) and in [limiting the dataset overall](#justification-behind-limiting-the-dataset-by-franchise). However, it appears we can at least tell that the choice to dress up from a certain franchise is not influenced much by box office success of the franchise, but that recent exposure might be a factor in the decision.
