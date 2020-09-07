####################################################################################################
#  File name: LogicModule_console.py
#  Author: JordanCurnew
#
# Description: Logic module combining all the modules together to run the program.
#              This is the console version.
#
# Parameters : None
#
# Returns : Generates an HTML document containing summary information on the topic & related topics
####################################################################################################


from RetrieveURL import retrieveURL
from RelatedLinks import RelatedLinks
from RetrievePageInfo import RetrievePageInfo
from GenerateHTMLReport import generateHTMLReport


print('|---------- Welcome to WikiCrawler ----------|')

#Get the topic of interest from the user and find a corresponding Wikipedia page URL
userTopic = input("Type in a topic of interest:")
userWikiLink, directMatchBool = retrieveURL.retrieveURL(userTopic)

while userWikiLink == "ERROR_TOPIC":
    print("A Wikipedia page could not be found for your topic. Please try with a different topic.")
    userTopic = input("Type in a topic of interest:")
    userWikiLink, directMatchBool = retrieveURL.retrieveURL(userTopic)
    
print(userWikiLink)
if directMatchBool == False:
    print('A direct match could not be found, a close match will be provided instead.')

#Find related topics sorted by popularity (second argument is the amount of topics to return)
relatedTopics = RelatedLinks.getRelatedLinks(userWikiLink, 2)
print('relatedTopics:')
print(relatedTopics)


articleSummaries = []
#Get the main topic summary and add it to the articleSummaries list
firstSummary = RetrievePageInfo.getPageInfo(userWikiLink)
articleSummaries.append(firstSummary)

print("firstSummary:")
print(firstSummary)

#Loop through all of the related topic URLs and append their summaries to articleSummaries
for article in relatedTopics:
    articleSummary = RetrievePageInfo.getPageInfo(article)
    articleSummaries.append(articleSummary)

print('articleSummaries:')
print(articleSummaries)

#Produce the HTML document of the first three topic summaries
reportGenerator = generateHTMLReport()
reportGenerator.genReport(articleSummaries[0], articleSummaries[1], articleSummaries[2])
input("Complete: The HTML document has been created.")