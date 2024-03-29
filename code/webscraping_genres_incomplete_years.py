'''
This is the code to extract the unclean genres of the Billboard songs from the DBPedia resources. This file deals with songs 
for the years which do not have links for all the 100 songs
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib, json 

def find_between(s, first, last):
    '''
    Find a specific string/pattern between to expressions
    '''
    try:
        start = s.index( first ) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

skipped_years = [1965,1967,1971,1972,1988,1990,1994,1996,1999,2002,2003,2014,2016]
years = [2016]

# We need to loop through each year individually as we don't know apriori which songs might not have links

for year in years:

#  read song names from file

    file = 'wiki1959-2018.csv'

# acquire links for the individual songs

    df = pd.read_csv(file, encoding='latin-1')
    all_songs = list(df.song)
    wiki_url = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{}'.format(year)
    page = requests.get(wiki_url).text
    html = BeautifulSoup(page,'html.parser')
    table = html.find('table', 'wikitable')
    links = table.findAll('a',href=True)
    links_content = {}
    count=0
    count2=0
    skipped_list2 = []
    all_genres = []
    songs_genr = {}
    skipped_list = []

# loop through the links and extract genre data from dbpedia. If genre is not present, or link is not readable, add '-' to the song

    for link in links:
        song_name = find_between(str(link), '>', '</a>')
        if(song_name in all_songs[100*(year-1959):100*(year-1959+1)]):
            song_url = str(link['href']).split('/')[-1]
            song_url = urllib.parse.unquote(song_url)
            if('#' in str(song_url)):
                skipped_list2.append(song_url)
                all_genres.append('-')
                continue
            try:
                with urllib.request.urlopen("http://dbpedia.org/data/{}.json".format(song_url)) as url:
                    data = json.loads(url.read().decode())
            except (UnicodeEncodeError, urllib.error.HTTPError):
                skipped_list2.append(song_url)
                all_genres.append('-')
                continue

            dict_1 = data.get("http://dbpedia.org/resource/{}".format(song_url))
            if(dict_1 is None):
                skipped_list2.append(song_url)
                all_genres.append('-')
                continue
            dict_2 = dict_1.get("http://dbpedia.org/ontology/genre")
            if(dict_2 is None):
                dict_2 = dict_1.get("http://dbpedia.org/property/genre")
            if(dict_2 is None):
                skipped_list2.append(song_url)
                all_genres.append('-')
                continue
            genres = []
            for dicts in dict_2:
                genres.append(dicts.get('value').split('/')[-1])
            if(song_name in list(songs_genr.keys())):
                songs_genr[song_name].append(genres)
            else:
                songs_genr[song_name]=genres
            all_genres.append(str(genres).strip('[]'))
            count+=1

# save dictionary with song names as keys and genres as values

    final_dict = {}
    for name in all_songs[100*(year-1959):100*(year-1959+1)]:
        if(name in list(songs_genr.keys())):
            print(len(songs_genr.get(name)))
            final_dict[name] = songs_genr.get(name)
        else:
            final_dict[name] = '-'
    print(len(final_dict))
    assert len(final_dict) == 100

# add uncleaned genres to the existing .csv file

file2 = 'nation_cleaned.csv'
df2 = pd.read_csv(file2, encoding='latin-1')
df3 = df2.iloc[100*(year-1959):100*(year-1959+1)]
df3['genres'] = all_genres
df3.to_csv('wiki_with_genres_newest/wiki{}_with_genre.csv'.format(year),index=False)
