
import pandas as pd
import numpy as np
import string

from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use('seaborn')

from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
import nltk.data
nltk.download('vader_lexicon')
nltk.download('punkt')


lyricslist = [{'lyrics': "Intro]\nI do not talk, I am just a rapper\n\n[Verse]\nI am so different, being me is like the lottery\nI am so on like the TV when you fall asleep\nNiggas makin pottery, but I broke the mold\nNow my shit has got them dancing like a baby Oakenfold\nYes, I got a lust for life, and I drink my weight in whiskey\nAnd these hoes are actin' different cause I'm Rich comma Richie\nThese friends are iffy, they're alcoholic geniuses\nI think they hang around until I'm drunk and buy them Guinnesses\nI gotta drink my medicine to cover what's inside of me\nI'm still fucked up from the days nobody liked me\nI'm lying just a little when I say that I don't give a fuck\nYou know I gotta give a fuck\nYou know I gotta give a fuck\nMy face is broken out\nMy shirt is hand-me-down\nThis kid named Vincent wanna take my shirt and lay me out\nI'm trying to fit in like a fat bitch in her shoe size\nIt's funny how I'm flyer now than witches on their broom rides\nI always thought these new clothes were the potion\nCause I never felt that good in my own skin\nIt's probably cause I'm the only black kid in my school\nAnd when I meet another black kid they tell me I'm a fool\nCause I wear these tight clothes, tight jeans, tight shirt\nYeah I stay tight like these girls that make my dick hurt\nYeah, I'm self conscious\nGo ahead, laugh it up\nCause I dig deep and pull something out to back it up\nThey told my ass to blacken up\nWhat the fuck are you?\nYou don't even say shit\nQuit writing gay shit\nNow they see me, have to squint like Asians\nCause I'm too bright like an old night light\nWhen I do not talk, I am being polite\nRap all night\nAct all day\nMama so scared 'imma waste away\nI don't have time to sleep\nI don't have time to eat\nThese niggas got time to do\nEverything but be unique\nI gotta do me like I'm jerkin' to a mirror\nI am just a rapper\nCan't make it clearer\nTo every kid in a world full of pain\nPlease give a listen to this song and my name\nChildish Gambino\nWe are all children\nI am just a murderer\nMan, I just killed this"},{'lyrics': "Intro]\nI do not talk, I am just a rapper\n\n[Verse]\nI am so different, being me is like the lottery\nI am so on like the TV when you fall asleep\nNiggas makin pottery, but I broke the mold\nNow my shit has got them dancing like a baby Oakenfold\nYes, I got a lust for life, and I drink my weight in whiskey\nAnd these hoes are actin' different cause I'm Rich comma Richie\nThese friends are iffy, they're alcoholic geniuses\nI think they hang around until I'm drunk and buy them Guinnesses\nI gotta drink my medicine to cover what's inside of me\nI'm still fucked up from the days nobody liked me\nI'm lying just a little when I say that I don't give a fuck\nYou know I gotta give a fuck\nYou know I gotta give a fuck\nMy face is broken out\nMy shirt is hand-me-down\nThis kid named Vincent wanna take my shirt and lay me out\nI'm trying to fit in like a fat bitch in her shoe size\nIt's funny how I'm flyer now than witches on their broom rides\nI always thought these new clothes were the potion\nCause I never felt that good in my own skin\nIt's probably cause I'm the only black kid in my school\nAnd when I meet another black kid they tell me I'm a fool\nCause I wear these tight clothes, tight jeans, tight shirt\nYeah I stay tight like these girls that make my dick hurt\nYeah, I'm self conscious\nGo ahead, laugh it up\nCause I dig deep and pull something out to back it up\nThey told my ass to blacken up\nWhat the fuck are you?\nYou don't even say shit\nQuit writing gay shit\nNow they see me, have to squint like Asians\nCause I'm too bright like an old night light\nWhen I do not talk, I am being polite\nRap all night\nAct all day\nMama so scared 'imma waste away\nI don't have time to sleep\nI don't have time to eat\nThese niggas got time to do\nEverything but be unique\nI gotta do me like I'm jerkin' to a mirror\nI am just a rapper\nCan't make it clearer\nTo every kid in a world full of pain\nPlease give a listen to this song and my name\nChildish Gambino\nWe are all children\nI am just a murderer\nMan, I just killed this"}]

df = pd.DataFrame(lyricslist)

print(df)

def unique(list1):
     unique_list = []
     for x in list1:
         if x not in unique_list:
              unique_list.append(x)
     return unique_list

words = []

