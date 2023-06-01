from bs4 import BeautifulSoup
import unittest
import lxml
import re

from langchain.schema import Document

class EUDirective:
    def __init__(self, html_file):
        self.html_file = html_file
        self.name = None
        self.soup = None
        self.raw_paragraphs = []
        self.articles = {}

        # Parse the HTML file
        self._parse_html()

        self.title = self._find_title()
        self.date = self._find_date()

        self.articles = self._process_articles()

    def _find_title(self):
        def _title_start_index(paragraphs):
            for i, p in enumerate(paragraphs):
                if p.startswith('REGULATION'):
                    return i
            raise ValueError('No paragraph starts with REGULATION')
        
        start_index = _title_start_index(self.raw_paragraphs)
        return '\n'.join(self.raw_paragraphs[start_index:start_index+3])

    def _find_date(self):
        for p in self.raw_paragraphs:
            if p.startswith('of '):
                return p[3:]
        raise ValueError('No date was found in the HTML')

    def _parse_html(self):
        # Read the HTML file
        with open(self.html_file) as file:
            html = file.read()

        # Create a BeautifulSoup object
        self.soup = BeautifulSoup(html, 'lxml-xml')

        # Extract all paragraphs
        raw_paragraphs = self.soup.find_all('p')
        for paragraph in raw_paragraphs:
            self.raw_paragraphs.append(paragraph.text.replace('\xa0', ' '))

    
    def _process_articles(self):
        start_pattern = r"Article\s\d{1,4}$"

        end_patterns = [r'This\sRegulation\sshall\sbe\sbinding\sin\sits\sentirety\sand\sdirectly\sapplicable\sin\sall\sMember\sStates.']

        current_article = []
        in_article = False
        articles = {}
        for p in self.raw_paragraphs:
            if re.match(start_pattern, p):
                current_article = []
                in_article=True
                articles[p] = current_article
                continue

            if any(map(lambda pat: re.match(pat, p), end_patterns)):
                in_article = False
                current_article = []
                continue

            if in_article:
                current_article.append(p)

        articles = {k: '\n'.join(v) for k, v in articles.items()}
        return articles
    
    def article_to_document(self, article_key):
        return Document(page_content=self.articles[article_key],
                        metadata={'Directive': self.name,
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

    print(len(directive._process_articles()))
    print(directive._process_articles()['Article 9'])