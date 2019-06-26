'''
This file cleans up the genre data. It classifies the 489 detected genres into the 17 existing genre categories.
'''

import pandas as pd

# concatenate the different csv files for the years into one big file

file = 'wiki_with_genres_newest/wiki1959_with_genre.csv'
df = pd.read_csv(file, encoding='latin-1')
years = list(range(1960,2019))
for year in years:
    file = 'wiki_with_genres_newest/wiki{}_with_genre.csv'.format(year)
    df_temp = pd.read_csv(file, encoding='latin-1')
    df = df.append(df_temp, ignore_index=True)
df.to_csv('wiki1959-2018_with_genre_v2.csv',index=False)    

# read this new file

file = 'wiki1959-2018_with_genre_v2.csv'
df = pd.read_csv(file, encoding='latin-1')

def splitDataFrameList(df,target_column,separator):
    ''' df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(target_column, str)
    assert isinstance(separator, str)

    row_accumulator = []

    def splitListToRows(row, separator):
        split_row = row[target_column].split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)

    df.apply(splitListToRows, axis=1, args = (separator, ))
    new_df = pd.DataFrame(row_accumulator)
    return new_df

new_df = splitDataFrameList(df,'genres',',')

old_list = new_df['genres'].tolist()
new_list = []

# remove all the punctuations and blank spaces

for ele in old_list:
    new_ele = ele.strip()
    new_list.append(new_ele)

new_df['genres'] = new_list

# Enlist the 17 different main genres, and their sub-genres

A_capella = ['A_cappella']

Afro = ['Afrobeat']

Avant_garde = ['Experimental_music']

Blues = ['Acoustic_blues','Blues','Blues_music','Blues_rock','Country_blues',
        'Delta_blues','Electric_blues','Gospel','Gospel_music','Soul_Blues',
        'Soul_blues','Talking_blues']

Caribbean = ['Calypso_Music','Calypso_music','Dancehall_music','Merengue_music',
            'Reggae','Reggae-pop','Reggae_Pop','Reggae_fusion','Reggae_rock',
            'Reggaeton','Ska','Ska_punk','Soca_music']

Children_music = ['"Children\'s_music"']

Comedy = ['Comedy_music','Comedy_rock','Comedy_song','Novelty','Novelty_music',
         'Novelty_song']

Country = ['Americana_(music)','Americana_music','Big_Band','Big_band',
          'Bluegrass_music','Bro-country','Christian_music','Country',
          'Country_crossover','Country_music','Country_rap','Countrypolitan',
          'Lubbock_sound','Minneapolis_sound','Nashville_sound','Parody_music',
          'Tex-Mex_music','Traditional_country','Truck-driving_country']

Easy_Listening = ['Easy-Listening','Easy_Listening','Easy_listening',
                 'Middle_of_the_road_(music)','New-age_music']

Electronic = ['2-step_garage','Acoustic_music','Alternative_dance','Bass_music',
             'Bassline','Bhangra_(music)','Bounce_music','Breakbeat',
             'Bubblegum_dance','Chill-out_music','Club_music','Crunk&B','Dance-punk',
             'Dance_music','Dancehall','Deep_house','Disco','Disco-dance',
             'Disco_music','Downtempo','Dream_trance','Dub_music','Dubstep',
             'EDM','Electro-house','Electro_(music)','Electro_funk',
             'Electro_house','Electro_music','Electronic_dance_music',
             'Electronic_music','Electronica','Electronicore','Euro_disco',
             'Eurodance','Eurodisco','Folktronica','Funktronica','Future_bass',
             'Future_garage','Happy_hardcore','Hardcore_(electronic_dance_music_genre)',
             'Hi-NRG','Hip_house','House','House_music','Indietronica','Industrial_music',
             'Italo_disco','Kwaito','Miami_bass','Minimal_music','Moombahton',
             'Nu-disco','Piano_music','Post-disco','Progressive_electronic_dance_music',
             'Synth-funk','Tech_house','Techno','Trance_Music','Trance_music',
             'Tropical_house','Tropical_music','UK_garage']

Folk = ['American_folk_music','British_Invasion','Celtic_music','Christmas_song',
       'Classical_music','Contemporary_Christian','Contemporary_Christian_Music',
       'Contemporary_Christian_music','Contemporary_folk_music','Country_folk',
       'Folk','Folk_music','Indie_folk','Progressive_folk','Progressive_house',
       'Protest_song','Psychedelic_folk','Psychedelic_music',
       'Urban_adult_contemporary','Urban_contemporary','Urban_contemporary_gospel']

Hip_hop = ['Acoustic_hip_hop','Alternative_hip-hop','Alternative_hip_hop',
          'Canadian_hip_hop','Chopped_and_screwed','Christian_hip_hop','Comedy_hip_hop',
          'Conscious_hip_hop','Crunk','Crunkcore','East_Coast_hip_hop',
          'East_coast_hip_hop','Electro-hop','Electro_hop_music','Electrohop',
          'G-Funk','G-funk','Golden_age_hip_hop','Hardcore_hip_hop','Hip hop',
          'Hip-Hop','Hip-Hop_Singles_and_Tracks','Hip-Hop_music','Hip-hop',
          'Hip-hop_music','Hip_Hop','Hip_Hop_music','Hip_hop','Hip_hop_music',
          'Hip_hop_soul','Hipster_hop','Horrorcore','Hyphy','Instrumental','Instrumental_music',
          'Jersey_Shore_sound','Midwest_hip_hop','New_jack_swing',
          'Old-school_hip_hop','Old_school_hip_hop','Snap_music','Southern_hip_hop',
          'Trap_(music_genre)','Trap_music','Trip_hop','Underground_hip_hop',
          'West_Coast_Hip_Hop','West_Coast_hip_hop','West_coast_hip_hop']

Jazz = ['Acid_jazz','Bossa_nova','Dixieland_jazz','Folk_jazz','Jazz','Jazz-funk',
       'Jazz-rock','Jazz_Fusion','Jazz_fusion','Jazz_music','Jazz_rap','Jazz_rock',
       'Orchestral','Ragtime','Smooth_Jazz','Smooth_jazz','Soul_jazz','Swing_music',
       'Vocal_jazz','West_Coast_jazz']

Latin = ['Bachata_(music)','Bolero','Cumbia','Flamenco','Latin_hip_hop',
        'Latin_jazz','Latin_music_(genre)','Latin_pop','Latin_rap','Latin_rock',
        'Latin_soul','Mambo_(music)','Power_ballad','Salsa_music','Sentimental_ballad',
        'Tango_music','Tejano_music']

Pop = ['Adult_Contemporary','Adult_album_alternative','Adult_contemporary',
      'Adult_contemporary_music','Alternative_pop','Art_pop','Ballad','Baroque_pop',
      'Bitpop','Brill_Building_(genre)','Britpop','Bubblegum_pop','California_Sound',
       'Chamber_pop','Chanson','Classical_crossover','Cloud_rap','Country_Pop',
      'Country_pop','Crossover_music','Dance-pop','Dance_pop','Dirty_Rap',
      'Dirty_pop','Dirty_rap','Dream_pop','Electropop','Europop','Exotica',
      'Experimental_pop','Film_score','Folk_pop','Freestyle_rap','Funk_rap',
      'Gangsta_Rap','Gangsta_rap','Girl_Group','Girl_group','Gulf_and_western_(music_genre)',
      'Hip_pop','Indie_pop','Italo_house','J-pop','Jangle_pop','Jive_(dance)',
      'K-pop','Kay?kyoku','Mafioso_rap','Mashup_(music)','Midwest_rap','Minstrel_show',
      'Modern_adult_contemporary','Motown','Musical_theatre','New_Wave_Music',
      'New_wave','New_wave_music','Orchestral_pop','Pop','Pop-Rock','Pop-rap',
      'Pop-rock','Pop-soul','Pop_(music)','Pop_Music','Pop_Rap','Pop_Rock',
      'Pop_music','Pop_punk','Pop_rap','Pop_rock','Pop_rock_music','Pop_soul',
      'Pop_standard','Popular_music','Popular_song','Post-punk','Post-punk_revival',
      'Power_pop','Progressive_pop','Proto-prog','Proto-punk','Protopunk',
      'Psychedelic_Pop','Psychedelic_pop','Quiet_Storm','Quiet_storm','Rap',
      'Rap_metal','Rap_music','Rapcore','Show_tunes','Sophisti-pop',
      'Spoken_word','Sunshine_Pop','Sunshine_pop','Swamp_pop','Synthpop',
      'Teen_pop','Teen_tragedy_song','Teenage_tragedy_song','Theme_music',
      'Traditional_pop','Traditional_pop_music','Vocal_music','Vocal_pop']

R_and_B = ['Alternative_R&B','Balkan_music','Blue-eyed_soul','Blue_eyed_soul',
          'Boogie_(genre)','British_rhythm_and_blues','British_soul','Chicago_soul',
          'Contemporary_R&B','Country_soul','Doo-Wop','Doo-wop','Doo_wop',
          'Electro-R&B','Freestyle_music','Funk','Funk_music','Go-go','Memphis_soul',
          'Neo_soul','New_Orleans_rhythm_and_blues','Northern_soul','PBR&B',
          'Philadelphia_Soul','Philadelphia_soul','Philly_Soul','Philly_soul',
          'Psychedelic_soul','R&B','R&B_music','R&b','Rhythm_&_Blues',
          'Rhythm_&_blues','Rhythm_and_Blues','Rhythm_and_blues','Slow_jam',
          'Smooth_soul','Soul','Soul_(music)','Soul_Music','Soul_music','Southern_soul'
          ]

Rock = ["Rock'n'roll","Rock_'n'_Roll","Rock_'n'_roll",' Rock','Acid_rock',
        'Acoustic_rock','Alternative_metal','Alternative_rap','Alternative_rock',
       'Arena_rock','Art_rock','Beat_music','Boogie_rock','British_rock_and_roll',
       'Car_song','Cello_rock','Celtic_rock','Chicano_rock','Christian_Rock',
       'Christian_rock','Classic_rock','College_rock','Country_Rock','Country_rock',
       'Crossover_thrash','Dance-rock','Dance_rock','Disco-rock','Electronic_rock',
       'Emo','Experimental_rock','Folk_rock','Funk_metal','Funk_rock','Garage_rock',
       'Glam_Metal','Glam_metal','Glam_punk','Glam_rock','Gothic_metal','Grunge',
       'Hard_Rock','Hard_rock','Hardcore_punk','Heartland_rock','Heavy_metal_music',
       'Horror_punk','Hot_rod_rock','Indie_rock','Industrial_rock','Instrumental_rock',
       'Merseybeat','Metalcore','Modern_rock','Neo-psychedelia','Neue_Deutsche_Welle',
       'Noise_rock','Nu_metal','Piano_rock','Post-Britpop','Post-grunge','Post-hardcore',
       'Post_grunge','Power_metal','Progressive_rock','Proto-metal',
       'Psychedelic_rock','Pub_rock_(United_Kingdom)','Punk_Rock','Punk_rock',
       'Raga_rock','Rap_rock','Rock and roll','Rock n Roll','Rock','Rock_&_Roll',
       'Rock_&_roll','Rock_(music)','Rock_Music','Rock_and_Roll','Rock_and_roll',
       'Rock_ballad','Rock_en_Español','Rock_en_español','Rock_music','Rock_n_Roll',
       'Rock_n_roll','Rock_opera','Rockabilly','Rocksteady','Roots_rock','Soft Rock',
       'Soft_Rock','Soft_rock','Southern_Rock','Southern_rock','Space_rock',
       'Speed_metal','Surf_music','Surf_rock','Swamp_rock','Symphonic_music',
       'Symphonic_rock','Synthrock','World_music','Worldbeat']

newer_list = []
for element in new_list:
    if(element in str(A_capella) and element is not '-'):
        newer_list.append('A_capella')
    elif(element in str(Afro) and element is not '-'):
        newer_list.append('Afro')
    elif(element in str(Avant_garde) and element is not '-'):
        newer_list.append('Avant_garde')
    elif(element in str(Blues) and element is not '-'):
        newer_list.append('Blues')
    elif(element in str(Caribbean) and element is not '-'):
        newer_list.append('Caribbean')
    elif(element in str(Children_music) and element is not '-'):
        newer_list.append('Children_music')
    elif(element in str(Comedy) and element is not '-'):
        newer_list.append('Comedy')
    elif(element in str(Country) and element is not '-'):
        newer_list.append('Country')
    elif(element in str(Easy_Listening) and element is not '-'):
        newer_list.append('Easy_Listening')
    elif(element in str(Electronic) and element is not '-'):
        newer_list.append('Electronic')
    elif(element in str(Folk) and element is not '-'):
        newer_list.append('Folk')
    elif(element in str(Hip_hop) and element is not '-'):
        newer_list.append('Hip_hop')
    elif(element in str(Jazz) and element is not '-'):
        newer_list.append('Jazz')
    elif(element in str(Latin) and element is not '-'):
        newer_list.append('Latin')
    elif(element in str(Pop) and element is not '-'):
        newer_list.append('Pop')
    elif(element in str(R_and_B)) and element is not '-':
        newer_list.append('Rhythm_and_Blues')
    elif(element in str(Rock) and element is not '-'):
        newer_list.append('Rock')
    else:
        newer_list.append('-')
    
assert len(new_list) == len(newer_list)

new_df['genres_cleaned'] = newer_list

# regroup the different genres into the same list for each song (reverse of what splitDataFrameList did)

newer_df = new_df.groupby(['year','rank','artist','song'])['genres_cleaned'].apply(', '.join).reset_index()
genres_cleaned = newer_df['genres_cleaned'].tolist()

# remove all '[]'

genres_cleaned_single = []
for genre in genres_cleaned:
    if(genre == '-'):
        genres_cleaned_single.append('-')
        continue
    genres_cleaned_single.append(str(list(set(genre.split(', ')))).strip('[]'))

# create final .csv file listing the cleaned up genres

file = 'wiki1959-2018_with_genre_v2.csv'
newest_df = pd.read_csv(file, encoding='latin-1')
newest_df['genres_cleaned'] = genres_cleaned_single

newest_df.to_csv('TEAM_wiki1959-2018_with_genres_cleaned.csv',index=False)
