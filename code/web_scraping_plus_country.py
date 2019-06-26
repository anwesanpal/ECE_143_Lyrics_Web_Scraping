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
		
# Getting rank, song, artist, nationality from Wiki - Hot 100 music from year 1959 - 2018

raw_html = simple_get('https://en.wikipedia.org/wiki/Billboard_Year-End') #base url
html = BeautifulSoup(raw_html, 'html.parser')

df = pd.DataFrame()
ind = -1  # from 1959
    
# get links for Hot 100 music, retrieve 'Title' and 'Artist(s)'
for link in html.find_all('a'):        
    if '/wiki/Billboard_Year-End_Hot_100_singles_of_' in str(link) and str(ind+1960) in str(link):
        ind += 1   
        sub_url = 'https://en.wikipedia.org' + str(link.get('href')) #sub url for each year
        sub_raw_html = simple_get(sub_url)
        sub_html = BeautifulSoup(sub_raw_html, 'html.parser')
        
        ranks = []
        artists = []
        nationality = []
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
                n = ''
                for i in range(len(items.contents)):
                    s = s + str(items.contents[i])
                if "</a>" in s:
                    # find the nationality of the artist
                    nation_url = 'https://en.wikipedia.org' + find_between(s,'href="','"')
                    nation_raw_html = simple_get(nation_url)
                    nation_html = BeautifulSoup(nation_raw_html, 'html.parser')
                    table = nation_html.find('table', attrs={'class':'infobox'})
                    if table:
                        if table.find_all('th',text='Origin'):
                            n = table.find_all('th',text='Origin')[0].next_sibling.text.split(',')[-1]
                        else:
                            table = table.find_all('th',text='Born')
                            if table:
                                n = table[0].next_sibling.text.split(',')[-1]
                    s = find_between(s, '>', '</a>')
                nationality.append(n)
                artists.append(s)
                if ind >= 23:
                    same_rank = 1
                else:
                    same_rank = 0
        # create a dataset for rank, song, artist
        df = df.append(pd.DataFrame({'rank': list(range(1,rank_ind+1)), 
                                     'song': songs, 
                                     'artist': artists, 
                                     'year':[ind+1959]*rank_ind,
                                     'nationality':nationality}))

        # output wiki dataset
        df.to_csv('TEAM_wiki1959-2018.csv',index=False)
