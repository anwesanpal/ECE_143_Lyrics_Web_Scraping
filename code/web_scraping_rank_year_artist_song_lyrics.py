from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import re

import csv
import os

# making web requests
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    assert isinstance(url,string)
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
    
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# [function] find a specific string/pattern between to expressions

def find_between(s, first, last):
    """
    Find a specific string/pattern between to expressions
    """
    assert isinstance(s,string)
    assert isinstance(first,string)
    assert isinstance(last,string)
    try:
        start = s.index( first ) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

def find_between_r(s, first, last):
    """
    Find a specific string/pattern between to expressions
    """
    assert isinstance(s,string)
    assert isinstance(first,string)
    assert isinstance(last,string)
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ''
		
# Part 1: getting rank, song, artist from Wiki - Hot 100 music from year 1959 - 2018

raw_html = simple_get('https://en.wikipedia.org/wiki/Billboard_Year-End') #base url
html = BeautifulSoup(raw_html, 'html.parser')

df = pd.DataFrame()
ind = -1
    
# get links for Hot 100 music, retrieve 'Title' and 'Artist(s)'
for link in html.find_all('a'):
    if '/wiki/Billboard_Year-End_Hot_100_singles_of_' in str(link):
        ind += 1   
        sub_url = 'https://en.wikipedia.org' + str(link.get('href')) #sub url for each year
        sub_raw_html = simple_get(sub_url)
        sub_html = BeautifulSoup(sub_raw_html, 'html.parser')
        
        ranks = []
        artists = []
        songs = []
        index = 0
        if ind >= 23:
            same_rank = 1
        else:
            same_rank = 0
        
        rank_ind = 0
        
        for items in sub_html.find('table', attrs={'class':'wikitable sortable'}).find_all('td'):
            same_rank += 1 # deal with the instance with multiple artists
            if same_rank == 2:
                rank_ind += 1
                s = ''
                for i in range(len(items.contents)):
                    s = s + str(items.contents[i])
                if '</a>' in s:
                    s = find_between(s, '>', '</a>')
                songs.append(s)
            elif same_rank == 3:
                s = ''
                for i in range(len(items.contents)):
                    s = s + str(items.contents[i])
                if "</a>" in s:
                    s = find_between(s, '>', '</a>')
                artists.append(s)
                if ind >= 23:
                    same_rank = 1
                else:
                    same_rank = 0
        # create a dataset for rank, song, artist
        df = df.append(pd.DataFrame({'rank': list(range(1,rank_ind+1)), 
                                     'song': songs, 
                                     'artist': artists, 
                                     'year':[ind+1959]*rank_ind}))

# output wiki dataset
df.to_csv('wiki1959-2018.csv',index=False)

# Part 2: Get lyrics from https://genius.com

# print current directory
print('Path at terminal when executing this file')
print(os.getcwd() + "\n")

# read in csv file, store the original dataset as wiki_dat
wiki_dat = pd.read_csv('wiki1959-2018.csv', encoding='ISO-8859-1')
wiki_dat.head()
df = wiki_dat

# create row index
df['obsnum'] = df.index + 1

# create url by concatenating song name and artist name
df['url'] = df.apply(lambda row: ('https://genius.com/'+removeSpecial(row.artist+' '+row.song)+'-lyrics').replace(' ','-').lower(), axis=1)

df.sample(20)

start = 0
end = 6001

for i in range(start,end):
    lyrics_url=df.at[i,'url']
    try: 
        lyrics_raw_html = simple_get(lyrics_url)
        lyrics_html = BeautifulSoup(lyrics_raw_html,'html.parser')
        df.at[i,'lyrics'] = str(lyrics_html.find('div', attrs={'class':'lyrics'}).text) # only pull down text between nodes

    except:
        df.at[i,'lyrics'] = 'url not retrieved'
        pass

df.to_csv('lyrics_final.csv',index=False) #634/6000=10.6%

tm_dat = pd.read_csv('data/lyrics_final.csv', encoding='ISO-8859-1')
df = tm_dat

df['lyrics'] = df['lyrics'].apply(lambda x: re.sub('Hook|Verse 1|Intro|Chorus', '', x).replace('[]',''))
