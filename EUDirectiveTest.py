import unittest
from EUDirective import EUDirective

class TestEUDirective(unittest.TestCase):
    def setUp(self):
        self.directive = EUDirective('dlt_pilot.html')

    def test_title(self):
        true_title = """REGULATION (EU) 2022/858 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL
of 30 May 2022
on a pilot regime for market infrastructures based on distributed ledger technology, and amending Regulations (EU) No 600/2014 and (EU) No 909/2014 and Directive 2014/65/EU"""
        self.assertEqual(self.directive.title, true_title)

    def test_date(self):
        true_date = '30 May 2022'
        self.assertEqual(self.directive.date, true_date)

    def test_articles(self):
        true_number_of_articles = 19
        self.assertEqual(len(self.directive.articles), true_number_of_articles)

if __name__ == '__main__':
    unittest.main()
