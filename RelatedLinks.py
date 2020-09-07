#######################################################################
# File name: RelatedLinks.py                                  	      #
# Author: PhilipBasaric                                               #
#                                                                     #
# Description: This module returns a list of links that are related   #
# to a given wikipedia article. These links are retrieved from either # 
# the "see also" section or the "category" section.                   #                      	  			
#	                                                                  #
# Parameters: link - a URL addressing a wikipedia page                #
#             n - the threshold for the number of see also links 	  #											  
#																	  #
# Returns: A list of wikipedia URLs that are related to the input URL #                                       
#                                                                     #
#######################################################################

from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from SortPopularLinks import SortPopularLinks
import wikipediaapi
import requests
import re


class RelatedLinks:

    #Arugment(s): A wikipedia page url, the threshold for the number of links (i.e. if n = 5, the length of relatedLinks must be 5)
    #Return(s): A 1D list of links to wikipedia pages that are related to the input page
    @staticmethod
    def getRelatedLinks(url, linkThreshold):
        try:
            webpage = urlopen(url)
        except HTTPError as e:
            print('Page not found')
        except URLError as e:
            print('The server could not be found')
        else:
            print('Retrieval successful')
        bs = BeautifulSoup(webpage.read(), 'html.parser')

        articleName = bs.h1.get_text()

        relatedLinks = []

        if bs.find('span', id="See_also") is not None:
            relatedLinks = RelatedLinks.seeAlsoLinks(bs.h1.get_text())
            if len(relatedLinks) >= linkThreshold:
                sortedLinks = SortPopularLinks.SortPopularLinks(relatedLinks)
                return RelatedLinks.cutList(sortedLinks, linkThreshold)
            elif len(relatedLinks) < linkThreshold:
                addLinks = RelatedLinks.categoryLinks(bs, articleName)
                sortedLinks = SortPopularLinks.SortPopularLinks(addLinks)
                relatedLinks.extend(sortedLinks)
                return RelatedLinks.cutList(relatedLinks, linkThreshold)
        else:
            relatedLinks = RelatedLinks.categoryLinks(bs, articleName)
            sortedLinks = SortPopularLinks.SortPopularLinks(relatedLinks)
            return RelatedLinks.cutList(sortedLinks, linkThreshold)

    #Arugment(s): A beautifulsoup object
    #Return(s): A 1D list containing category links that are found in the first reference under the "categories" section
    @staticmethod
    def categoryLinks(bs, articleName):
        articleName = articleName.replace(" ", "_")
        relatedLinks = []
        link = "https://en.wikipedia.org" + bs.find('div', id="mw-normal-catlinks").find('ul').find('li').find('a').attrs['href']
        page = urlopen(link)
        sub_bs = BeautifulSoup(page.read(), 'html.parser')
        for link in (sub_bs.find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))):
            if ('href' in link.attrs) & (link.attrs['href'].find('Main_Page') == -1) & (link.attrs['href'].find(articleName) == -1):
                relatedLinks.append("https://en.wikipedia.org" + link.attrs['href'])
            if len(relatedLinks) > 20: # HARDCODED LIMIT
                break
        if len(relatedLinks) > 20:
            return relatedLinks[int(((len(relatedLinks)/2)-7)):int(((len(relatedLinks)/2)+7))]
        return relatedLinks

    #Arugment(s): The title of a wikipedia article (the article header)
    #Return(s): A 1D list containing the links found in the "see also" section of the article 
    @staticmethod
    def seeAlsoLinks(articleName):
        relatedLinks = []
        article = articleName
        r = requests.get("https://en.wikipedia.org/w/api.php?action=parse&prop=sections&page=" + article + "&format=json")

        data_dict = r.json()
        data_dict2 = data_dict['parse']
        data = data_dict2['sections']

        index = -1
        for dictionary in data:
            if dictionary['anchor'] == 'See_also':
                index = dictionary['index']
                break
        if index == -1:
            return None

        r = requests.get("https://en.wikipedia.org/w/api.php?action=parse&prop=links&page=" + article + "&section=" + index + "&format=json")

        data_dict = r.json()
        data_dict2 = data_dict['parse']
        data = data_dict2['links']

        for dictionary in data:
            if dictionary['*'].find('Portal:') != -1:
                continue
            identifier = dictionary['*'].replace(" ", "_")
            try:
                print(identifier)
                relatedLinks.append("https://en.wikipedia.org/wiki/" + identifier)
            except Exception as e:
                print(e)
            else:
                continue
        return relatedLinks

    # Helper function - ensures return list is of specified size
    @staticmethod
    def cutList(links, linkThreshold):
        for i in range(0,len(links)):
            if len(links) == linkThreshold:
                break
            links.pop()
        return links


