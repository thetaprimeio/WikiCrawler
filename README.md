# WikiCrawler

### Introduction 
WikiCrawler is a web scraper that helps people explore their interests and learn more about a subject by providing the user with formatted HTML documents of wikipedia article summaries and images along with suggestions for further reading. WikiCrawler makes use of the Wikimedia REST API to obtain aggregate article view counts which it uses to sort related articles from most to least relevant. The two most relevant articles are then presented to the user as suggestions for further reading.

### Program modules
The WikiCrawler functionality has been implemented as six distinct program modules

#### RetrieveURL 
This module takes in a string specifying a topic of interest and returns the best matched Wikipedia page article for the topic.
#### RelatedLinks
This module takes in a wikipedia url and returns a list of links that are related to the given article. These links are retrieved from either the "see also" section or the first link in the related categories section of a wikipedia page. 
#### SortPopularLinks
This module takes as an argument a list of wikipedia links and returns a list of the wikipedia links along with their view count sorted from highest to lowest views.	 
#### RetrievePageInfo
This module takes in a url of given page as input and returns a list containing the page header, summary, and image to be used in the formatted HTML document.			
#### GenerateHTMLReport
This module takes in a set of page summaries and outputs a corresponding HTML newsletter for the user provided topic.
#### LogicModule_web
Logic module combining all the modules together to run the program. This is the web version.

### Conclusions 
1. Relevance of topic suggestions can be improved by considering additional metrics 
2. Improvement in run time and category search space can be achieved by hosting on a cloud server 
3. Additional product features such as automated emails containing summary documents can be added to improve user experience  

### How to run the code
To use WikiCrawler, simply run server.py and provide a topic of interest when prompted. Ensure that you have the following libraries installed: 
- beautifulsoup4
- requests
- urllib3
- wikipediaapi
- socketserver
- http

### Contact information 

For any communication relating to this project, please email us at contact@thetaprime.io.

![alt text](thetaprime_shape.png)
