from bs4 import BeautifulSoup
import unittest
import lxml
import re

from langchain.schema import Document

class EUDirective:
    def __init__(self, html_file):
        self.html_file = html_file
        self.soup = None
        self.raw_paragraphs = []
        self.articles = {}

        self.annexes = []

        self.title_classes = {'doc-ti', 'oj-doc-ti'}

        self.article_classes = {'oj-ti-art', 'ti-art'}

        self.directive_end_classes = {'oj-final', 'final', 'signatory', 'oj-signatory'}

        # Parse the HTML file
        self._parse_html()

        self.title, self.date, self.annexes = self._find_metadata()

        self.articles = self._process_articles()

    def _find_metadata(self):
        def is_title(element):
            if element in self.title_classes:
                return True
            return False
        
        title_elements = self.soup.find_all('p', is_title)

        title = title_elements[0].text
        date = title_elements[1].text[3:]
        annexes = [t.text for t in title_elements if t.text.startswith('ANNEX')]
        return title, date, annexes

    def _parse_html(self):
        # Read the HTML file
        with open(self.html_file) as file:
            html = file.read()

        # Create a BeautifulSoup object
        self.soup = BeautifulSoup(html, 'lxml-xml')

        # Extract all paragraphs
        raw_paragraphs = self.soup.find_all('p')
        for paragraph in raw_paragraphs:
            self.raw_paragraphs.append(paragraph.text)

    
    def _process_articles(self):
        start_pattern = r"Article\s\d{1,4}$"

        end_patterns = [r'This\sRegulation\sshall\sbe\sbinding\sin\sits\sentirety\sand\sdirectly\sapplicable\sin\sall\sMember\sStates.']

        current_article_text = []
        current_article_name = ''
        in_article = False
        articles = {}
        for p in self.soup.find_all('p'):
            if p.attrs.get('class', '') in self.article_classes:
                print(f"Starting article {p.text}. Currently in article: {in_article}")
                if in_article:
                    articles[current_article_name] = current_article_text
                in_article = True
                current_article_text = []
                current_article_name = p.text.replace('\xa0', ' ')
                continue

            if p.attrs.get('class', '') in self.directive_end_classes:
                if in_article:
                    articles[current_article_name] = current_article_text
                break

            if in_article:
                current_article_text.append(p.text.replace('\xa0', ' '))

        for k, v in articles.items():
            print(len(v))
        articles = {k: '\n'.join(v) for k, v in articles.items()}
        return articles
    
    def article_to_document(self, article_key):
        return Document(page_content=self.articles[article_key],
                        metadata={'Directive': self.title,
                                  'Date': self.date,
                                  'Article': article_key})
    
    def get_documents(self):
        """
        Represents the directive as langchain documents
        """

        output = []
        for art in self.articles:
            output.append(self.article_to_document(art))

        return output


if __name__=='__main__':
    directive = EUDirective('dlt_pilot.html')

    print(directive.articles.keys())
    #print(directive.articles[list(directive.articles.keys())[18]])