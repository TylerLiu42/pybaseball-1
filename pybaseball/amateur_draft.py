import pandas as pd
import requests 
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage

class Client(QWebEnginePage):
    
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()
        
    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def amateur_draft(year, round):
    round = round.replace('s', '.5')
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', None)
    url = f"https://www.baseballamerica.com/draft-history/mlb-draft-database/#/?Year={year}&Round={round}"
    page = Client(url)
    soup = BeautifulSoup(page.html, 'html.parser')
    js_test = soup.find('table', class_='draft-search-table')
    draftResults = pd.read_html(soup.prettify())
    draftResults = postprocess(draftResults)
    return draftResults

def postprocess(draftResults):
    for draftee in draftResults:
        draftee.drop(['Year', 'Team', 'Reports'], axis=1, inplace=True)
    return draftResults

#amateur_draft(2019, '1s')