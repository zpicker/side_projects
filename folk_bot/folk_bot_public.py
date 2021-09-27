"""
markov chain music creator by Zac Picker
"""

import markovify as mfy
import random
import tweepy
import matplotlib.pyplot as plt
import numpy as np
import os

#uses 'ajj.txt' and 'tmg.txt' to generate song structure. 
#they're just plain text files that go chords-lyrics-chords-lyrics etc
#contain all the lyrics for the folk bands 'the mountain goats' and 'AJJ', all lyrics and chords are theirs.
#feel free to copy any of your favorite songs from your favorite chord website etc


#%% twitter shit:
"""
again, twitter api stuff goes here
"""
#try: #to test if its connecting to twitter
#    api.verify_credentials()
#    print("Authentication OK")
#except:
#    print("Error during authentication")
#api.update_status("I wish that I was a big ball of meat") #test status update
    
#%%song generation stuff

#band choosing below
artist = 2
#1=ajj
#2=tmg
#3=all
if artist == 1:
    file = 'ajj.txt' #put music in this text file. first line chords, second line lyrics, etc.
    bandname = 'AJJ'
elif artist == 2:
    file = 'tmg.txt'
    bandname = 'The Mountain Goats'
elif artist == 3:
    filenames = ['ajj.txt', 'tmg.txt']
    bandname = 'folk artists'
    with open('mergedfile.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
#song setup here                    
songlength = random.randint(7,14) #number of lines
titlecharacterlength = random.randint(15,45)
statesize=random.randint(2,8) #something to do with jumbled-ness?? It seems like higher= more jumble. don't @ me
chordtype = random.randint(1,4)#see below for chord structures
chordswap = 2*random.randint(1,3)
longparam = 0 #makes bigger pic if long lines
#1 - totally random
#2 - every other line, whole way through
#3 - every other line, swaps every chordswap lines
#4 - every line same, swaps every chordswap lines #technically overlaps 2 but I want to be less common

lyrics = open( file, "r" ).readlines()[1::2] #only take every other line for lyrics
fulltext = open( file, "r" ).readlines() #full text including chords and lyrics
chordout = open("chordout.txt", "w") #new file for chord spacing, apologies

for line in fulltext:
	chordout.write(line.replace('  ', ' ~')) #need spacing of chords for markov chain

chords = open("chordout.txt","r").readlines()[::2] #now do the chord markov, with spacing
chordout.close()

model_lyrics = mfy.NewlineText(lyrics) #create models
model_chords = mfy.NewlineText(chords)

#title and filename making:
title = model_lyrics.make_short_sentence(titlecharacterlength,tries=100,state_size=10) #make a title for the song!
title=' '.join(word[0].upper() + word[1:] for word in title.split())
titlelong = title+'\n\ngenerated from '+bandname
dir_path = os.path.dirname(os.path.realpath(file))
songfilename = dir_path+'\\songs\\'+title+'.txt'

song= open(songfilename, "w") #new file for song with its title
song.write(titlelong+"\n\n\n")

#song generation below, for each chord structure type
if chordtype==1:
    for i in range(songlength): #make a song of length specified
        song.write(model_chords.make_sentence(test_output=False)) #don't care about 'copying'
        song.write("\n")
        song.write(model_lyrics.make_sentence(tries=100,state_size=statesize)) #care about copying
        song.write("\n")
        if random.random()>0.9: #some random riffs for fun
            song.write(model_chords.make_sentence(test_output=False))
            song.write("\n")
    song.write(model_chords.make_sentence(test_output=False)) #closing chords
    song.close()
elif chordtype ==2:
    line1 = model_chords.make_sentence(test_output=False)
    line2 = model_chords.make_sentence(test_output=False)
    for i in range(songlength): #make a song of length specified
        if i%2 ==1:
            song.write(line1) #don't care about 'copying'
        else:
            song.write(line2)
        song.write("\n")
        song.write(model_lyrics.make_sentence(tries=100,state_size=statesize)) #care about copying
        song.write("\n")
        if random.random()>0.9: #some random riffs for fun
           song.write(model_chords.make_sentence(test_output=False))
           song.write("\n")
    song.write(model_chords.make_sentence(test_output=False)) #closing chords

    song.close()
elif chordtype ==3:
    line1 = model_chords.make_sentence(test_output=False)
    line2 = model_chords.make_sentence(test_output=False)
    line3 = model_chords.make_sentence(test_output=False)
    line4 = model_chords.make_sentence(test_output=False)
    for i in range(songlength): #make a song of length specified
        if np.floor(i/chordswap)%2==0:
            if i%2 ==1:
                song.write(line1) #don't care about 'copying'
            else:
                song.write(line2)
        else:
            if i%2 ==1:
                song.write(line3) #don't care about 'copying'
            else:
                song.write(line4)
        song.write("\n")
        song.write(model_lyrics.make_sentence(tries=100,state_size=statesize)) #care about copying
        song.write("\n")
        if random.random()>0.9: #some random riffs for fun
           song.write(model_chords.make_sentence(test_output=False))
           song.write("\n")
    song.write(model_chords.make_sentence(test_output=False)) #closing chords
    song.close()
elif chordtype ==4:
    line1 = model_chords.make_sentence(test_output=False)
    line2 = model_chords.make_sentence(test_output=False)
    for i in range(songlength): #make a song of length specified
        if np.floor(i/chordswap)%2==0:
            song.write(line1) #don't care about 'copying'
        else:
            song.write(line2) #don't care about 'copying'
        song.write("\n")
        sentence = model_lyrics.make_sentence(tries=100,state_size=statesize)
        if len(sentence)>100:
            longparam = 1
        if len(sentence)>150:
            longparam=2
        song.write(sentence) 
        song.write("\n")
        if random.random()>0.9: #some random riffs for fun
           song.write(model_chords.make_sentence(test_output=False))
           song.write("\n")
    song.write(model_chords.make_sentence(test_output=False)) #closing chords
    song.close()


fin = open(songfilename, "rt") #removing tildes again
data = fin.read()
data = data.replace('~', ' ')
print(data) #prints in console if you like
print(chordtype)
print(chordswap)
fin.close()

fin = open(songfilename, "wt") #saving final file out
fin.write(data)
fin.close()
os.remove('chordout.txt') #clear the chordout file, was giving me errors when changing artists

#%% image saving

songfile = open(songfilename,'r')
text = songfile.read()
wide = 15
if longparam==1:
    wide = 20
if longparam==2:
    wide = 25
plt.figure(figsize=(wide,15))
image = plt.text(-.1,.1,text,fontsize=18)
plt.axis('off')
plt.savefig(songfilename.replace('.txt','.png'))

#%% pushing song to twitter

#these don't do anything without the api setup: 

#api.update_with_media(songfilename.replace('.txt','.png'), status=titlelong)

#api.update_status(model_lyrics.make_sentence(tries=100,state_size=statesize)) #send a random sentence











