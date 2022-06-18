import requests
from bs4 import BeautifulSoup, NavigableString

import hashlib


def quotes_by_author(author, page_num=None):

	old_author = author

	author = author.replace(" ", "+")

	all_quotes = []

	# if page number not specified, get true page number
	if page_num is None:
		try:
			page = requests.get("https://www.goodreads.com/quotes/search?commit=Search&page=1" + "&q=" + author + "&utf8=%E2%9C%93")
			soup = BeautifulSoup(page.text, 'html.parser')
			pages = soup.find(class_="smallText").text
			a = pages.find("of ")
			page_num = pages[a+3:]
			page_num = page_num.replace(",", "").replace("\n", "")
			page_num = int(page_num)
			print("looking through", page_num, "pages")
		except:
			page_num = 1

	# for each page
	for i in range(1, page_num+1, 1):

		try:
			page = requests.get("https://www.goodreads.com/quotes/search?commit=Search&page=" + str(i) + "&q=" + author + "&utf8=%E2%9C%93")
			soup = BeautifulSoup(page.text, 'html.parser')
			print("scraping page", i)
		except:
			print("could not connect to goodreads")
			break
			
		try:
			quote = soup.find(class_="leftContainer")
			quote_list = quote.find_all(class_="quoteDetails")
		except:
			pass

		# get data for each quote
		for quote in quote_list:

			meta_data = {}

			# Get quote's text
			try:
				outer = quote.find(class_="quoteText")
				inner_text = [element for element in outer if isinstance(element, NavigableString)]
				inner_text = [x.replace("\n", "") for x in inner_text]
				final_quote = "\n".join(inner_text[:-4])
				meta_data['text'] = final_quote.strip()
				final_quote_encoded = final_quote.strip().encode()                
				meta_data['_id'] = hashlib.sha256(final_quote_encoded).hexdigest()                 
			except:
				pass 
                
                
            
             

			# Get quote's author
			try:
				author = quote.find(class_="authorOrTitle").text
				author = author.replace(",", "")
				# author = author.replace("\n", "")
				meta_data['author'] = author.strip()
				# print(author)
			except:
				meta_data['author'] = None

			# Get quote's book title
			try: 
				title = quote.find(class_="authorOrTitle")
				title = title.nextSibling.nextSibling.text
				# title = title.replace("\n", "")
				meta_data['title'] = title.strip()
				# print(title)
			except:
				meta_data['title'] = None

			# Get quote's tags
			try:
				tags = quote.find(class_="greyText smallText left").text
				tags = [x.strip() for x in tags.split(',')]
				tags = tags[1:]
				meta_data['tags'] = tags
				# print(tags)
			except:
				meta_data['tags']=None

			# Get number of likes
			try:
				likes = quote.find(class_="right").text
				likes = likes.replace("likes", "")
				likes = int(likes)
				meta_data['likes'] = likes
				# print(likes)
			except:
				meta_data['likes'] = None

			all_quotes.append(meta_data)


# 		for text, author, title, tags, likes in all_quotes:
# # 			print(text)
# # 			print(author)
# # 			print(title)
# # 			print(tags)
# # 			print(likes)
# # 			print()

	return all_quotes

author = input('Which author')
listofquotes = quotes_by_author(author)


import pandas as pd
import numpy as np  

df = pd.DataFrame(listofquotes)
df['text'].replace('', np.nan, inplace=True)
newdf = df.dropna(subset=['text'])
df_filtered = newdf[newdf['_id'] != "296824c5dbab2caa08ae2570641c5b09e8ede6acbed110ead2b348f17da6662c"]
df_final = df_filtered.drop_duplicates(subset=['text'])

# importing module
from pymongo import MongoClient

# creation of MongoClient
client=MongoClient()

# Connect with the portnumber and host
client = MongoClient("mongodb://kratos0002:Mongodbsucks.123@ac-8w501ar-shard-00-00.u5ocxsz.mongodb.net:27017,ac-8w501ar-shard-00-01.u5ocxsz.mongodb.net:27017,ac-8w501ar-shard-00-02.u5ocxsz.mongodb.net:27017/?ssl=true&replicaSet=atlas-vu9haa-shard-0&authSource=admin&retryWrites=true&w=majority")


db = client.quotesdb

records = db.malazanq
dict = df_final.to_dict('records')
records.insert_many(dict)