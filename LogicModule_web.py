####################################################################################################
#  File name: LogicModule_web.py
#  Author: JordanCurnew
#
# Description: Logic module combining all the modules together to run the program.
#              This is the web version.
#
# Parameters : userTopic: The user chosen topic 
#
# Returns : The name of the report HTML file or the string "ERROR_TOPIC" to flag an error
####################################################################################################


from RetrieveURL import retrieveURL
from RelatedLinks import RelatedLinks
from RetrievePageInfo import RetrievePageInfo
from GenerateHTMLReport import generateHTMLReport

class LogicModuleWeb:
    @staticmethod
    def runProgram(userTopic):
        print('|----- WikiCrawler Web: Console Log -----|')

        #Get the topic of interest from the user and find a corresponding Wikipedia page URL
        userWikiLink, directMatchBool = retrieveURL.retrieveURL(userTopic)
        if userWikiLink == "ERROR_TOPIC":
            return "ERROR_TOPIC"
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
        return reportGenerator.genReport(articleSummaries[0], articleSummaries[1], articleSummaries[2])