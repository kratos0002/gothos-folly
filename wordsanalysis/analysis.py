
import pandas as pd
import numpy as np
import string

from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use('seaborn')

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
import nltk.data
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
nltk.download('wordnet')
nltk.download('omw-1.4')
from nrclex import NRCLex

#import libraries
from pyecharts.charts import Bar
from pyecharts import options as opts


# importing module
from pymongo import MongoClient

# creation of MongoClient
client=MongoClient()

# Connect with the portnumber and host
client = MongoClient("mongodb://kratos0002:Mongodbsucks.123@ac-8w501ar-shard-00-00.u5ocxsz.mongodb.net:27017,ac-8w501ar-shard-00-01.u5ocxsz.mongodb.net:27017,ac-8w501ar-shard-00-02.u5ocxsz.mongodb.net:27017/?ssl=true&replicaSet=atlas-vu9haa-shard-0&authSource=admin&retryWrites=true&w=majority")

db = client.musicdb

records = db.music_c

y= []
for x in records.find({'artist': 'Eminem'}):
    y.append(x)


dfy = pd.DataFrame(y)
dfy = dfy.astype({"lyrics": str})

dfy['newlyrics'] = dfy.groupby(['artist'])['lyrics'].transform(
                                              lambda x: ' '.join(x))

 # lyricsdict = {'title':"abc", 'lyrics':"[Intro: Sway]\nDJ Wonder\nWe gon' rock at least 5 beats, to show your versatility\nWhat you're made of\nYou gotta rock 5 back, aiight?\nHere we go. Childish Gambino, let's go\n\n[Verse 1]\nAs the world's turnin', I feel like I'm a worse person\nMy tongue's hurtin', from all of its work cursin'\nAnd I'm not certain I think my father's Lavar Burton\n'Til I'm walkin' in circles and I'm talkin' in third person\nIn the eighth grade I got high off paper maché\nI put it in my desk and I let it ferment a day\nCause shit, ain't nothin' changed\nI'm still known as a rude student\nThat'll walk inside your class and make fun of your school shootin'\nI can prove it\nI'm too cool as a matter of fact\nI've been writin' these verses while I'm havin' a heart attack\nI'm in your bedroom, crankin' No Doubt and Staring Back\nStereo blaring, Gwen Stefani can holla black\nI'm not black, I'm a white boy with dark skin\nAt a Klan rally, wondering why they won't let me in\nI'm drunk off this gin and I'm high off Ritalin\nFuck it, let me get to the next beat\n[Verse 2]\nI'm the nerdiest rapper ever\nI'm wearing a Cosby sweater\nAnd reading Oscar Wilde\nRipping my foreskin to make a washable condom\nA bunch of assassins tried to jump me\nThey couldn't touch me\nI rolled off in a yellow Humvee with a bunch of monkeys\nMy taste buds hate fudge, man\nPlus I'm allergic\nI'mma dress up like a surgeon so I could hurt Curtis on purpose\nAnd girls see my dick size and they realize\nThat they can't handle it\nI get more sodomy than Tommy Lee and Pam... Anderson?\nWith my du-rag in my left hand\nAnd my iPod and my diskman\nI get more kicks out of it than Jean Claude Van Damm\nAnd I'm still spittin', I'm still hittin'\nBig pimpin' like Hova\nYo, let me be the rap...run over\nYea, lemme go, lemme go\n\n[Verse 3]\nChildish Gambino, yo this off the dome\nI gotta keep it goin' cause I came from home\nCome from Rome, Athens\nOr Atlanta, Georgia\nGot somethin' for ya\nYes I got some s'mores cause I'll boil you\nLike I got that Goya\nYou know how they play Reggaeton in the beats\nWhen you in NYC\nMeaning that me and I'm sickest\nYo, Aaahh!!! Real Monsters Like Ickis\nYo, this chick that I used to lick it\nNow her name Aubrey Plaza\nI didn't mean to kick it while I'm gettin' salsa\nLike I'm eatin' salsa, cause she Puerto Rican\nSome people speakin' like she ain't white\nBut you know that's alright 'cause I keep it tight\n"}


newdf = dfy['newlyrics']
newdf = newdf.drop_duplicates()
# print(newdf)

# df = pd.DataFrame(lyricsdict)

dict = newdf.to_dict()

# print(dict)

def process_text(raw_text):
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    
    text = re.sub(r"[^a-zA-Z0-9]", " ", raw_text.lower().strip())
    tokens = word_tokenize(text)
    lemmed = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    lemmed_tokens = [WordNetLemmatizer().lemmatize(w, pos='v') for w in lemmed]  # lemm to verbs, not nouns 
    return lemmed_tokens


lyrics_dict_clean = process_text(dict[0])

# print(lyrics_dict_clean)


# https://www.geeksforgeeks.org/emotion-classification-using-nrc-lexicon-in-python/


new_dict =[]
for i in range(len(lyrics_dict_clean)):
 
  
    emotion = NRCLex(lyrics_dict_clean[i])
    
    new_dict.append(emotion.raw_emotion_scores)
 
# print(new_dict)


    # print('\n\n', lyrics_dict_clean['lyrics'][i], ': ', emotion.affect_frequencies)



dfnew = pd.DataFrame(new_dict)
df1_transposed = dfnew.T

df1_transposed= df1_transposed.fillna(0)
df1_transposed['sum'] = df1_transposed.sum(axis=1)
df1_transposed = df1_transposed.reset_index(level=0)


emotion = df1_transposed['index']
sumofemotion = df1_transposed['sum']
plt.figure(dpi=300)

plt.bar(emotion, sumofemotion)
plt.title('Song and Emotions graph')
plt.xlabel('Emotions')
plt.ylabel('Artist')

ax= plt.subplot()
plt.plot(emotion, sumofemotion)
plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

plt.show()