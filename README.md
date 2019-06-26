# ECE-143-Lyrics-Web-Scraping

This repository contains the code and the results for the project titled "Lyrics Web Scraping and Text Mining Analysis". It was completed by Group-2 for the course ECE 143, Winter 2019. 

## Codes

### Data Collection
- Song rank, year, artist and lyrics - [This](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/web_scraping_rank_year_artist_song_lyrics.py) file contains the code to gather the data regarding the song name, the rank it obtained in the billboard charts, the respective year, and finally the name of the artist. All these information were gather using Wikipedia Billboard Year End [list](https://en.wikipedia.org/wiki/Billboard_Year-End). Lyrics of these songs were extracted from [genius](https://genius.com).
- Nationality - [This](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/web_scraping_plus_country.py) file contains the code for gathering data about the nationality of the artists for each of the songs. This was gathered from the Wikipedia pages for the artists.
- Genre - The genre data was collected for the songs in two parts. Firstly, we consider the years which have links for all the 100 songs in the list. This is done in the [first](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/webscraping_genres_complete_years.py) file. Secondly, the years which do not fall into this category need to be dealt with individually since we do not know which song might be absent. This is done in the [second](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/webscraping_genres_incomplete_years.py) file. 

### Data Cleaning
Data cleaning is very important for perfoming text mining analysis. This is specially true for the attributes of nationality, genres, and lyrics. 
- Nationality - The data cleaning for nationalities involved classifying more than 128 areas into 37 different nationalities. This was done by grouping labels of different areas(stats, cities, etc) in the same country into a uniform label of nationality. This part is shown in [this](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/TextMining.ipynb) file.
- Genres - The data cleaning for genres involved classifying the 489 different genres as obtained from the data collection process into the 17 different existing main genres. This was done by grouping differently labelled genres under the umbrella of some main genres. This part is shown in [this](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/datacleaning_genres.py) file. 
- Lyrics - The data cleaning for lyrics involved filtering out 'url not retrieved' and removing stop words, punctuations and unwanted words. We retrieved 5367 out of 6000 lyrics from [genius](https://genius.com). This part is shown in [this](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/TextMining.ipynb) file.

## Text-Mining
We performed 3 types of text-mining analysis. The first is [N-gram](https://en.wikipedia.org/wiki/N-gram) where we show the results for unigram, bigram and trigram. The second is the [Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) where the songs are studied in terms of their positive/negative sentiment scores. The third analysis is using [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf), where we try to find out the most common words which could be found for the three most popular genres - hiphop, electronic, and pop. All the analysis and their visualizations can be found in this [file](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/code/TextMining.ipynb). 
## Result 

### Data
The [data](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/tree/master/data) folder contains our results in .csv files. all information are represented as pandas dataframes, and stored in 5 different parts - [only song details](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/TEAM_wiki1959-2018.csv), [song details + lyrics](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/lyrics_final.csv), [song details + nationality cleaned](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/TEAM_wiki1959-2018_with_nationality_cleaned.csv), [song details + nationality cleaned + genres cleaned](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/TEAM_wiki1959-2018_with_genres_cleaned.csv) and [all information](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/All_20190224.csv). In addition, [positive words](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/positive-words.txt) and [negative words](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/blob/master/data/negative-words.txt) were found online and used for sentiment analysis. 

### Plots
All the plots for our codes can be found in the [plots](https://github.com/hzy0211/ECE-143-Lyrics-Web-Scraping/tree/master/plots) folder. Each plot is named and titled to show what they represent.

## Contribution

- Proposal - Equal Contribution
- Song name, artist, rank, year and lyrics collection - Zhaoyuan He
- Nationality Collection + Cleaning - Yihua Yang and Qinyan Li
- Genre Collection + Cleaning - Anwesan Pal
- Text Mining - Equal Contribution
- Presentation - Equal Contribution
