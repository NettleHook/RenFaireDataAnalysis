# Renaissance Faire Data Analysis Project

|Section|Subsections|
|---|---|
|[Quick Summary](#Quick-Summary)||
|[Goal](#Goal)||
|[The Data](#The-Data)|[Renaissance Faire Data](#Renaissance-Faire-Data), [Movie Data](#Movie-Data), [Ticket Data](#Ticket-Data)|
|[Analysis + Methods](#Analysis-+-Methods)|[Justification behind Limiting the Dataset by Franchise](#Justification-behind-Limiting-the-Dataset-by-Franchise), [Defining Popularity for Analysis](#Defining-Popularity-for-Analysis), [Reasons for Time-Based analysis](#Reasons-for-Time-Based-analysis), [General Analysis Approach](#General-Analysis-Approach)|
|[Results](#Results)||
|[Conclusions](#Conclusions)||

## Quick Summary
### Project 1:
#### Hypothesis: 
Popularity of a theater release, indicated as tickets sold, can be used to predict what people would cosplay as at the Renaissance Faire during a Superhero and Villains theme week.

#### Process: 
Focusing on specific Disney movies, DC, Marvel, Star Wars, Lord of the Rings movies, we collect all the domestic box office revenue and the release dates. We use the release dates to find the average ticket price per year. Next, we divide revenue by average ticket price to get tickets sold for that movie. We also get normalization data by dividing the tickets sold for the movie by the tickets sold that year. This is to account for any economic limitations. Both are then compared to the observations of cosplay counts in 2023.

#### Results:
![Scatter plot comparing tickets sold domestically to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_Norm_vs_RFObs.svg)  
The tickets sold were summed across franchises. The correlation coefficient between these is 0.32.  

![Scatter plot comparing tickets sold domestically, normalized by year, to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_vs_RFObs.svg)  
The normalization values were summed across franchises. The correlation coefficient between these is 0.62.  

### Project 2:
#### Hypothesis:
 We can predict from instances of a franchise and tickets sold in the year before the renaissance faire in question  what people would cosplay as at the Renaissance Faire during a Superhero and Villains theme week.

#### Process: This project is still underway

 
## Goal
&nbsp;&nbsp;The purpose of this analysis was to see if it might be possible to determine what people might cosplay at a Heroes and Villain themed week at my local Renaissance Faire.  
&nbsp;&nbsp;Since my friend and I have gotten full- time jobs, and after she's moved a bit further away, we've been trying to go to the Renaissance Faire every year. Our first trip together was in 2021, which also happened to coincide with their Heroes and Villain theme week. That year, the TV Show Loki had come out, and when we visited, I noticed that about half of all people who had dressed in theme were dressed as either Loki, or one of the multiverse variants introduced in that show.
&nbsp;&nbsp;This piqued my curiosity about whether it would be possible to predict what people would cosplay as based off of general popularity of franchises, but specifically recent releases prior to the Renaissance Faire. I didn't gather data that year, and in 2022 we didn't go during the Heroes and Villain theme week. We did return for that week in 2023, which is when the data I've used for this analysis is from.  
&nbsp;&nbsp;Ultimately, the questions we're hoping to answer are the following:
- Do movie releases in the year before this renaissance faire predict what costumes we see?
- Does the all-time popularity of these franchises predict what costumes we see?

## The Data
### Renaissance Faire Data
&nbsp;&nbsp;The Renaissance Faire data was gathered from a list of observations I made when I visited during 2023. There are some limitations with the accuracy of this data, which are as follows:
- My priority in visiting the Renaissance Faire was to have fun, rather than to observe total instances of costumes, so it's very likely I missed some cosplayers
- As a continuation of the previous point, I am of legal age and fond of cider, so I was tipsy for a not insignificant portion of the faire, which would have further inhibited my ability to notice cosplayers
- I am limited to only observing what I was able to recognize. There were some costumes that looked like they could be a specific character to me, but I wouldn't know who they were, so they weren't noted.

&nbsp;&nbsp;After the observations were gathered, I built a list from them, and used a switch statement to add various facts I thought may be useful to this analysis project and possible to some future projects. The final columns in the pandas dataframe were:
|Column Name| Description|
|---|---|
|Character| The name of the character|
|Media Source| The franchise from which the character came|
|Gender| Observed gender of the character|
|Year| For all this data, it's just 2023. I hoped in the future if I visit during this week, I might add more observations|


&nbsp;&nbsp;The script to form the csv from the observations is file `RenFaireSuperheroes.py`, which creates the csv `RenFaireObservations.csv`
&nbsp;&nbsp;The Observation data contains more data than what was ultimately used. I decided to only examine movie theater data, to ensure the scope of the project wouldn't be too big, and because expanding to video games, TV shows, and streaming would make it much harder to find a common metric to use as the definition of popularity.
&nbsp;&nbsp;The franchises I observed were Star Wars, Disney (Robin Hood, Shrek, Hercules), Marvel, DC, My Hero Academia, Legend of Zelda, Genshin Impact, Lord of the Rings, Princess Bride
&nbsp;&nbsp;Due to the decision to focus on movie series, this list was reduced to Star Wars, Disney (Robin Hood, Shrek, Hercules), Marvel, DC, and Lord of the Rings (LOTR), for the purposes of the final data analysis. More details on this decision can be found [here](#Justification-behind-Limiting-the-Dataset-by-Franchise)


### Movie Data
&nbsp;&nbsp;For the next dataset, I searched for all the movies within a franchise, and copied their information into a csv. The exception to this was Disney movies, as including all of their movies would obscure all the other data, due to the sheer amount of them. For Disney movies, I only included those we observed people dressing as characters from -  Robin Hood, Hercules, and the Shrek series. Of course, this means introducing another dataset later, when I'm checking the preceding year's theatrical releases.
&nbsp;&nbsp;The data focuses on domestic releases in order to get as close to local data as is feasible. I also only noted data for the initial release, in the cases where movies were re- run a few years later. This seemed to be the easiest way to measure the success of a movie without accounting for any re- releases that may be done.
Failings of this approach include the inability to account for cult classics, doesn't account for the effects re- watchability has on popularity, and that movies people really liked are more likely to be rewatched many years after the fact.
&nbsp;&nbsp;Here is the column data for the `movies.csv` file, which contains the data gathered:
|Column Name| Description|
|---|---|
|name| title of the movie|
|release_date| Date of initial release. Due to lack of information, this isn't always the domestic release date|
| opening_box_office | opening weekend box office revenue. This information isn't necessarily domestic|
| domestic_box_office | box office revenue the film made during its initial run in theaters, domestically|
|franchise| the franchise it belongs too from the list: DC, Disney, Marvel, LOTR, Star Wars|

&nbsp;&nbsp;Data Source:https://www.boxofficemojo.com/


### Ticket Data
&nbsp;&nbsp;Because I chose to use tickets sold as the metric for popularity[insert link to justification], I also needed a dataset with ticket prices to help calculate the tickets sold per movie.
&nbsp;&nbsp;The dataset has the following columns;
|Column Name| Description|
|---|---|
|Year| year|
|Tickets Sold| total tickets sold that year|
|Total Box Office| Box Office revenue for that year|
|Total Inflation Adjusted Box Office| Box office revenue for the year, adjusted for inflation|
|Avg. Ticket Price| Average price of tickets that year, not accounted for inflation|

Our first dataset only had information as early as 1995, but we needed information as early as 1970.
&nbsp;&nbsp;All data reflects domestic box office numbers.
&nbsp;&nbsp;Data Sources:
- https://www.the- numbers.com/market/ (yielded the 1995- 2023 information)
- https://finance.yahoo.com/news/cost- movie- ticket- were- born- 155153039.html (yielded the - 1994 average ticket prices)
- https://www.boxofficemojo.com/year/?ref_=bo_nb_hm_secondarytab (1977- - 1994 Total Box Office revenue)
- To fill in the blanks, I was able to calculate total tickets sold that year by dividing total box office revenue by average ticket price.


## Analysis + Methods
### Justification behind Limiting the Dataset by Franchise
&nbsp;&nbsp;While at the Renaissance Faire, I noticed characters from movies, comics, video games, and TV Shows, I ultimately decided to only focus on movies released in theater. The primary reason for this was the availability of box office data and theater ticket pricing was far easier to find than data from streaming platforms such as Netflix and Disney+. It was also harder to find any download data about video games. The other main reason to focus only on box office data would be avoiding the difficulty introduced when quantifying popularity in a way that is comparable between different types of media.
&nbsp;&nbsp;If I wanted to compare video game download instances (assuming I could find it) to times a movie was seen in theaters, these wouldn't necessarily be comparable. Video Games are more expensive that theater tickets in many cases, and in some cases video games can be installed in multiple places at no additional cost. How would we compare these two metrics, and how would we relate these to popularity?
&nbsp;&nbsp;Furthermore, because of the way I am measuring popularity, it's not effective for works that aren't serialized. As a result, Princess Bride unfortunately had to be dropped from consideration.
To conclude, in order to  keep the scope of my project manageable, make sure my datasets were easier to find, and to ensure I could establish only one metric of 'popularity', I chose to focus my analysis on box office data for semi- serialized movies.


### Defining Popularity for Analysis
&nbsp;&nbsp;As we are using 'popularity' to see if we can predict cosplays at Heroes and Villains Week at my local Renaissance Faire, I needed to begin by defining what the popularity metric would be in this case. Ultimately, I decided tickets sold normalized per year would be the metric I used.
&nbsp;&nbsp;Reasons for this:
- In the context of initial theatrical release, box office revenue or tickets sold would be the best metrics of how well the movie performed among people
- Using tickets sold means I don't have to account too much for how inflation affected prices.
- Due to the effect of covid and post- covid on theater attendance, I wanted to use the normalized values, as that would more accurately demonstrate the movies relative success, and remove any penalty movies released in this theater would have in comparison to movies released pre- covid.


### Reasons for Time-Based analysis
There are two questions, split on the time axes. In one question, I hoped to determine if releases in the past year would predict cosplays seen. My idea behind this is that having recent exposure to an instance of a franchise will place both the notion of that franchise and the memory of loving previous iterations in your mind enough that when it comes time to planning your costume for the Renaissance Faire, you might decide to use that as inspiration.
To clarify, I mean that if Disney produced a new movie this year that you see, you might remember “Oh, I really loved Shrek!” and a few months down the line, when it comes time for you to start planning your costume, you'll remember thinking about Shrek, and might consider that as the inspiration for the costume.
As anecdotal evidence of this, I did watch Blue Beetle when it came out in the summer of 2023, and it did make me think about possibly doing a Batgirl- inspired Renaissance Faire costume. Ultimately, the decision not to was only due to an external influence (previous commitment to be a pirate with my friend), so I felt that there was sufficient evidence that nostalgia can fuel cosplay choices.
&nbsp;&nbsp;Of course, the nostalgia being fuel for the inspiration is dependent on you actually liking the franchise in the first place, which is why I think it's still important to examine all- time popularity of a franchise as a potential measure of the likelihood of people cosplaying from that franchise.
&nbsp;&nbsp;These are the justifications behind examining both all- time data, and the data from within the past year.


### General Analysis Approach
&nbsp;&nbsp;We begin by importing the movies data set from the `movies.csv` file, and the tickets dataset from the `tickets_1.csv` file. The data in these two is explained in section the [Movie Data](#Movie-Data) and [Ticket Data](#Ticket-Data) sections.
&nbsp;&nbsp;Next, we do a bit of dtype formatting. I need to get the year from the `release_date` column of the movies dataset, because I intend to merge these two datasets later
&nbsp;&nbsp;My code includes the `franchise` counts, because I wanted to see the general entry breakdown before we began.
&nbsp;&nbsp;Now, we merge the two datasets on the `Year` column, and we need to get the tickets sold per movie by dividing `Avg. Ticket Price` by `domestic_all`. This creates the column `Tickets Sold by Movie_domestic` Next, we create a new column, called `normal_tics_Opening`, with the normalized data, by dividing the tickets sold per movie by `Tickets Sold`. As a reminder, we want to compare using the normalized data to diminish any penalties caused by covid and post- covid (lack of) theater attendance.
&nbsp;&nbsp;The next step is to import the observation data from `RenFaireObservations.csv`. I've already explained in [this section](#Justification-behind-Limiting-the-Dataset-by-Franchise) why I'm limiting the data to just DC, Disney, LOTR, Marvel, and Star Wars franchises. The next step is to filter the dataset imported from the file to reflect this.


Now that the datasets are ready, I can start doing the comparisons to see if the normalized ticket sales reflect cosplays seen at the Renaissance Faire.


## Results
&nbsp;&nbsp;I made bar graphs of the general data distributions, so we could examine visually if they seem to compare.
![Bar graph indicating tickets sold across franchises](/Supporting%20Files/graphs/Tickets_Sold_Bar.svg)  
![Bar graph indicating tickets sold across franchises, with tickets sold normalized by year](/Supporting%20Files/graphs/Tickets_Sold_Bar_Normal.svg)  
![Bar graph showing cosplay observations by franchise](/Supporting%20Files/graphs/Ren_Faire_Observations_Bar.svg)  

&nbsp;&nbsp;We can already see that these don't seem to match up, though interestingly Tickets Sold matches better than Tickets Sold Normalized to the Character Observations bar graph.

&nbsp;&nbsp;That being said, this is just an initial look at the tickets sold data and how it compares to our observations at the 2023 faire. We still have to see how data from the year before appears compared to the observations.

&nbsp;&nbsp;Additionally, we can better see if there's any relationship between these values using scatterplots.
Here are the scatterplots comparing 'all-time' tickets sold to Ren Faire observations:

![Scatter plot comparing tickets sold domestically to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_Norm_vs_RFObs.svg)  

The tickets sold were summed across franchises. The correlation coefficient between these is 0.32.  
And the same graph, where the tickets sold have been normalized based off all tickets sold that year:   
![Scatter plot comparing tickets sold domestically, normalized by year, to cosplay observations at the renaissance faire](/Supporting%20Files/graphs/Tickets_Sold_vs_RFObs.svg)  
The normalization values were summed across franchises. The correlation coefficient between these is 0.62.  

## Conclusions
&nbsp;&nbsp;From all-time data, we can't seem to predict the likelihood of cosplaying from a franchise from the tickets sold as a sum across all-time. We do have a better chance of guessing if we normalize ticket sales by year before summing. This isn't totally a surprise, due to the effects of various phenomena such as Covid and economic recessions on theater ticket sales. Normalizing the tickets sold by year gives us a better idea of how popular that movie was in comparison to the others released the same year, which is what I originally intended to represent with the ticket sales at domestic theaters.

&nbsp;&nbsp;Ultimately, the ability to predict what people cosplay as is still limited by assumptions made when [choosing and collecting the data](#The-Data) and in [limiting the dataset overall](#Justification-behind-Limiting-the-Dataset-by-Franchise)


