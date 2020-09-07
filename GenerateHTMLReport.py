################################################################################################
#  File name: generateHTMLReport.py
#  Author: BenjaminBeggs
#
# Description: Takes in a set of page summaries and outputs a corresponding
#              HTML newsletter for the user provided topic
#
# Parameters : topic set (lists containing [0] title, [1] summary, [2] image] for the topic)
#
# Returns : None
################################################################################################

import zipfile # To extract the HTML template archive
import textwrap # For string truncation
from shutil import copyfile

# Extract the HTML template archive
with zipfile.ZipFile('HTML_TEMPLATE.zip', 'r') as zip_ref:
    zip_ref.extractall()

class generateHTMLReport:
    def genReport(self, main_topic, related_topic1, related_topic2):
        reportName = 'report-' + main_topic[0] + '.html'
        copyfile('report.html', reportName)
        # Fill in the topic title section of HTML template
        self.replaceAll('report.html', 'TOPIC_TITLE_TAG', main_topic[0], main_topic[0])
        # Fill in the topic summary section of HTML template
        self.replaceAll('report.html', 'TOPIC_SUMMARY_TAG', main_topic[1], main_topic[0])
        # Replace the image tag with the appropriate file name
        if main_topic[2] is not None:
            self.replaceAll('report.html', 'TOPIC_IMAGE_NAME', main_topic[2], main_topic[0])
        else:
            self.replaceAll('report.html', 'TOPIC_IMAGE_NAME', 'noImage.png', main_topic[0])
        # Fill in the related topic sections
        self.replaceAll('report.html', 'RELATED_TOPIC1_TITLE_TAG', related_topic1[0], main_topic[0])
        self.replaceAll('report.html', 'RELATED_TOPIC1_SUMMARY_TAG', textwrap.shorten(related_topic1[1], width=250, placeholder="..."), main_topic[0])
        self.replaceAll('report.html', 'RELATED_TOPIC2_TITLE_TAG', related_topic2[0], main_topic[0])
        self.replaceAll('report.html', 'RELATED_TOPIC2_SUMMARY_TAG', textwrap.shorten(related_topic2[1], width=250, placeholder="..."), main_topic[0])
        self.replaceAll('report.html', 'RELATED_TOPIC1_LINK', "https://en.wikipedia.org/wiki/" + related_topic1[0].replace(' ', '_'), main_topic[0])
        self.replaceAll('report.html', 'RELATED_TOPIC2_LINK', "https://en.wikipedia.org/wiki/" + related_topic2[0].replace(' ', '_'), main_topic[0])
        return 'report-' + main_topic[0] + '.html'
        
    # Helper function to read and replace lines in the HTML template
    def replaceAll(self, filename, searchExp, replaceExp, topic):
        reportName = 'report-' + topic + '.html'
        with open(reportName, 'r', encoding='utf-8') as file:
          filedata = file.read()
        filedata = filedata.replace(searchExp, replaceExp)
        with open(reportName, 'w', encoding='utf-8') as file:
          file.write(filedata)