#######################################################################
# File name: RetrievePageInfo.py                                      #
# Author: PhilipBasaric                                               #
#                                                                     #
# Description: Takes url of given page as input, returns a list 	  #
# containing the page header, summary, and image to be used in the    #
# pdf doc.															  #
#																	  #
# Parameters: url - the url of a given page  						  #
#																	  #
# Returns: List of the form [title, summary, image]					  #
#                                                                     #
#######################################################################


from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import wikipediaapi
import requests
import re
import time 
import random


class RetrievePageInfo:

	# This function retrieves the page info of a given wikipedia article 
	@staticmethod
	def getPageInfo(url):
		try:
			html = urlopen(url)
		except HTTPError as e:
			print('Page could not found')
		except URLError as e:
			print('The server could not be found')
		else:
			print('Retrieval successful.')

		bs = BeautifulSoup(html.read(), 'html.parser')
		
		title = bs.find('h1').get_text()
		summary = RetrievePageInfo.getText(bs)
		image = RetrievePageInfo.getImage(bs)

		return [title, summary, image]

	# This function retrieves the summary text from the selected article
	@staticmethod 
	def getText(bs):
		wiki_wiki = wikipediaapi.Wikipedia('en')
		articleTitle = bs.find('h1').get_text()
		page = wiki_wiki.page(articleTitle)
		return page.summary 

	# This function retrieves the image associated with the article (this is the image that appears in the topic summary box)
	@staticmethod
	def getImage(bs):
		try:
			imgLoc = bs.find('meta', property='og:image')['content']
			imageName = bs.h1.get_text()+  ".png"
			urlretrieve(imgLoc, imageName) # save image to workspace folder with specified file name 'imageName'
		except Exception as e:
			print("No image found.")
		else:
			imageName = None # if no image is present in article, return None
		return imageName