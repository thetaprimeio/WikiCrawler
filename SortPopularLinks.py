#######################################################################
# File name: sortPopularLinks.py                                  	  #
# Author: PhilipBasaric, JordanCurnew                                 #
#                                                                     #
# Description: This module takes as an argument a list of wikipedia   #
# links and returns a list of the wikipedia links along with their	  #
# view count sorted from highest to lowest views.	  				  #
#																	  #											  
#																	  #
# Returns: Sorted 2D list of a wikipedia page URLs and its total views#           
#                                                                     #
#######################################################################

import requests

class sortPopularLinks:

    #Arugment(s): A list of Wikipedia page URLs
    #Return(s): A 2D list of Wikipedia page URLs containing the URL and views. Sorted in descending order.
    @staticmethod
    def sortPopularLinks(linksList):
        sortedLinks = []
        returnLinks = []

        for link in linksList:
            articleName = link.split('wiki/',1)[1]
            numViews = sortPopularLinks.getArticlePopularity(articleName)
            sortedLinks.append([link, numViews])
        
        sortedLinks.sort(key = lambda x: x[1], reverse=True)

        for link in sortedLinks:
            returnLinks.append(link[0])

        return returnLinks
   
    
    # Wikipedia RestAPI GET format: https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}
    #Argument(s): Wikipedia article name
    #Return(s): Total views for the page (Integer)
    @staticmethod
    def getArticlePopularity(articleName):
        article = articleName
        api_version = "rest_v1"
        api_base_url = f"https://wikimedia.org/api/{api_version}"
        endpoint_path = f"/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article}/monthly/2015100100/2020060100"
        endpoint = f"{api_base_url}{endpoint_path}"

        r = requests.get(endpoint)

        data_dict = r.json()

        try:
            list_data = data_dict['items']
            return sortPopularLinks.getViews(list_data)
        except Exception as e:
            return 0


    #Argument(s): Data given from the Wikipedia RestAPI for a Wikipedia article
    #Return(s): Total view count for the Wikipedia article
    @staticmethod
    def getViews(data):
        totalViews = 0
        temp = {}
        for i in range(0, len(data)-1):
            temp = data[i] 
            totalViews += temp['views']
        return totalViews