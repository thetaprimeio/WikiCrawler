################################################################################################
#  File name: retrieveURL.py
#  Author: BenjaminBeggs
#
# Description: Takes in a string specifying a topic of interest and returns the best matched
#              Wikipedia page article for the topic.
#
# Parameters : topic_string (string label for the topic of interest)
#
# Returns : url (a string containing the full page URL of the Wikipedia topic match)
#           Boolean (True indicates a direct page match was found, False indicates the nearest
#           search result was used)
################################################################################################

from bs4 import BeautifulSoup # Used for HTML parsing
from urllib.request import urlopen # For web page internet retrieval
from urllib.error import HTTPError # Exception catch for missing article page
from urllib.error import URLError # Exception catch for DNS error
import sys # For program termination following DNS error

class retrieveURL:
    @staticmethod
    def retrieveURL(topic_string):
        # Replace space characters with underscores
        topic_string = topic_string.replace(' ', '_')
        # Attempt to generate a direct Wikipedia article match based on the user topic string
        url = "https://en.wikipedia.org/wiki/" + topic_string
        try:
            html = urlopen(url)
            bs = BeautifulSoup(html.read(), 'html.parser')
            if 'may refer to:' in str(bs):
                raise Exception('May refer to page retrieved by article tag.')
        except HTTPError as e:
            # Indicative of no direct article match, search for closest match
            search_url = "https://en.wikipedia.org/w/index.php?search=" + topic_string.replace('_', '+')
            search_html = urlopen(search_url)
            # Open return HTML
            bs = BeautifulSoup(search_html.read(), 'html.parser')
            # Isolate top search result, first element with CSS class 'mw-search-result-heading'
            top_match = bs.select_one('.mw-search-result-heading')
            # Check if no article at all has been found
            if 'There were no results matching the query.' in str(bs):
                return 'ERROR_TOPIC', False
            if top_match is not None:
                # URL extension given by the href of the first <a> tag
                url = "https://en.wikipedia.org" + top_match.find('a').attrs['href']
            # Redirect case whereby a search time will instantly redirect to the proper article
            else:
                url = search_html.geturl()
            return url, False
        # Take the first link recommended
        except Exception as e:
            set = str(bs)
            set = set[set.find('<li><a href="/wiki/')+len('<li><a href="/wiki/'):len(set)]
            set = set[:set.find('"')]
            url = "https://en.wikipedia.org/wiki/" + set
            return url, False
        except URLError as e:
            # Likely a DNS error on the user machine
            input("The server could not be found. This program will exit following user keypress.")
            sys.exit()
        else:
            # Direct article URL match successful
            return url, True
