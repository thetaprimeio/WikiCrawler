####################################################################################################
#  File name: server.py
#  Author: JordanCurnew
#
# Description: Launches the html user-interface at localhost:8080
#              
#
# Parameters : None
#
# Returns : None
####################################################################################################


import http.server
import socketserver
import re
import urllib.parse
import webbrowser
from LogicModule_web import LogicModuleWeb

#Handler to handle GET requests
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
       #this code execute when a GET request happen, then you have to check if the request happenned because the user pressed the button
        if self.path.find("isButtonPressed=true") != -1:
            print("Button clicked")
            print("test 2")
            URLstring = self.path
            topic = urllib.parse.unquote(re.search("/\?name=(.*?)&isButtonPressed", URLstring).group(1)).replace('+',' ')
            print(topic)

            #Run the program with the user chosen topic.
            if LogicModuleWeb.runProgram(topic) == "ERROR_TOPIC":
                print('server.py got here')
                self.path = "#error"
            else:
                print('got to else')
                self.path = LogicModuleWeb.runProgram(topic)

        return super().do_GET()


PORT = 8080
myHandler = Handler

with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()